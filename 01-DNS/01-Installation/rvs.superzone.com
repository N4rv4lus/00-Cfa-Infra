;
; BIND reverse data file for the local loopback interface
;
$TTL    604800
@       IN      SOA     lab-dns.superzone.com. admin.superzone.com. (
                              3         ; Serial
                         604800         ; Refresh
                          86400         ; Retry
                        2419200         ; Expire
                         604800 )       ; Negative Cache TTL
;

; name servers - NS records
      IN      NS      lab-dns.superzone.com.

; PTR Records
2   IN      PTR     lab-dns;
6   IN      PTR     prometheus;
7   IN      PTR     grafana;
5   IN      PTR     srv-ansible;
8   IN      PTR     dev-gitlab;