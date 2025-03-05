## Block / open flows for rocky internal firewall

sudo firewall-cmd --zone=public --add-port=443/tcp # exemple ouverture port 443 - HTTPS
sudo firewall-cmd --runtime-to-permanent # appliquez la configuration 
sudo firewall-cmd --list-services # Lister tous les services