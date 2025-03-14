## Install and Configure Prometheus and Grafana with docker

1st check prometheus images on docker hub
```shell
sudo docker search prometheus
```
Then run the prometheus image (select the one you prefer, here we downloaded the one who as the most Stars)
```shell
sudo docker run --name prometheus -d -p 127.0.0.1:9090:9090 prom/prometheus
```
You can now access Prometheus on your server with localhost with the port 9090.
So type in your browser "localhost:9090" or "127.0.0.1:9090" and you should see Prometheus Url and dashboard. 
For now prometheus only monitors himself, we will add node exporters to monitor other servers.

2nd check grafana images on docker hub
```shell 
sudo docker search grafana
```
Now run grafana image on prometheus
```shell
sudo docker run -d --name=grafana -p 3000:3000 grafana/grafana
```
So type in your browser "localhost:3000" or "127.0.0.1:3000" and you should see Grafana Url and dashboard.
The credentials for the first setup are : 
account : admin
password : admin

You will be ask to modify the password, select a new one.
And you can also create one.

Now to connect grafana to prometheus and enable the dashboard you need to setup the datasource.
So Prometheus is the data source, but you cannot add it by using localhost:9090, so you will need to now the prometheus docker internal IP.

To check prometheus internal IP run the cli : 
```shell
sudo docker inspect prometheus
```
It will display a file, and you must be looking to the "Network Settings Part" to find the IP.
Then put the IP with the port in the dashboard and you will have finished the setup of the datasource.

Now to check the prometheus dashboard, go in the datasource and there are 2 tabs, "Setting" and "Dashboard" download "Prometheus 2.0 Stats" and you will have your first dashboard.

You can also check that your containers are correctly running by running : 
```shell
sudo docker ps
```
It will display something like this, with the image, the container ID's, and more informations :
```sql
CONTAINER ID   IMAGE             COMMAND                  CREATED        STATUS        PORTS                                         NAMES
ced952fcb712   grafana/grafana   "/run.sh"                19 hours ago   Up 19 hours   0.0.0.0:3000->3000/tcp, [::]:3000->3000/tcp   grafana
95b46aa4a9c9   prom/prometheus   "/bin/prometheus --c…"   19 hours ago   Up 19 hours   127.0.0.1:9090->9090/tcp                      prometheus
```

## Node Exporter
Now we will install and run node-exporter to monitor the host where are running prometheus and grafana because prometheus only monitors himself.

As always, search node-exporter image in the docker hub :

```shell
sudo docker search node-exporter
```

Now go to the docker hub and run : 
```shell
docker run -d \
  --net="host" \
  --pid="host" \
  -v "/:/host:ro,rslave" \
  quay.io/prometheus/node-exporter:latest \
  --path.rootfs=/host
```

