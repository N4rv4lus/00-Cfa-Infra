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
```shell
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
```
Maintenant vérifiez la liste d'autorisation et la politique nginx-tls-agent
```shell
bao auth list -detailed
bao policy read nginx-tls-agent
```

Maintenant configurer l'appRole : 
```shell
bao write auth/approle/role/nginx-tls-agent \
  bind_secret_id=true \
  secret_id_bound_cidrs="192.168.100.100/32" \
  secret_id_ttl=0 \
  secret_id_num_uses=0 \
  token_bound_cidrs="192.168.100.100/32" \
  token_policies="nginx-tls-agent" \
  token_no_default_policy=true \
  token_type="service" \
  token_period="1h" \
  token_explicit_max_ttl=0 \
  token_num_uses=0
```
  Validez la configuration via ce check : 
```shell
bao read auth/approle/role/nginx-tls-agent
```
output: 
```shell
Key                        Value
---                        -----
bind_secret_id             true
local_secret_ids           false
secret_id_bound_cidrs      [192.168.100.100/32]
secret_id_num_uses         0
secret_id_ttl              0s
token_bound_cidrs          [192.168.100.100]
token_explicit_max_ttl     0s
token_max_ttl              0s
token_no_default_policy    true
token_num_uses             0
token_period               1h
token_policies             [nginx-tls-agent]
token_strictly_bind_ip     false
token_ttl                  0s
token_type                 service
```
Maintenant sur le serveur Docker : 

Executez ces commandes pour préciser la version et le fichier de destination : 
```shell
$ OPENBAO_VERSION="2.6.2"
OPENBAO_ARCHIVE="openbao_${OPENBAO_VERSION}_linux_amd64.tar.gz"
OPENBAO_TMP="$(mktemp -d)"
```
ensuite téléchargez la bonne version :
```shell
curl -fLO \
  "https://github.com/openbao/openbao/releases/download/v${OPENBAO_VERSION}/${OPENBAO_ARCHIVE}"
```
Puis le checksum permettant de valider que le fichier est bien le bon : 
```shell
curl -fLO \
  "https://github.com/openbao/openbao/releases/download/v${OPENBAO_VERSION}/${OPENBAO_ARCHIVE}"
```
ensuite comparez les fichiers : 
```shell
sha256sum --ignore-missing --check checksums.txt
openbao_2.6.2_linux_amd64.tar.gz: OK
```
Il faut maintenant extraire l'archive, puis installer openbao et valider la version : 
extraire openbao : 
```shell
tar -xzf "$OPENBAO_ARCHIVE"
```
Installez le dans le répertoire et configurez les droits du répertoire : 
```shell
sudo install \
  -o root \
  -g root \
  -m 0755 \
  "$OPENBAO_TMP/bao" \
  /usr/local/bin/bao
```
Ensuite validez la vesrion : 
```shell
/usr/local/bin/bao version
OpenBao v2.6.2 (dd9c19c37a878cf4a81b18efb8d6f0599c7da923), committed 2026-08-18T15:48:19Z
```
## Création du compte

Créez l'utilisateur openbao-agent : 
```shell
sudo useradd \
  --system \
  --user-group \
  --home-dir /var/lib/openbao-agent \
  --create-home \
  --shell /usr/sbin/nologin \
  openbao-agent
```
Puis configurez les repertoires pour l'agent dédiés au RoleID et au SecretID :
```shell
sudo install -d \
  -o root \
  -g openbao-agent \
  -m 0750 \
  /etc/openbao-agent \
  /etc/openbao-agent/auth \
  /etc/openbao-agent/templates
```
Maintenant configurez le repertoire de travail de l'agent pour écrire le nouveau certificat et la nouvelle clé, puis le répetoire trigger pour systemd lui permetant de signaler dès qu'un nouveau certificat sera disponible : 
```shell
sudo install -d \
  -o openbao-agent \
  -g openbao-agent \
  -m 0700 \
  /var/lib/openbao-agent \
  /var/lib/openbao-agent/rendered \
  /var/lib/openbao-agent/trigger
```
Maintenant validez que le compte et les répertoires on bien été créés : 
```shell
getent passwd openbao-agent
id openbao-agent
```
```shell
ls -als /etc/openbao-agent/ /var/lib/openbao-agent/
```
Maintenant sur le serveur OpenBao nous allons récupérer le RoleID (automatiquement généré), puis le stocker sur le serveur Docker.
```shell
ROLE_ID_FILE="/tmp/nginx-tls-agent.role-id"
```
install -m 0600 /dev/null "$ROLE_ID_FILE"
```shell
bao read \
  -field=role_id \
  auth/approle/role/nginx-tls-agent/role-id \
  > "$ROLE_ID_FILE"
```
Maintenant copiez le Role ID sur le serveur docker.
```shell
scp "$ROLE_ID_FILE" administrator@192.168.100.100:/tmp/nginx-tls-agent.role-id
```
Maintenant sur le serveur docker : 

