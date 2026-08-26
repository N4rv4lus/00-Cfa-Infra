# Installer mdadm outil de gestion pour raid (disque dur)

## Install mdam & parted
Install mdadm, it's a tool to setup raid configurations
```shell
sudo dnf install mdadm
```
List block for hard-drives
```shell
lsblk 
```

Install parted, it's a tool that permit to create partitions
```shell
sudo dnf install parted
```

Now set a first partition on your hardrive
```shell
sudo parted --script /dev/sdc "mklabel gpt" (parted programme / ) 
```
If you have multiple disks create a partition on each disk with an other name "sda" - "sdd"

## Now setup raid configuration on the 3 partitions

Setup raid 5 on each data disks (sda / sdc / sdd):
```shell
sudo mdadm --create --verbose /dev/md0 --level=5 --raid-devices=3 /dev/sda /dev/sdc /dev/sdd
```
Check your actions :
```shell 
mdadm –detail /dev/md0
```

Now format the disks
```shell
sudo mkfs.xfs /dev/md0
```
Now check your new configuration
```shell
lsblk 
```
