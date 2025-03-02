# Kubernetes installation with KUBEADM  (RockyLinux 9.3 - Onyx)

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
Now push these data in K8 configuration file : 
```shell
cat <<EOF | sudo tee /etc/modules-load.d/k8s.conf
   22  overlay
   23  br_netfilter
   24  EOF
```

reload you kernel files to confirm k8 modules
```shell
sudo sysctl --system
```

check system modules : 
```shell
lsmod | grep br_netfilter
lsmod | grep overlay
```

chek and modify
```shell
sysctl net.bridge.bridge-nf-call-iptables net.bridge.bridge-nf-call-ip6tables net.ipv4.ip_forward
```

```shell
sudo cat /sys/class/dmi/id/product_uuid
```

## SeLinux to permissiv mode (Rhel distrib)
set linux to permissiv mode 
(it is not supported on redhat distribution, it will be tested quickly on this repo to have the highest security settiings, if it's not functionnal, there will be installed on another OS)
```shell
sudo setenforce 0
```
add it to the 
```shell
sudo sed -i 's/^SELINUX=enforcing$/SELINUX=permissive/' /etc/selinux/config
```

## Download Kubernetes app
Add K8's repo for yum in yum repos config files
```shell
cat <<EOF | sudo tee /etc/yum.repos.d/kubernetes.repo
[kubernetes]
name=Kubernetes
baseurl=https://pkgs.k8s.io/core:/stable:/v1.29/rpm/
enabled=1
gpgcheck=1
gpgkey=https://pkgs.k8s.io/core:/stable:/v1.29/rpm/repodata/repomd.xml.key
exclude=kubelet kubeadm kubectl cri-tools kubernetes-cni
```

download kubelet / kubeadm / kubectl
```shell
sudo yum install -y kubelet kubeadm kubectl --disableexcludes=kubernetes
```

now enable services
```shell
sudo systemctl enable --now kubelet
```
```shell
sudo systemctl status kubelet.service
```

now you can insert those lines in kubernetes

```yaml
kind: ClusterConfiguration
apiVersion: kubeadm.k8s.io/v1beta3
kubernetesVersion: v1.28.0
---
kind: KubeletConfiguration
apiVersion: kubelet.config.k8s.io
cgroupDriver: systemd
```
## Now launch k8 setup with kubeadm

install kubeadm
```shell
sudo kubeadm init
```

to check the configuration
```shell
kubectl config view
```

now check the configuration 
```shell
sudo kubeadm certs check-expiration
```

configurer cgroupdrivers

control plane
firewall-cmd --permanent --add-port={6443/tcp,2379/tcp,2380/tcp,10250/tcp,10259/tcp,10257/tcp,10248/tcp,9100/tcp,7946/udp,7946/tcp,7646/udp,7646/tcp,2379/tcp}