sudo hostnamectl set-hostname Cluster-KUB-Worker01
    3  sudo dnf upgrade -y
    4  sudo firewall-cmd --permanent --add-port={10250/tcp,30000-32767/tcp,9100/tcp,7946/tcp,7946/udp,7646/tcp,7646/udp,2379/tcp}
    5  sudo firewall-cmd --reload
    6  sudo firewall-cmd --list-all
    7  sudo reboot now
    8  ifconfig
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
   28  sudo dnf install dnf-utils -y
   29  sudo yum-config-manager     --add-repo     https://download.docker.com/linux/centos/docker-ce.repo
   30  sudo dnf repolist
   31  sudo dnf makecache
   32  sudo dnf install containerd.io -y
   33  su
   34  sudo nano /etc/containerd/config.toml
   35  sudo systemctl enable --now containerd
   36  sudo systemctl is-enabled containerd
   37  sudo systemctl status containerd
   38  cat <<EOF | sudo tee /etc/yum.repos.d/kubernetes.repo
   39  [kubernetes]
   40  name=Kubernetes
   41  baseurl=https://packages.cloud.google.com/yum/repos/kubernetes-el7-\$basearch
   42  enabled=1
   43  gpgcheck=1
   44  gpgkey=https://packages.cloud.google.com/yum/doc/yum-key.gpg https://packages.cloud.google.com/yum/doc/rpm-package-key.gpg
   45  exclude=kubelet kubeadm kubectl
   46  EOF
   47  sudo dnf repolist
   48  sudo dnf makecache
   49  sudo dnf install kubelet kubeadm kubectl --disableexcludes=kubernetes -y
   50  sudo systemctl enable --now kubelet
   51  su
   52  sudo curl -fsSLo /opt/bin/flanneld https://github.com/flannel-io/flannel/releases/download/v0.19.0/flanneld-amd64
   53  sudo chmod +x /opt/bin/flanneld
   54  lsmod | grep br_netfilter
   55  sudo shutdown now
   56  ls -als | grep bash