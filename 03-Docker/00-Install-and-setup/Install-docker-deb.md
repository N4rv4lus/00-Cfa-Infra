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

