# Deploy containerized Monitoring stack tailord for your needs

Here we will deploy pre-configured Promtheus and Grafana docker images with our configuration, and we will run them just to check that it correctly works. (no use of docker compose because it will be deployed in kubernetes in another repo =) ) 

## Prometheus image configuration

So we need to start with prometheus (in this exemple node-exporter is already running as nd-exporter and listening on port 9100)

The directory dedicated for prometheus build in this repo is in :
03-Docker/Dockerfile/Monitoring/Prometheus

So the prometheus configuration file is defined like this :
```yaml
### SIMPLE PROMETHEUS FILE


# my global config
global:
  scrape_interval: 15s # Set the scrape interval to every 15 seconds. Default is every 1 minute.
  evaluation_interval: 15s # Evaluate rules every 15 seconds. The default is every 1 minute.
  # scrape_timeout is set to the global default (10s).

# Alertmanager configuration
alerting:
  alertmanagers:
    - static_configs:
        - targets:
          # - alertmanager:9093

# Load rules once and periodically evaluate them according to the global 'evaluation_interval'.
rule_files:
  # - "first_rules.yml"
  # - "second_rules.yml"

# A scrape configuration containing exactly one endpoint to scrape:
# Here it's Prometheus itself.
scrape_configs:
  # The job name is added as a label `job=<job_name>` to any timeseries scraped from this config.
  - job_name: "prometheus"

    # metrics_path defaults to '/metrics'
    # scheme defaults to 'http'.

    static_configs:
      - targets: ["localhost:9090"]

  - job_name: "node exporter"


    static_configs:
      - targets: ["nd-exporter:9100"]
```
There a 2 jobs, one for prometheus to scrap himself (base set up), and the second one is for the nd-exporter that is already running in a container (check 03-Docker/00-Install-and-setup/Monitoring-with-Docker.md)

Here is the Dockerfile :
```Dockerfile
# syntax=docker/dockerfile:1

FROM prom/prometheus

# push prometheus.yml with the scraping jobs needed

COPY promtheus.yml /etc/prometheus/prometheus.yml
```
The image selected is already downloaded and is the original one create by prometheus "/prom/prometheus".
The second part will copy the configuration file to erase the base configuration from prometheus image with the one configured for our needs.

So now you can start your image :
```shell
docker build -t test-prometheus:latest .
```
Check that it's correctly build :`
```shell
docker image ls | grep test-prometheus
```
Output : 
```shell
test-prometheus                    latest    eefb909112d4   28 minutes ago   295MB
```

Now run it with :
```shell 
docker run --name Prom -d -p 127.0.0.1:9090:9090 test-prometheus.latest
```
And now connect it to the already created docker network "monitoring" (check 03-Docker/00-Install-and-setup/Network-Docker.md):
```shell
docker network connect monitoring Prom
```
Now inspect your network : 
```shell
docker network inspect Prom
```
You can now access "Prom" container in your browser with localhost:9090, and Prom is monitoring nd-exporter.

## Grafana image Configuration

Now for the setup of Grafana a few files, but we will not be working with the api to create new users.
So as usual to create an image, create a directory for your image.
```shell
mkdir /monitoring/grafna
```
Secondly parameter and create "grafana.ini", this is the file that will be run by grafana a the start of the container or server (here it's a container). We will not check here all of the part of configuring grafan, we will just modidy the administrator by our wanted name and password.
```ini
[security]
# disable creation of admin user on first start of grafana
;disable_initial_admin_creation = false

# default admin user, created on startup
admin_user = grafana

# default admin password, can be changed before first start of grafana,  or in profile settings
admin_password = 0000
```
The second part is the datasources. The datasources are the endpoint where grafana will go fetch the data that will be displayed in the dashboard. This setup is configured to check prometheus data from our Prometheus container.
```yaml
apiVersion: 1
datasources:
  - name: Prometheus
    type: prometheus
    url: http://Prom:9090
    access: proxy
    isDefault: true
```
Now since all we wanted is correctly configured, we can now create the docker file. The base image is the grafana image provided by grafana.
The second part is the copy of the grafana.ini in the grafana installation folder /etc/grafana.
The third part is configuration file "datasource.yml" where we have configured our Prometheus container configuration :
```Dockerfile
# syntax=docker/dockerfile:1

FROM grafana/grafana

# Copy modified grafana.ini in grafa directory
COPY grafana.ini /etc/grafana

COPY datasources.yml /etc/grafana/provisioning/datasources
```

Now go to the directory and build the new image :
```shell
docker build -t test-grafana:latest .
```

Then run the image on localhost with the ports dedicated for grafana "3000" : 
```shell
docker run --name new-test-grafana -d -p 127.0.0.1:3000:3000 test-grafana:latest
```

And to permit grafana to access prometheus url, connect grafana to the docker network "monitoring" :

```shell
docker network connect monitoring new-test-grafana
```

Now connect you with the provided credentials for the administrator and import the dashboard you want.
This part is specified in 03-Docker/00-Install-and-setup/Monitoring-with-Docker.md".