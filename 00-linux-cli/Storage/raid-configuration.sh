# Installer mdadm outil de gestion pour raid (disque dur)
sudo dnf install mdadm (pour le raid)
lsblk (list block - lister les disques dur) 
sudo dnf install parted 
sudo parted --script /dev/sdc "mklabel gpt" (parted programme / ) 
# remettre la meme commande sur chacun des disque 
# mise en place du raid 5 sur les 3disque de données (sda / sdc / sdd): 
sudo mdadm --create --verbose /dev/md0 --level=5 --raid-devices=3 /dev/sda /dev/sdc /dev/sdd
# Vérifiez vos actions : 
mdadm –detail /dev/md0
# formater le disque raid : 
sudo mkfs.xfs /dev/md0
# vérifier la liste des disque et de le raid 
lsblk 

