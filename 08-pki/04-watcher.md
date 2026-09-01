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
```shell
getent group tls-rendered >/dev/null || sudo groupadd --system tls-rendered
getent group tls-deploy >/dev/null || sudo groupadd --system tls-deploy
```
```shell
id watcher >/dev/null 2>&1 || sudo useradd \
  --system \
  --home-dir /watcher \
  --no-create-home \
  --shell /usr/sbin/nologin \
  --user-group \
  watcher
```
```shell
sudo usermod -aG tls-rendered watcher
sudo usermod -aG tls-deploy watcher
sudo usermod -aG tls-rendered openbao-agent
sudo usermod -aG docker watcher
```
Droits du répertoire watcher : 
```shell
sudo chown root:watcher /watcher
sudo chmod 0750 /watcher
```
```shell
sudo install -d \
  -o watcher \
  -g watcher \
  -m 0700 \
  /watcher/extract
```
```shell
sudo install -d \
  -o watcher \
  -g watcher \
  -m 0700 \
  /watcher/tmp
```
```shell
sudo chown root:watcher /watcher/test-watcher.py
sudo chmod 0750 /watcher/test-watcher.py
```
Droits repertoire openbao : 
```shell
sudo chown openbao-agent:tls-rendered \
  /var/lib/openbao-agent/rendered
```
```shell
sudo chmod 2770 \
  /var/lib/openbao-agent/rendered
```
verif :
```shell
namei -l /var/lib/openbao-agent/rendered
```
maintenant modifier le template openbao :
```shell
sudoedit /etc/openbao-agent/agent.hcl
```
exemple : 
```shell
template {
  source           = "/etc/openbao-agent/templates/nginx-wildcard.pem.ctmpl"
  destination      = "/var/lib/openbao-agent/rendered/nginx-wildcard-bundle.pem"
  create_dest_dirs = false
  perms            = "0640"
}
```
Ajoutez au service openbao le umask 0027 :
```shell
sudo nano /etc/systemd/system/openbao-agent.service
```
```shell
[Service]
UMask=0027
```
Puis corrigez le ficheir actuel :

```shell
sudo chgrp tls-rendered \
  /var/lib/openbao-agent/rendered/nginx-wildcard-bundle.pem
```
sudo chmod 0640 \
  /var/lib/openbao-agent/rendered/nginx-wildcard-bundle.pem
```
et pour les fichiers déjà présents dans le repertoire nginx :
```shell
sudo chown watcher:tls-deploy \
  /store-docker-file/nginx-reverse/tls/fullchain.pem \
  /store-docker-file/nginx-reverse/tls/privkey.pem

sudo chmod 0640 \
  /store-docker-file/nginx-reverse/tls/fullchain.pem \
  /store-docker-file/nginx-reverse/tls/privkey.pem
```
vérifiez les répertoires :
```shell
namei -l /store-docker-file/nginx-reverse/tls
```
Configuration systemd du watcher : 
```shell
sudoedit /etc/systemd/system/cert-watcher.service
```
Contenu :
```shell
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
```
Ensuite configurez le service inotify systemd :
```shell
sudoedit /etc/systemd/system/cert-watcher.path
```
contenu :
```shell 
[Unit]
Description=Surveillance du répertoire OpenBao

[Path]
PathChanged=/var/lib/openbao-agent/rendered
Unit=cert-watcher.service

[Install]
WantedBy=multi-user.target
```
affectez les droits aux fichiers systemd certwatcher : 
```shell
sudo chown root:root \
  /etc/systemd/system/cert-watcher.service \
  /etc/systemd/system/cert-watcher.path

sudo chmod 0644 \
  /etc/systemd/system/cert-watcher.service \
  /etc/systemd/system/cert-watcher.path
```
Puis rechargez et activer : 
```shell
sudo systemd-analyze verify \
  /etc/systemd/system/cert-watcher.service \
  /etc/systemd/system/cert-watcher.path
```
```shell
sudo systemctl daemon-reload
sudo systemctl restart openbao-agent.service
sudo systemctl enable --now cert-watcher.path
```
Maintenant vérifiez les droits : 
```shell
id watcher
id openbao-agent
```
```shell
stat -c '%U:%G %a %n' \
  /var/lib/openbao-agent/rendered \
  /var/lib/openbao-agent/rendered/nginx-wildcard-bundle.pem \
  /store-docker-file/nginx-reverse/tls
```
###### TEST & validation ######
Si vous rencontrez un problème : 
```shell
sudo usermod -aG tls-deploy watcher

sudo chown root:tls-deploy \
  /store-docker-file/nginx-reverse/tls

sudo chmod 2770 \
  /store-docker-file/nginx-reverse/tls
```
Puis pour les ficheirs déjà présents : 
```shell
sudo chown watcher:tls-deploy \
  /store-docker-file/nginx-reverse/tls/fullchain.pem \
  /store-docker-file/nginx-reverse/tls/privkey.pem

sudo chmod 0640 \
  /store-docker-file/nginx-reverse/tls/fullchain.pem \
  /store-docker-file/nginx-reverse/tls/privkey.pem
```
sur les ficheirs déjà présents : 
```shell
namei -l /store-docker-file/nginx-reverse/tls
```
ensuite effectuez le test suivant : 
```shell
sudo -u watcher test -r \
  /store-docker-file/nginx-reverse/tls/fullchain.pem \
  && echo "Lecture autorisée"

sudo -u watcher test -w \
  /store-docker-file/nginx-reverse/tls \
  && echo "Écriture autorisée"
```