Copiez le role et affectez les droits au groupe openbao. Ici root pourra modifier et lire, et openbao-agent pourra uniquement lire : 
```shell
sudo install \
  -o root \
  -g openbao-agent \
  -m 0640 \
  /tmp/nginx-tls-agent.role-id \
  /etc/openbao-agent/auth/role-id
```
Validez maintenant les permissions : 
```shell
sudo stat -c '%A %U:%G %n' \
  /etc/openbao-agent/auth/role-id
```
Maintenant sur le serveur Docker il va falloir préparer le fichier secret-id que nous allons récupérer sur le serveur OpenBao : 

Sur le serveur Docker créez le répertoire et le fichier 
```shell
sudo install \
  -o root \
  -g openbao-agent \
  -m 0640 \
  /dev/null \
  /etc/openbao-agent/auth/secret-id
```
Sur Openbao générez un fichier temporaire dans lequel vous allez stocker le token permettant au compte openbao-agent de génrérer un token qui lui permettra de récupérer le secret-ID :
```shell
WRAP_FILE="$(mktemp /tmp/nginx-tls-agent.secret-id.wrap.XXXXXX)"
```
```shell
chmod 0600 "$WRAP_FILE"
```
Maintenant écrivez 
```shell
bao write \
  -wrap-ttl=15m \
  -field=wrapping_token \
  -f auth/approle/role/nginx-tls-agent/secret-id \
  > "$WRAP_FILE"
```
Verifiez le fichier :
```shell
test -s "$WRAP_FILE" && echo "Jeton d'encapsulation généré"
```
  Puis transférez le sur le serveur docker :
```shell
scp "$WRAP_FILE" administrator@192.168.100.100:nginx-tls-agent.secret-id.wrap
```

Appliquez les droits uniquement à root et appliquez les droits de modifications du fichier : 
```shell
sudo chown root:root \
  /home/administrator/nginx-tls-agent.secret-id.wrap

sudo chmod 0600 \
  /home/administrator/nginx-tls-agent.secret-id.wrap
```
Ensuite avec ce token, récupérez le véritable sercret ID.
```shell
sudo /bin/sh -c '
  export BAO_ADDR="https://openbao.superzone.com:8200"
  export BAO_CACERT="/usr/local/share/ca-certificates/superzone-root-ca.crt"
  export BAO_TOKEN="$(cat /home/administrator/nginx-tls-agent.secret-id.wrap)"
```
```shell
  /usr/local/bin/bao unwrap \
    -field=secret_id \
    > /etc/openbao-agent/auth/secret-id
'
```
Supprimez maintenant le fichier sur le serveur docker : 
```shell
sudo rm -- \
  /home/administrator/nginx-tls-agent.secret-id.wrap
```
Puis sur le serveur openBao :
```shell
rm -- "$WRAP_FILE"
```
et vérifierz le fichier sans afficher le secret : 
```shell
sudo stat -c '%A %U:%G %s-octets %n' \
  /etc/openbao-agent/auth/secret-id
```
```shell
sudo -u openbao-agent test \
  -s /etc/openbao-agent/auth/secret-id \
  && echo "SecretID présent"
```
```shell
sudo -u openbao-agent test \
  ! -w /etc/openbao-agent/auth/secret-id \
  && echo "SecretID non modifiable par l'Agent"

Maintenant vous pouvez créer la configuration sur le serveur docker
```shell
sudo tee /etc/openbao-agent/agent.hcl >/dev/null <<'EOF'
exit_after_auth = true
log_level       = "info"

vault {
  address = "https://openbao.superzone.com:8200"
  ca_cert = "/usr/local/share/ca-certificates/superzone-root-ca.crt"

  retry {
    num_retries = 5
  }
}

auto_auth {
  method "approle" {
    mount_path  = "auth/approle"
    min_backoff = "1s"
    max_backoff = "1m"
    exit_on_err = true

    config = {
      role_id_file_path                   = "/etc/openbao-agent/auth/role-id"
      secret_id_file_path                 = "/etc/openbao-agent/auth/secret-id"
      remove_secret_id_file_after_reading = false
    }
  }
}
EOF
```
Puis appliquez les permissions sur ce fichier :
```shell
sudo chown root:openbao-agent \
  /etc/openbao-agent/agent.hcl

sudo chmod 0640 \
  /etc/openbao-agent/agent.hcl
```
Validez maintenant que tout est lisible :
```shell
sudo -u openbao-agent test \
  -r /etc/openbao-agent/agent.hcl \
  && echo "Configuration lisible"

sudo -u openbao-agent test \
  -r /etc/openbao-agent/auth/role-id \
  && echo "RoleID lisible"

sudo -u openbao-agent test \
  -r /etc/openbao-agent/auth/secret-id \
  && echo "SecretID lisible"

sudo -u openbao-agent test \
  -r /usr/local/share/ca-certificates/superzone-root-ca.crt \
  && echo "CA lisible"
```
Une fois ce test effectué, nous allons mettre à jour la policy pour autoriser l'agent à update le certificat, à lire la ca_chain, à renouveller le token automatiquement puis à revoquer aussi le token.
```shell
bao policy write nginx-tls-agent - <<'EOF'
path "pki_services/issue/tls-server-superzone" {
  capabilities = ["update"]
}

