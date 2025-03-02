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

set linux to permissiv mode
```shell
sudo setenforce 0
```

```shell
sudo sed -i 's/^SELINUX=enforcing$/SELINUX=permissive/' /etc/selinux/config
```
   44  cat <<EOF | sudo tee /etc/yum.repos.d/kubernetes.repo
   45  [kubernetes]
   46  name=Kubernetes
   47  baseurl=https://pkgs.k8s.io/core:/stable:/v1.29/rpm/
   48  enabled=1
   49  gpgcheck=1
   50  gpgkey=https://pkgs.k8s.io/core:/stable:/v1.29/rpm/repodata/repomd.xml.key
   51  exclude=kubelet kubeadm kubectl cri-tools kubernetes-cni

sudo yum install -y kubelet kubeadm kubectl --disableexcludes=kubernetes
   54  sudo systemctl enable --now kubelet
   55  sudo systemctl status kubelet.service
   56  sudo nano kubeadm-config.yaml

# kubeadm-config.yaml
kind: ClusterConfiguration
apiVersion: kubeadm.k8s.io/v1beta3
kubernetesVersion: v1.28.0
---
kind: KubeletConfiguration
apiVersion: kubelet.config.k8s.io
cgroupDriver: systemd

ip route show
sudo kubeadm init

kubectl config view
sudo kubeadm certs check-expiration

configurer cgroupdrivers

control plane
firewall-cmd --permanent --add-port={6443/tcp,2379/tcp,2380/tcp,10250/tcp,10259/tcp,10257/tcp,10248/tcp,9100/tcp,7946/udp,7946/tcp,7646/udp,7646/tcp,2379/tcp}