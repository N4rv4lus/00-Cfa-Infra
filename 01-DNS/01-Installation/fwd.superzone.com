; BIND data file for the local loopback interface
;
$TTL    604800
@       IN      SOA     lab-dns.superzone.com. admin.superzone.com. (
                              3         ; Serial
                         604800         ; Refresh
                          86400         ; Retry
                        2419200         ; Expire
                         604800 )       ; Negative Cache TTL
;

; NS records for name servers
@    IN      NS      lab-dns.superzone.com.

; A records for name servers
lab-dns          IN      A       192.168.100.2

; A records for domain names
prometheus          IN      A       192.168.100.6
grafana          IN      A       192.168.100.7
srv-ansible          IN      A       192.168.100.5
dev-gitlab           IN      A       192.168.100.8