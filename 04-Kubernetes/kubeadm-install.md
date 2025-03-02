# Kubernetes installation with KUBEADM



## Getting started

Here is a small procedure to install Kubernetes and setup a cluster

## Install docker on your server

Install docker :
Clean your server and add the docker repo
```shell
sudo yum remove docker docker-client docker-client-latest docker-common docker-latest docker-latest-logrotate docker-logrotate docker-engine podman runc
sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
```

Now downdload docker :
```shell
sudo yum install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin -y
```

Enable containerd
```shell
sudo systemctl enable --now docker containerd
sudo systemctl status --now docker containerd
```

Now disable CRI by commenting the line in the config file "config.toml"
```shell
sudo nano /etc/containerd/config.toml
```
And then restart containerd
```shell
sudo systemctl restart containerd
```

