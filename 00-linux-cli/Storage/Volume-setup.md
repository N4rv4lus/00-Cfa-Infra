# Création des disque data (pv physical volume / vg volume group / lv logical volume) : 

## Création du pv : 
(pv create + chemin du raid) Si votre volume a des données, il va vous demander de le supprimer validez l’opération : 
```shell
sudo pvcreate /dev/md0
```
Validez votre opération avec la commande : 
```shell
sudo pvs
```

## Création du vg : 
```shell
sudo vgcreate DATA /dev/md0
```
Validez votre création avec : 
```shell
sudo vgs
```
# Création du lv : 
# (-l fournir une taille en % / 100% vg = 100% du vg et vg01 = nomvg )
```shell
sudo lvcreate -n lv_data -l 100%VG DATA 
```
Validez la configuration
```shell
sudo lvs
```

# Ensuite formatez le LV :
```shell
sudo mkfs.xfs /dev/DATA/lv_data
```
# puis montez le point de montage :
```shell
sudo mount -a
```
# puis vérifiez que c’est bien monté avec 
```shell
df -h
```
# vous voyez le le lv_data et bien monté sur /srv

# Pour le montage automatique : 
```shell
sudo nano /etc/fstab
```

```shell
/dev/DATA/lv_data       /srv                    xfs     defaults        0 0
```
# Puis rebootez le système pour vérifier que le disque monte bien au démarrage : 
```shell
sudo reboot now
```

```shell
df -h
```
