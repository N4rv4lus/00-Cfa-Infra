Here we will review how to setup an NFS Server with the system.
It is divided in 2 parts, one server where will be stored the data, and one client who will access the shared directory.

## NFS Server

First download for rocky linux nfs-kernel-server
```shell
sudo dnf install nfs-kernel-server
```
Enable the service to run the server at start
```shell
sudo systemctl enable nfs-server.service
```
Check nfs-server status
```shell
sudo systemctl status nfs-server.service
```
Now add the services nfs/nfs3/mountd/rpc-bind, reload the services and check them.
```shell
sudo firewall-cmd --add-service={nfs,nfs3,mountd,rpc-bind} --permanent
sudo firewall-cmd --reload
sudo firewall-cmd --list-services
```
Now edit the exports :
```shell
sudo nano /etc/exports
```
Here is the setup for the edits (other configurations are possible), rw = read write, sync (synchrone, async is possible and is recommended for huge transfers and many users)
```txt
/nfshare/docker-test 192.168.100.188/24(rw,sync)
/nfshare/docker-test 192.168.100.32/24(rw,sync)
```
Check mounts available
```shell
showmount -e 192.168.100.188
```
Here is the output, there is the shared folder, and the IP setted up to access it :
```shell
Export list for 192.168.100.188:
/nfshare/docker-test 192.168.100.32/24,192.168.100.188/24
```
Now add the user specified in /etc/exports, here is "docker-test"
```shell
sudo adduser docker-test
```
Now check that you have created the user :
```shell
sudo cat /etc/passwd | grep docker-test
```
Now modify the user uid and group ID 
```shell
sudo usermod -u 1002 docker-test
sudo groupmod -g 1002 docker-test
```
Now recheck that the user ID have been modified :
```shell
sudo cat /etc/passwd | grep 1002
```
Now set the shared directory ownership to docker-test user. 
```shell
sudo chown docker-test /nfshare/docker-test/
```

## NFS Client

```shell
sudo apt search nfs-utils
```

```shell
sudo apt install libnfs-utils
```

```shell
sudo mount -t nfs4 192.168.100.188:/nfshare/docker-test/ /nfsmount
```

```shell
mount -a
echo $?
```

```txt
fstab
192.168.100.188:/nfshare/docker-test/ /nfsmount nfs     rw      0       0
```