# Setup Docker Network

There are multiple type of network solutions in docker. Here we will see how to setup a bridge network.
All of the informations can be found on docker docs website.
(all the configurations files are stored in /var/lib/docker/)

First check docker networks :
```shell
docker network ls
```

```bash
NETWORK ID     NAME      DRIVER    SCOPE
cc7fc61985e6   bridge    bridge    local
2b745836f8c9   host      host      local
dc9127aa6cc4   none      null      local
```

Now to setup a simple docker network run :

```shell
docker network create -d bridge monitoring
```

and re-run docker network ls
```shell
docker network ls
```
Here is the output,  you can check that your bridged docker network has been created :
```bash
NETWORK ID     NAME         DRIVER    SCOPE
cc7fc61985e6   bridge       bridge    local
2b745836f8c9   host         host      local
b4676e55d8b4   monitoring   bridge    local
dc9127aa6cc4   none         null      local
```

You can also inspect it to now what is the base configuration : 

```shell
docker network inspect monitoring
```
Here is the output :
```json
[
    {
        "Name": "monitoring",
        "Id": "b4676e55d8b4c2a3e18b4d4863426fb5436c844459eacc5b00bdd08e9083ab70",
        "Created": "2025-03-16T19:47:36.69031135+01:00",
        "Scope": "local",
        "Driver": "bridge",
        "EnableIPv4": true,
        "EnableIPv6": false,
        "IPAM": {
            "Driver": "default",
            "Options": {},
            "Config": [
                {
                    "Subnet": "172.18.0.0/16",
                    "Gateway": "172.18.0.1"
                }
            ]
        },
        "Internal": false,
        "Attachable": false,
        "Ingress": false,
        "ConfigFrom": {
            "Network": ""
        },
        "ConfigOnly": false,
        "Containers": {},
        "Options": {},
        "Labels": {}
    }
]
```

## configure a network

Now remove the network you just created.
If your network have hosts you need to disconnect them.
To do so run :
```shell
docker network disconnect monitoring container_name
```
Now you can delete the network monitoring : 
```shell
docker network rm monitoring
```

Now here is an exemple to setup a network : 
```shell
docker network create --driver bridge --subnet=172.16.20.0/24 --gateway=172.16.20.1 --ip-range=172.16.20.128/25 monitoring
```
THe subnet permits you to create a specific IP scope for your custom bridged network, the gateway permit you to define the gateway of the scope, and the IP range permit you to limit the number of hosts on the network to a specific range, just don't forget to put the subnet mask.

Now you can connect host to this network, it will enable a new virtual network interface for your pod, here we will be adding this new network for all the containers that have been created in "Monitoring with Docker" (prometheus/grafana/node-exporter) :
```shell
docker network connect monitoring prometheus
docker network connect monitoring grafana
docker network connect monitoring node-exporter
```

Now inspect the new network, all the containers will be referenced inside :
```shell
docker inspect monitoring
```
Here is the output, check the section "container" :
```json
[
    {
        "Name": "monitoring",
        "Id": "70c27287e55449f7d90b06c1c84e7d8f70e627df8153b8abe73453eee9ca6df9",
        "Created": "2025-03-16T20:22:35.844868036+01:00",
        "Scope": "local",
        "Driver": "bridge",
        "EnableIPv4": true,
        "EnableIPv6": false,
        "IPAM": {
            "Driver": "default",
            "Options": {},
            "Config": [
                {
                    "Subnet": "172.16.20.0/24",
                    "IPRange": "172.16.20.128/25",
                    "Gateway": "172.16.20.1"
                }
            ]
        },
        "Internal": false,
        "Attachable": false,
        "Ingress": false,
        "ConfigFrom": {
            "Network": ""
        },
        "ConfigOnly": false,
        "Containers": {
            "083415c900801b339230b17fcd03c3011d2e720a33c91849ceb3086ecc106494": {
                "Name": "nd-exporter",
                "EndpointID": "981cb5aa7edf04cc6c5cc325907c36192293bb866587b27a0db01380c898b38f",
                "MacAddress": "4a:11:9a:8f:23:b9",
                "IPv4Address": "172.16.20.130/24",
                "IPv6Address": ""
            },
            "cb968b87f15db836ec187a6860a738e482700453d740e066f1fd885412219ae4": {
                "Name": "prometheus",
                "EndpointID": "bb4ff6c39bae6c91b2120626d5301d20156cd2f98e7a24ec4653ad7b9a45c7df",
                "MacAddress": "3e:fb:71:a5:f4:46",
                "IPv4Address": "172.16.20.129/24",
                "IPv6Address": ""
            },
            "ced952fcb712023d5b711fbb548448fb5769ef1e1f4f219e02105ef93675b54f": {
                "Name": "grafana",
                "EndpointID": "eae7d3dabde21bcb5db518045d0d1499e2023f983f25e0e7cdcce52a05b3f04f",
                "MacAddress": "d6:b3:9c:a8:4e:e8",
                "IPv4Address": "172.16.20.128/24",
                "IPv6Address": ""
            }
        },
        "Options": {},
        "Labels": {}
    }
]
```

Just to be sure that your configuration is working just modify the scrape config for promtheus (/etc/prometheus/prometheus.yml) and replace the old IP of node exporter by the new one, and all the containers will be accessible by their new IP.

