generate rsa key (public & private)
```shell
ssh-keygen.exe -t rsa -b 4096
```
-t = algo
-b size wanted

send public key
```shell
scp user-folder\.ssh\id_rsa.pub account-remote-server@yourIP:/home/user-dir/.ssh/authorized_keys
```
add passphrase

now use remote regular command
```shell
ssh account@hosts-ip-or-name
```

now enter your passphrase

Change SSH port - with selinux & firewallcmd

allez modifier le port sur sshd (ligne commentée)
```shell
nano /etc/ssh/sshd_config
```
pour valider votre modification affichez le fichier :
```shell
cat /etc/ssh/sshd_config | grep Port
```
ensuite allez modifier les ports d'écoutes pour l'application ssh dans selinux : 
```
sudo semanage port -a -t ssh_port_t -p tcp 2222
```
Vous pouvez maintenant voir les ports disponibles de cette façon : 
```
sudo cat /var/lib/selinux/targeted/active/ports.local
```
Ou sinon : 
```
sudo semanage port -l | grep ssh
```
Ensuite redémarrez le service sshd : 
```
systemctl restart sshd
```
Puis ouvrez le port via firewallcmd : 
```
sudo firewall-cmd --add-port=2222/tcp --permanent
firewall-cmd --remove-port=22/tcp --permanent
firewall-cmd --reload
```
ensuite confirmer les ports ouverts : 
```
sudo firewall-cmd --list-ports
```
