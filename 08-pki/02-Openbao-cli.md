## Lister les configuration OpenBao

### Méthodes d’authentification
```shell
bao auth list -detailed
```
### Moteurs de secrets
```shell
bao secrets list -detailed
```
### Rôles PKI
```shell
bao list pki_services/roles
bao read pki_services/roles/tls-server-superzone
```
### Politiques
```shell
bao policy list
bao policy read nginx-tls-agent
```
### AppRoles, une fois AppRole activé
```shell
bao list auth/approle/role
bao read auth/approle/role/nginx-tls-agent
```
### Issuers de la PKI
```shell
bao list pki_services/issuers
bao read pki_services/config/issuers
```
## Exploitation du serveur openBao

### initialisation du serveur openBao
```shell
bao operator init
```
### déverouiller openBao
```shell
bao operator unseal
```
### vérouiller openBao
```shell
bao operator seal
```
```shell
bao operator rotate
```
### modifie les clé d'unseal
```shell
bao operator rotate-keys
```
```shell
bao operator key-status
bao operator generate-root
```