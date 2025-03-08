sudo hostnamectl set-hostname Cluster-KUB-Worker01
sudo dnf upgrade -y
sudo firewall-cmd --permanent --add-port={10250/tcp,30000-32767/tcp,9100/tcp,7946/tcp,7946/udp,7646/tcp,7646/udp,2379/tcp}
sudo firewall-cmd --reload
sudo firewall-cmd --list-all
sudo reboot now
ifconfig
sudo sed -i 's/^SELINUX=enforcing$/SELINUX=permissive/' /etc/selinux/config
sestatus
sudo setenforce 0
sestatus
sudo modprobe overlay
sudo modprobe br_netfilter
cat <<EOF | sudo tee /etc/modules-load.d/k8s.conf
overlay
br_netfilter
EOF
cat <<EOF | sudo tee /etc/sysctl.d/k8s.conf
net.bridge.bridge-nf-call-iptables  = 1
net.bridge.bridge-nf-call-ip6tables = 1
net.ipv4.ip_forward                 = 1
EOF
sudo sysctl --system
sudo sed -i '/ swap / s/^\(.*\)$/#\1/g' /etc/fstab
sudo swapoff -a
free -m
sudo dnf install dnf-utils -y
sudo yum-config-manager     --add-repo     https://download.docker.com/linux/centos/docker-ce.repo
sudo dnf repolist
sudo dnf makecache
sudo dnf install containerd.io -y
sudo nano /etc/containerd/config.toml
sudo systemctl enable --now containerd
sudo systemctl is-enabled containerd
sudo systemctl status containerd
cat <<EOF | sudo tee /etc/yum.repos.d/kubernetes.repo
[kubernetes]
name=Kubernetes
baseurl=https://packages.cloud.google.com/yum/repos/kubernetes-el7-\$basearch
enabled=1
gpgcheck=1
gpgkey=https://packages.cloud.google.com/yum/doc/yum-key.gpg https://packages.cloud.google.com/yum/doc/rpm-package-key.gpg
exclude=kubelet kubeadm kubectl
EOF
sudo dnf repolist
sudo dnf makecache
sudo dnf install kubelet kubeadm kubectl --disableexcludes=kubernetes -y
sudo systemctl enable --now kubelet
sudo curl -fsSLo /opt/bin/flanneld https://github.com/flannel-io/flannel/releases/download/v0.19.0/flanneld-amd64
sudo chmod +x /opt/bin/flanneld
lsmod | grep br_netfilter
sudo shutdown now
