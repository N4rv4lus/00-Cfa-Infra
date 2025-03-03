sudo hostnamectl set-hostname Cluster-KUB-Manager01
    3  sudo dnf upgrade -y
    4  sudo firewall-cmd --permanent --add-port={6443/tcp,2379/tcp,2380/tcp,10250/tcp,10259/tcp,10257/tcp,10248/tcp,9100/tcp,7946/ucp,7946/tcp,7646/ucp,7646/ucp,2379/tcp}
    5  sudo firewall-cmd --permanent --add-port={6443/tcp,2379/tcp,2380/tcp,10250/tcp,10259/tcp,10257/tcp,10248/tcp,9100/tcp,7946/udp,7946/tcp,7646/udp,7646/tcp,2379/tcp}
    6  sudo firewall-cmd --reload
    7  sudo firewall-cmd --list-all
    8  sudo reboot now
    9  sudo sed -i 's/^SELINUX=enforcing$/SELINUX=permissive/' /etc/selinux/config
   10  sestatus
   11  sudo setenforce 0
   12  sestatus
   13  sudo modprobe overlay
   14  sudo modprobe br_netfilter
   15  cat <<EOF | sudo tee /etc/modules-load.d/k8s.conf
   16  overlay
   17  br_netfilter
   18  EOF
   19  cat <<EOF | sudo tee /etc/sysctl.d/k8s.conf
   20  net.bridge.bridge-nf-call-iptables  = 1
   21  net.bridge.bridge-nf-call-ip6tables = 1
   22  net.ipv4.ip_forward                 = 1
   23  EOF
   24  sudo sysctl --system
   25  sudo sed -i '/ swap / s/^\(.*\)$/#\1/g' /etc/fstab
   26  sudo swapoff -a
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