# Automatisation du renouvellement de certificat openbao pour container nginx reverse proxy
OpenBao Agent natif non privilégié → marqueur → systemd.path → script root contrôlé → SIGHUP Nginx

L'idée est de renouveller le certificat du service nginx car il est limité à 48h.

## Création du role App Role sur Openbao

Ce role a pour but d'identifier l'agent openbao et de déterminer ses permissions.

Le role tls-server-superzone (précédemment créé) dédiée à la PKI interne d'OpenBao a pour but de déterminer quel certificat pourront être généré.
Ici le certificat autorisé est une wildcard *.superzone.com

Sur le serveur openbao :
```shell 
bao auth enable approle
```
Maintenant il faut apliquer la politique suivante qui permettra au nouveau role "nginx-tls-agent" de : 
- emettre un certificat
- consulter, renouveler ou révoquer son propre token
- n'a pas de modification de la PKI, ni du ou des autres roles ou secret

bao policy write nginx-tls-agent - <<'EOF'
path "pki_services/issue/tls-server-superzone" {
  capabilities = ["update"]
}

path "auth/token/lookup-self" {
  capabilities = ["read"]
}

path "auth/token/renew-self" {
  capabilities = ["update"]
}

path "auth/token/revoke-self" {
  capabilities = ["update"]
}
EOF

Maintenant vérifiez la liste d'autorisation et la politique nginx-tls-agent