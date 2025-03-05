## Block / open flows for rocky internal firewall

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