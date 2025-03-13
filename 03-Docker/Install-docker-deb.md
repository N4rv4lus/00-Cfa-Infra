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

Search your favorite Images in the docker hub 
```shell
sudo docker search nginx
```
You can either download by pulling it :
```shell
sudo docker pull nginx
```
Or you can run :
```shell
sudo docker pull nginx
```




```shell
sudo docker run --name prometheus -d -p 127.0.0.1:9090:9090 prom/prometheus
```

