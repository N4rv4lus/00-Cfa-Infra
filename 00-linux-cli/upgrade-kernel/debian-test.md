check your version : 
uname -a

get your version codname : 
grep VERSION_CODENAME /etc/os-release

check the backports latest version in your source list : 
echo "deb http://ftp.debian.org/debian/ stretch-backports main non-free contrib" >> /etc/apt/sources.listapt-get update

refresh your package to update apt repo list : 
sudo apt-get update

search for the headers : 
apt search linux-headers

search for the image : 
apt search linux-image

select the image & the headers fitting and install them : 
apt install linux-headers-6.12.90+deb12-amd64/oldstable-backports linux-image-6.12.90+deb12.1-amd64

then reboot to apply the upgrade : 
apt install linux-headers-6.12.90+deb12-amd64/oldstable-backports linux-image-6.12.90+deb12.1-amd64

then check your kernel version : 
uname -r

- headers are needed for some applications/drivers to be compiled for your exact kernel version

- rt means "real time" which is better for applications/infrastructure needing quick execution / depending on latency, this may impact the stablity of the with "longer latency" but safer process management




