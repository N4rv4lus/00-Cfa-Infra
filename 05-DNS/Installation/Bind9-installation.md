Here you will find how to install Bind9 (DNS Server) and setup the configuration files to setup a forward zone and a reverse zone. (this is a base implementation to perform labs, do not use in production)

## Installation
1st download bind9 packages and bind-utils files
```shell
sudo dnf install bind bind-utils -y
```

## Bind9 service systemd setup
2nd part start systemctl named service, this will permit to run the service named (bind9 dns) with the systemd that permit to run the service when the server will start, this will reduce use of the shell commands and allow to use systemd informations like status of the service, and permit you to journalize the errors where some logs will be stored.

start the service named and then enable it
```shell
sudo systemctl start named
```
enable named service will permit that systemd run named at the start of the server or after a reboot
```shell
sudo systemctl enable named
```
Now check if the service is enabled
```shell
sudo systemctl is-enabled named
```
Now check the status of the service (it will show a small dashboard with the service major configurations files)
```shell
sudo systemctl status named
```
You can also check the logs with a timestamp of the service with journalctl
```shell
sudo journalctl -xeu named
```

## Allow queries with firewall-cmd
Now setup the os firewall to open the necessary ports (port 53) to permit other servers, clients to make queries on the dns server with UDP and/or TCP protocol if the request is bigger than 512 octets.
```shell
sudo firewall-cmd --add-service=dns --permanent
```
Now reload firewall-cmd to apply the configuration 
```shell
sudo firewall-cmd --reload
```

## Now configure the named configuration files
Here is the way to setup named configuration files, you can find this naemd.conf file in the repo
```shell
sudo nano /etc/named.conf
```

Now check if "named.conf", your file is correctly configured
```shell
sudo named-checkconf /etc/named.conf
```
Now to apply the configuration restart the service
```shell
sudo systemctl restart named
```

## Now create you Forward zone and reverse zone

Dns forward zone is the DNS zone where you will be associating DNS name with IP and allow clients to define what is the IP of a hostname
Now configure the forward zone
```shell
sudo nano /var/named/fwd.testzone.com
```
DNS reversed zone is the DNS zone where you will be associating IP with DNS names to allow clients to define what is the hosname of a specific IP and check if the IP is referenced in the DNS with a hostname
Now configure the reverse zone
```shell
sudo nano /var/named/rvs.testzone.com
```
Now this will change the ownership of the dns forward and reverse zone to the named account (and all the subdirectories, here a none, only forward and reverse zone)
```shell
sudo chown -R named: /var/named/{fwd.testzone.com,rvs.testzone.com}
```

Now check the syntax of the forward zone
```shell
sudo named-checkzone testzone.com /var/named/fwd.testzone.com
```

Now check the syntax of the forward zone
```shell
sudo named-checkzone testzone.com /var/named/rvs.testzone.com
```
If everything is correct you can now apply the new configuration by restarting the service
```shell
sudo systemctl restart named
```
And finalize it by checking the status
```shell
sudo systemctl restart named
```
