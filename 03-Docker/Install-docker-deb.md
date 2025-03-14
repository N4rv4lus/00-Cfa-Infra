# Docker Setup Debian 12.9 + Prometheus & Grafana

All of the following can be found on docker's installation guide 

1st delete docker & other's packages to avoid conflicts with the new one we'll be downloading
```shell
for pkg in docker.io docker-doc docker-compose podman-docker containerd runc; do sudo apt-get remove $pkg; done
```

## Install Docker
Add Docker's official GPG key
```shell
sudo apt-get update
sudo apt-get install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/debian/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc
```

Add the repository to Apt sources:
```shell
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/debian \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
```

Now Install docker-ce, cli, containerd.io, docker-buildx-plugin and docker-compose-plugin :
```shell
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

You can now check and run if docker is correctly installed, so run your first image "hello-world" :
```shell
sudo docker run hello-world
```

You can also check if docker systemd service is correctly working, it should be running and enabled to be executed at start of your server : 
```shell
sudo systemctl status docker
```

## Now manage, download, check and install application/services (easy way)

Search your favorite Images in the docker hub, here is an exemple with nginx :
```shell
sudo docker search nginx
```
You can either download by pulling it :
```shell
sudo docker pull nginx
```
Or you can also do it by running the image, and docker will pull the image after checking if the image is stored in your docker's image directory :
```shell
sudo docker run -it nginx bash
```
To check the images you have pulled run :
```shell
sudo docker image ls
```
this should be the output : 
```shell
REPOSITORY        TAG       IMAGE ID       CREATED       SIZE
nginx             latest    b52e0b094bc0   5 weeks ago   192MB
hello-world       latest    74cc54e27dc4   7 weeks ago   10.1kB
```

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