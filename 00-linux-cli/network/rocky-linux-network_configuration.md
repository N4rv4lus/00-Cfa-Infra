## Network Configuration files

Here you will find where a stored network configuration files in rocky-linux 9.2 and how to configure them.

## nmcli

So you can configure your files with the nmcli (network management command line)
Nmcli will open a programm that will permit you to modify with ease your network files
```shell
nmtui
```
It will open the Network Manager UI :
- 1st "Edit a connection"
here you can modify all your server networks interfaces (ex : eth0, eth1 etc), and this works for IPV4 and IPV6
Set it to manual and set Adresses with you IP and a subnet mask, your gateway, your dns servers & search for specific domains, and you can specify specific routes

you can find the network configurations files in : 
/etc/NetworkManager/system-connections/eth0.nmconnection
there is file example in the repo

- 2nd "Activate a connection"
Here you can activate or disactivate your network interfaces

- 3rd "Set system hostname"
Here you can modify the server's hostname
you can also do it with the cli : 
```shell
hostnamectl hostname yourserver_wanted-hostname
```

- 4th part "Radio"
Here you can check if you have Wi-Fi hardware are existing, and enabled. It works for Wi-Fi and WWAN
