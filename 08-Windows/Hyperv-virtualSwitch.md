Créez un nouveau switch : 
New-VMSwitch -Name "NAT" -SwitchType Internal

Ensuite configurez la carte réseau de l’hôte HyperV et affectez lui une ip et un masque de sous réseau : 
New-NetIPAddress -IPAddress 192.168.100.1 -PrefixLength 24 -InterfaceAlias "vEthernet (NAT)"

Ensuite activez la fonctionnalité NAT sur la carte réseau et indiquez lui son nom et le réseau IP : 
New-NetNat -Name NAT -InternalIPInterfaceAddressPrefix 192.168.100.0/24

Puis allez vérifier dans hyper et dans windows vos cartes réseaux : 
Windows : 



HyperV : 

Ensuite paramètrez votre VM dans le scope ip : 
IP : entre 192.168.100.2/24 et 192.168.100.254/24
Passerelle : 192.168.100.1

plus voir : https://activedirectorypro.com/how-to-create-a-nat-switch-on-hyper-v/ 
permet de sélectionner le switch interne par l’ip 
