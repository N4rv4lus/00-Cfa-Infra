## Block / open flows for rocky internal firewall



All of the commands can be found with the cli :
```shell
man firewalld
```

Here is a small cli to enable a specific flow like https - 443 on the firewall-cmd  (not permanent, will be reset when the server will be restarted)
```shell
sudo firewall-cmd --zone=public --add-port=443/tcp # exemple ouverture port 443 - HTTPS
```
Here you make the last command permanent
```shell
sudo firewall-cmd --runtime-to-permanent # appliquez la configuration
```
Now check firewalld services
```shell
sudo firewall-cmd --list-services # Lister tous les services
```
You can also reload firewall-cmd services
```shell
sudo firewall-cmd --reload
```
If you have an issue, or you have found an anomaly on logs or on your monitoring activate panic mode
```shell
sudo firewall-cmd --panic-on
```
To disable panic mode, disable it with 
```shell
sudo firewall-cmd --panic-off
```
Check if panic mode is enabled
```shell
sudo firewall-cmd --query-panic
```