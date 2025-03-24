Server side

sudo dnf install nfs-kernel-server

sudo systemctl enable nfs-server.service

sudo systemctl status nfs-server.service

sudo firewall-cmd --add-service={nfs,nfs3,mountd,rpc-bind} --permanent
sudo firewall-cmd --reload
sudo firewall-cmd --list-services

sudo nano /etc/exports

/nfshare/docker-test 192.168.100.188/24(rw,sync)
/nfshare/docker-test 192.168.100.32/24(rw,sync)

showmount -e 192.168.100.188


sudo adduser docker-test
sudo cat /etc/passwd
usermod -u 1002 docker-test
sudo usermod -u 1002 docker-test
sudo groupmod -g 1002 docker-test

sudo chown docker-test /nfshare/docker-test/

Client side

sudo apt search nfs-utils
sudo apt install libnfs-utils
sudo mount -t nfs4 192.168.100.188:/nfshare/docker-test/ /nfsmount

mount -a
echo $?

fstab
192.168.100.188:/nfshare/docker-test/ /nfsmount nfs     rw      0       0