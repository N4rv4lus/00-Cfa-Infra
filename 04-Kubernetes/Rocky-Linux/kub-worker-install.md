# Kubernetes installation with KUBEADM  (RockyLinux 9.3 - Onyx)

## Getting started

Here is a small procedure to setup a kubernetes worker (most of the parts are the same for the master)

First as usual set hosntame
```shell
sudo hostnamectl set-hostname Cluster-KUB-Manager01
```
Then update your server
```shell
sudo dnf upgrade -y
sudo dnf install dnf-utils -y
```

## Now prepare the install before

### Setup Network rules

Open ports & network protocols
```shell
sudo firewall-cmd --permanent --add-port={6443/tcp,2379/tcp,2380/tcp,10250/tcp,10259/tcp,10257/tcp,10248/tcp,9100/tcp,7946/udp,7946/tcp,7646/udp,7646/tcp,2379/tcp}
```
Reload firewalld configuration to apply
```shell
sudo firewall-cmd --reload
```
Check the configuration
```shell
sudo firewall-cmd --list-all
```
Reboot your server just in case to be sure the parameter are loaded during boot
```shell
sudo reboot now
```

### Set Rocky security protocols

Set linux to permissiv mode 
(it is not supported on redhat distribution, it will be tested quickly on this repo to have the highest security settiings, if it's not functionnal, there will be installed on another OS)

Modify permenantly the SELINUX to permissive mode (not applied until reboot)
```shell
sudo sed -i 's/^SELINUX=enforcing$/SELINUX=permissive/' /etc/selinux/config
```
Check selinux configuration
```shell
sestatus
```
Now set selinux to permissiv but temporarly
```shell
sudo setenforce 0
```
Check selinux configuration
```shell
sestatus
```
Add module to the kernel linux, here is a specific File System for docker
```shell
sudo modprobe overlay
```
Now add br_netfilter for kubernetes & docker to have access to iptables (all know ip from the server) & nftables (network firewall tables - same as ip but the server internal firewall)
```shell
sudo modprobe br_netfilter
```

Now push overlay & br_netfilter to the k8s modules configuration files in module loads to be loaded at boot
```shell
cat <<EOF | sudo tee /etc/modules-load.d/k8s.conf
overlay
br_netfilter
EOF
```
Now add the iptables & nftables for ipv4, ipv6 and forward, to permit docker & kubernetes to have access to it
```shell
cat <<EOF | sudo tee /etc/sysctl.d/k8s.conf
net.bridge.bridge-nf-call-iptables  = 1
net.bridge.bridge-nf-call-ip6tables = 1
net.ipv4.ip_forward                 = 1
EOF
```
Now check systctl conf
```shell
sudo sysctl --system
```

### Now disable swap because this version of k8s do not suppord isolated swap for containers and it could become a leak for containers because they will be using the same volume

Comment swap configuration line in fstab (configuration file that loads the storage systems at boot)
```shell
sudo sed -i '/ swap / s/^\(.*\)$/#\1/g' /etc/fstab
```
For avoiding a reboot turn off swap directly (and reboot later)
```shell
sudo swapoff -a
```
Now check if you have enough RAM, technically it should be configured to have at least 4 go
```shell
free -m
```

## Now install containerd

add docker repository
```shell
sudo yum-config-manager     --add-repo     https://download.docker.com/linux/centos/docker-ce.repo
```
Check your repository lists
```shell
sudo dnf repolist
```
Now run makecache for dnf to store directly metadata in cache (directory /var/cache/dnf/)
```shell
sudo dnf makecache
```
Now Install containered
```shell
sudo dnf install containerd.io -y
```


Now create a copy of containerd configuration
```shell
sudo mv /etc/containerd/config.toml /etc/containerd/config.toml.orig
```
Now set new containerd config default file
```shell
sudo containerd config default > /etc/containerd/config.toml
```
set up systemd for containerd - CRI-O for the container to have fair ressource allocation from the host
```shell
sudo nano /etc/containerd/config.toml
```
Now enable containerd
   41  sudo systemctl enable --now containerd

Now Check containerd and check status
```shell
sudo systemctl is-enabled containerd
sudo systemctl status containerd
```


## Now install Kubernetes
1st setup kubernetes repository in yum.repos
```shell
cat <<EOF | sudo tee /etc/yum.repos.d/kubernetes.repo
[kubernetes]
name=Kubernetes
baseurl=https://packages.cloud.google.com/yum/repos/kubernetes-el7-\$basearch
enabled=1
gpgcheck=1
gpgkey=https://packages.cloud.google.com/yum/doc/yum-key.gpg https://packages.cloud.google.com/yum/doc/rpm-package-key.gpg
exclude=kubelet kubeadm kubectl
EOF
```
Now check the repolist and load metadata to be more efficient for the download
```shell
sudo dnf repolist
sudo dnf makecache
```
Now install kubernetes (kubelet, kubeadm & kubectl)
```shell
sudo dnf install kubelet kubeadm kubectl --disableexcludes=kubernetes -y
```

Enable Kubelet service
```shell
sudo systemctl enable --now kubelet
```
## Install Kubernetes flannel network service to allow a virtual network
Create a directory to store flannel network service binaries
```shell
mkdir -p /opt/bin/
```

```shell
sudo curl -fsSLo /opt/bin/flanneld https://github.com/flannel-io/flannel/releases/download/v0.19.0/flanneld-amd64
```

Make flanneld executable
```shell
sudo chmod +x /opt/bin/flanneld
```

And now join the cluster with the output of the master setup :
```shell
kubeadm join 192.168.100.116:6443 --token ld9rui.p75uchc8omn29zq0 \
        --discovery-token-ca-cert-hash sha256:b953a71368d7521a7dbb6e46624e8c24af40651bdcceff18119fc71212ddd695
```
