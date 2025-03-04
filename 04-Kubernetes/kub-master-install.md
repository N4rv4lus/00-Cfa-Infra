# Kubernetes installation with KUBEADM  (RockyLinux 9.3 - Onyx)

## Getting started

Here is a small procedure to install Kubernetes and setup a cluster

First as usual set hosntame
```shell
sudo hostnamectl set-hostname Cluster-KUB-Manager01
```
Then update your server
```shell
sudo dnf upgrade -y
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
```shell
sestatus
```
   13  sudo modprobe overlay

sudo modprobe br_netfilter


cat <<EOF | sudo tee /etc/modules-load.d/k8s.conf
overlay
br_netfilter
EOF

   19  cat <<EOF | sudo tee /etc/sysctl.d/k8s.conf
   20  net.bridge.bridge-nf-call-iptables  = 1
   21  net.bridge.bridge-nf-call-ip6tables = 1
   22  net.ipv4.ip_forward                 = 1
   23  EOF
   24  sudo sysctl --system

Comment swap configuration line in fstab (configuration file that loads the storage systems at boot)
```shell
sudo sed -i '/ swap / s/^\(.*\)$/#\1/g' /etc/fstab
```
For avoiding a reboot turn off swap directly (and reboot later)
```shell
sudo swapoff -a
```
   27  free -m
   28  sudo dnf install dnf-utils
   29  sudo dnf install dnf-utils -y
   30  sudo yum-config-manager     --add-repo     https://download.docker.com/linux/centos/docker-ce.repo
   31  sudo dnf repolist
   32  sudo dnf makecache
   33  sudo dnf install containerd.io
   34  sudo dnf install containerd.io -y
   35  sudo mv /etc/containerd/config.toml /etc/containerd/config.toml.orig
   36  sudo containerd config default > /etc/containerd/config.toml
   37  sudo mv /etc/containerd/config.toml /etc/containerd/config.toml.orig
   38  sudo containerd config default > /etc/containerd/config.toml
   39  su
   40  sudo nano /etc/containerd/config.toml
   41  sudo systemctl enable --now containerd
   42  sudo systemctl is-enabled containerd
   43  sudo systemctl status containerd
   44  cat <<EOF | sudo tee /etc/yum.repos.d/kubernetes.repo
   45  [kubernetes]
   46  name=Kubernetes
   47  baseurl=https://packages.cloud.google.com/yum/repos/kubernetes-el7-\$basearch
   48  enabled=1
   49  gpgcheck=1
   50  gpgkey=https://packages.cloud.google.com/yum/doc/yum-key.gpg https://packages.cloud.google.com/yum/doc/rpm-package-key.gpg
   51  exclude=kubelet kubeadm kubectl
   52  EOF
   53  sudo dnf repolist
   54  sudo dnf makecache
   55  sudo dnf install kubelet kubeadm kubectl --disableexcludes=kubernetes
   56  sudo dnf install kubelet kubeadm kubectl --disableexcludes=kubernetes -y
   57  sudo systemctl enable --now kubelet
   58  mkdir -p /opt/bin/
   59  su
   60  sudo curl -fsSLo /opt/bin/flanneld https://github.com/flannel-io/flannel/releases/download/v0.19.0/flanneld-amd64
   61  sudo chmod +x /opt/bin/flanneld
   62  lsmod | grep br_netfilter
   63  sudo kubeadm config images pull
   64  sudo kubeadm init --pod-network-cidr=10.244.0.0/16 --apiserver-advertise-address=Cluster-KUB-Manager01 --cri-socket=unix:///run/containerd/containerd.sock