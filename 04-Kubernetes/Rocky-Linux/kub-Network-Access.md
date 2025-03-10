## Deploy a Loadbalancer for kubernetes with Metallb

Since we are creating a kubernetes cluster OnPremise, there is no Loadbalancer service on the cloud

There are 4 different kind of service (network access to pods) in Kubernetes :
- ClusterIP
- NodePort
- LoadBalancer
- Ingress

To get network information you can use these commands : 

```shell
kubectl get services
```

or 
```shell
kubectl get svc
```

it should output :

```sql
NAME                 TYPE           CLUSTER-IP      EXTERNAL-IP       PORT(S)          AGE
service/kubernetes   ClusterIP      10.96.0.1       <none>            443/TCP          226d
service/mysql01      NodePort       10.107.134.86   <none>            3306:30040/TCP   222d
service/nginx5       LoadBalancer   10.99.62.93     192.168.100.201   80:30495/TCP     1s
```

# Cluster IP

ClusterIP is used for internal communication.
It is dedicated for pods to communicate inside the cluster, and will permit the pods hosting apps to communicate together. 
It cannot be accessed outside the cluster, so if you want to access your application from another server or from a browser you will need to set another network service.

```sql
NAME                 TYPE           CLUSTER-IP      EXTERNAL-IP       PORT(S)          AGE
service/kubernetes   ClusterIP      10.96.0.1       <none>            443/TCP          226d
```

# NodePort

NodePort is used to open a port on the node where the pod is hosted.
The port dedicated for nodePort in kubernetes are between 30000-32767.
To access the service you need to know on which host the pod is hosted.

You can check the host and the node with :

```shell
kubectl get pods -o wide && kubectl get svc
```

Voici l'output : 
For the nodes
```sql
NAME                            READY   STATUS    RESTARTS   AGE   IP            NODE        NOMINATED NODE   READINESS GATES
web-app-7d9c6b5b8d-vgkdz       1/1     Running   0          5h    10.244.0.4    node-1      <none>           <none>
database-6f7c89d65f-lxg4j      1/1     Running   2          10h   10.244.0.5    node-2      <none>           <none>
nginx-ingress-controller-2w7kp 1/1     Running   0          3h    10.244.0.6    node-3      <none>           <none>
```

For services
```sql
NAME            TYPE           CLUSTER-IP       EXTERNAL-IP   PORT(S)          AGE   SELECTOR
kubernetes      ClusterIP      10.96.0.1        <none>        443/TCP          12d   <none>
my-service      NodePort       10.108.47.11     <none>        80:30007/TCP     5h    app=my-app
nginx-service   LoadBalancer   10.107.55.23     35.202.45.67  80:32000/TCP     8h    app=nginx
```

It is possible to have a more tailord one with jq(json)

```shell
kubectl get pods -o custom-columns="POD_NAME:.metadata.name,NODE:.spec.nodeName,IP:.status.podIP,EXTERNAL_IP:.status.hostIP"
```
Here is the output :
```sql
POD_NAME                    NODE        IP            EXTERNAL_IP
web-app-7d9c6b5b8d-vgkdz    node-1      10.244.0.4    192.168.1.1
database-6f7c89d65f-lxg4j   node-2      10.244.0.5    192.168.1.2
nginx-ingress-controller-2w7kp node-3  10.244.0.6    192.168.1.3
```

# LoadBalancer


