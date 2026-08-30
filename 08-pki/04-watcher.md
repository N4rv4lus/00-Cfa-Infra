Nous allons maintenant diviser les droits.
Nous aurions pu affecter des droits directement à openbao de façon à ce qu'il exécute le renouvellement et le redémarrage nginx, mais il est préférable que ce soit un utilisateur dédié qui manage ces parties.

Le watcher est composé de plusieurs fichiers : 
- certwatcher.path
- cert-watcher.service
- watcher-ca.py

certwatcher.path utilise le programme système inotify, et activera le script de mise à jour dès que l'agent openbao va renouveller le wildcard *.superzone.com (tous les 2 jours)

cert-watcher.service va lui être déclenché par cert-watcher.path dès qu'une modification sera effectuée. Il activera le script watcher-ca.py

watcher-ca.py lui va effectuer la procédure suivante : 
- comparer hash du bundle actuel et le hash du nouveau bundle.
- si le bundle est modifié, il va créer un répertoire temporaire
- copier le nouveau bundle dans le répertoire temporaire et ensuite extraire la clé privée et la fullchain
- il va ensuite effectuer des tests sur la clé privée et la fullchain
- si les certificats sont valides, il va ensuite copier les certificat dans le repertoire tls du reverse proxy nginx puis effectuer un test de renouvellement des certificat du conteneur docker
- si le test est valide il va ensuite reload le conteneur docker (cela permet de ne pas avoir de downtime sur le reverse proxy)
- une fois le renouvellement effectué il va supprimer le répertoire temporaire et attendre un nouveau certificat.

Cela permet de renouveller automatiquement le certificat dédié au reverse proxy d'nginx.

Voici les droits à appliquer : 

getent group tls-rendered >/dev/null || sudo groupadd --system tls-rendered
getent group tls-deploy >/dev/null || sudo groupadd --system tls-deploy

id watcher >/dev/null 2>&1 || sudo useradd \
  --system \
  --home-dir /watcher \
  --no-create-home \
  --shell /usr/sbin/nologin \
  --user-group \
  watcher

sudo usermod -aG tls-rendered watcher
sudo usermod -aG tls-deploy watcher
sudo usermod -aG tls-rendered openbao-agent

sudo usermod -aG docker watcher

Droits du répertoire watcher : 
sudo chown root:watcher /watcher
sudo chmod 0750 /watcher

sudo install -d \
  -o watcher \
  -g watcher \
  -m 0700 \
  /watcher/extract

sudo install -d \
  -o watcher \
  -g watcher \
  -m 0700 \
  /watcher/tmp

sudo chown root:watcher /watcher/test-watcher.py
sudo chmod 0750 /watcher/test-watcher.py

Droits repertoire openbao : 
sudo chown openbao-agent:tls-rendered \
  /var/lib/openbao-agent/rendered

sudo chmod 2770 \
  /var/lib/openbao-agent/rendered

verif :
namei -l /var/lib/openbao-agent/rendered

maintenant modifier le template openbao :
sudoedit /etc/openbao-agent/agent.hcl

exemple : 
template {
  source           = "/etc/openbao-agent/templates/nginx-wildcard.pem.ctmpl"
  destination      = "/var/lib/openbao-agent/rendered/nginx-wildcard-bundle.pem"
  create_dest_dirs = false
  perms            = "0640"
}

Ajoutez au service openbao le umask 0027 :
sudo nano /etc/systemd/system/openbao-agent.service

[Service]
UMask=0027

Puis corrigez le ficheir actuel :

sudo chgrp tls-rendered \
  /var/lib/openbao-agent/rendered/nginx-wildcard-bundle.pem

sudo chmod 0640 \
  /var/lib/openbao-agent/rendered/nginx-wildcard-bundle.pem

et pour les fichiers déjà présents dans le repertoire nginx :

sudo chown watcher:tls-deploy \
  /store-docker-file/nginx-reverse/tls/fullchain.pem \
  /store-docker-file/nginx-reverse/tls/privkey.pem

sudo chmod 0640 \
  /store-docker-file/nginx-reverse/tls/fullchain.pem \
  /store-docker-file/nginx-reverse/tls/privkey.pem

vérifiez les répertoires :
namei -l /store-docker-file/nginx-reverse/tls

Configuration systemd du watcher : 

sudoedit /etc/systemd/system/cert-watcher.service

Contenu :
[Unit]
Description=Validation et déploiement TLS Nginx
Requires=docker.service
After=docker.service

[Service]
Type=oneshot
User=watcher
Group=watcher
SupplementaryGroups=tls-rendered tls-deploy docker
WorkingDirectory=/watcher
ExecStart=/usr/bin/python3 -u /watcher/test-watcher.py
Environment="PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
UMask=0027

Ensuite configurez le service inotify systemd :
sudoedit /etc/systemd/system/cert-watcher.path

contenu : 
[Unit]
Description=Surveillance du répertoire OpenBao

[Path]
PathChanged=/var/lib/openbao-agent/rendered
Unit=cert-watcher.service

[Install]
WantedBy=multi-user.target

affectez les droits aux fichiers systemd certwatcher : 
sudo chown root:root \
  /etc/systemd/system/cert-watcher.service \
  /etc/systemd/system/cert-watcher.path

sudo chmod 0644 \
  /etc/systemd/system/cert-watcher.service \
  /etc/systemd/system/cert-watcher.path

Puis rechargez et activer : 
sudo systemd-analyze verify \
  /etc/systemd/system/cert-watcher.service \
  /etc/systemd/system/cert-watcher.path

sudo systemctl daemon-reload
sudo systemctl restart openbao-agent.service
sudo systemctl enable --now cert-watcher.path

Maintenant vérifiez les droits : 
id watcher
id openbao-agent

stat -c '%U:%G %a %n' \
  /var/lib/openbao-agent/rendered \
  /var/lib/openbao-agent/rendered/nginx-wildcard-bundle.pem \
  /store-docker-file/nginx-reverse/tls

###### TEST & validation ######
Si vous rencontrez un problème : 
sudo usermod -aG tls-deploy watcher

sudo chown root:tls-deploy \
  /store-docker-file/nginx-reverse/tls

sudo chmod 2770 \
  /store-docker-file/nginx-reverse/tls

Puis pour les ficheirs déjà présents : 
sudo chown watcher:tls-deploy \
  /store-docker-file/nginx-reverse/tls/fullchain.pem \
  /store-docker-file/nginx-reverse/tls/privkey.pem

sudo chmod 0640 \
  /store-docker-file/nginx-reverse/tls/fullchain.pem \
  /store-docker-file/nginx-reverse/tls/privkey.pem

sur les ficheirs déjà présents : 
namei -l /store-docker-file/nginx-reverse/tls

ensuite effectuez le test suivant : 
sudo -u watcher test -r \
  /store-docker-file/nginx-reverse/tls/fullchain.pem \
  && echo "Lecture autorisée"

sudo -u watcher test -w \
  /store-docker-file/nginx-reverse/tls \
  && echo "Écriture autorisée"


