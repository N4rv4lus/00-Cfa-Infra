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

Now for the setup of Grafana 