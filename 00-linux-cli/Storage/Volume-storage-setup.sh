# Création des disque data (pv physical volume / vg volume group / lv logical volume) : 
# Création du pv : 
# (pv create + chemin du raid) Si votre volume a des données, il va vous demander de le supprimer validez l’opération : 
sudo pvcreate /dev/md0

# Validez votre opération avec la commande : 
sudo pvs

# Création du vg : 
sudo vgcreate DATA /dev/md0
# Validez votre création avec : 
sudo vgs

# Création du lv : 
# (-l fournir une taille en % / 100% vg = 100% du vg et vg01 = nomvg )
sudo lvcreate -n lv_data -l 100%VG DATA 
sudo lvs (validez la configuration) : 


# Ensuite formatez le LV : 
sudo mkfs.xfs /dev/DATA/lv_data

# puis montez le point de montage : 
sudo mount -a
# puis vérifiez que c’est bien monté avec 
df -h 
# vous voyez le le lv_data et bien monté sur /srv

# Pour le montage automatique : 
sudo nano /etc/fstab : 
/dev/DATA/lv_data       /srv                    xfs     defaults        0 0

# Puis rebootez le système pour vérifier que le disque monte bien au démarrage : 
sudo reboot now
df -h 
