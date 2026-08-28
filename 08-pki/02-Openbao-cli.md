## Lister les configuration OpenBao

### Méthodes d’authentification
bao auth list -detailed

### Moteurs de secrets
bao secrets list -detailed

### Rôles PKI
bao list pki_services/roles
bao read pki_services/roles/tls-server-superzone

### Politiques
bao policy list
bao policy read nginx-tls-agent

### AppRoles, une fois AppRole activé
bao list auth/approle/role
bao read auth/approle/role/nginx-tls-agent

### Issuers de la PKI
bao list pki_services/issuers
bao read pki_services/config/issuers

## Exploitation du serveur openBao

### initialisation du serveur openBao
bao operator init

### déverouiller openBao
bao operator unseal

### vérouiller openBao
bao operator seal


bao operator rotate

### modifie les clé d'unseal
bao operator rotate-keys


bao operator key-status
bao operator generate-root