path "pki_services/cert/ca_chain" {
  capabilities = ["read"]
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
```
Maintenant il faut créer le template PKI sur le serveur docker.
Cela permet de créer un bundle comprenant le certificat wildcard, sa clé privée, la chaine des CA.
```shell
sudo tee \
  /etc/openbao-agent/templates/nginx-wildcard.pem.ctmpl \
  >/dev/null <<'EOF'
{{ with pkiCert "pki_services/issue/tls-server-superzone" "common_name=*.superzone.com" "ttl=48h" }}
{{ .Data.Cert }}
{{ .Data.Key }}
{{ end }}
{{ with secret "pki_services/cert/ca_chain" }}
{{ .Data.certificate }}
{{ end }}
EOF
```
Et maintenant il faut affecter les droits sur ce fichier et l'affecter à un groupe / user :
```shell
sudo chown root:openbao-agent \
  /etc/openbao-agent/templates/nginx-wildcard.pem.ctmpl

sudo chmod 0640 \
  /etc/openbao-agent/templates/nginx-wildcard.pem.ctmpl
```
Remplacer la configuration de test de l'agent openbao sur le serveur docker : 
```shell
sudo tee /etc/openbao-agent/agent.hcl >/dev/null <<'EOF'
exit_after_auth = false
log_level       = "info"

vault {
  address = "https://openbao.superzone.com:8200"
  ca_cert = "/usr/local/share/ca-certificates/superzone-root-ca.crt"

  retry {
    num_retries = 5
  }
}

auto_auth {
  method "approle" {
    mount_path  = "auth/approle"
    min_backoff = "1s"
    max_backoff = "1m"
    exit_on_err = false

    config = {
      role_id_file_path                   = "/etc/openbao-agent/auth/role-id"
      secret_id_file_path                 = "/etc/openbao-agent/auth/secret-id"
      remove_secret_id_file_after_reading = false
    }
  }
}

template_config {
  exit_on_retry_failure         = false
  static_secret_render_interval = "1h"
}

template {
  source          = "/etc/openbao-agent/templates/nginx-wildcard.pem.ctmpl"
  destination     = "/var/lib/openbao-agent/rendered/nginx-wildcard-bundle.pem"
  create_dest_dirs = false
  perms           = "0600"
  backup          = true
  error_on_missing_key = true

  exec {
    command = [
      "/usr/bin/touch",
      "/var/lib/openbao-agent/trigger/nginx-wildcard.ready"
    ]
    timeout = "5s"
  }
}
EOF
```
Maintenant nous allons effectuer la première émission controlée.
Exécutez l'agent : 
```shell
sudo -u openbao-agent \
  /usr/local/bin/bao agent \
  -config=/etc/openbao-agent/agent.hcl

Puis vérifiez les accès sans afficher les secrets :
```shell
sudo stat -c '%A %U:%G %s-octets %n' \
  /var/lib/openbao-agent/rendered/nginx-wildcard-bundle.pem

sudo grep -Ec '^-----BEGIN CERTIFICATE-----$' \
  /var/lib/openbao-agent/rendered/nginx-wildcard-bundle.pem

sudo grep -Ec '^-----BEGIN .*PRIVATE KEY-----$' \
  /var/lib/openbao-agent/rendered/nginx-wildcard-bundle.pem
```
Après avoir créé le role et activé le role openbao il faut créer l'unité systemd : 
```shell
sudo tee /etc/systemd/system/openbao-agent.service \
  >/dev/null <<'EOF'
[Unit]
Description=OpenBao Agent - renouvellement TLS Nginx
Documentation=https://openbao.org/docs/agent-and-proxy/agent/
Wants=network-online.target
After=network-online.target
StartLimitIntervalSec=60
StartLimitBurst=5

[Service]
Type=simple
User=openbao-agent
Group=openbao-agent

ExecStart=/usr/local/bin/bao agent -config=/etc/openbao-agent/agent.hcl

Restart=on-failure
RestartSec=5s
TimeoutStopSec=30s
UMask=0077

NoNewPrivileges=true
PrivateTmp=true
PrivateDevices=true
ProtectSystem=strict
ProtectHome=true
ProtectKernelTunables=true
ProtectKernelModules=true
ProtectControlGroups=true

ReadWritePaths=/var/lib/openbao-agent/rendered
ReadWritePaths=/var/lib/openbao-agent/trigger
ReadOnlyPaths=/etc/openbao-agent
ReadOnlyPaths=/usr/local/share/ca-certificates/superzone-root-ca.crt

[Install]
WantedBy=multi-user.target
EOF
```
Puis appliquer les droits à root : 
```shell
sudo chown root:root /etc/systemd/system/openbao-agent.service
sudo chmod 0644 /etc/systemd/system/openbao-agent.service
```
il faut maintenant vérifier la syntaxe du service systemd :
```shell
sudo systemd-analyze verify \
  /etc/systemd/system/openbao-agent.service
```
Activez maintenant le service : 
```shell
sudo systemctl daemon-reload
```
```shell
sudo systemctl enable --now openbao-agent.service
```

