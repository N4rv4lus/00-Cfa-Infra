## Labs and infratructure Application tests

Since I have a bad memory I rather right the commands and configuration I'm setting up for my labs to continuously test infrastructures applications.
Here you will find the recap of my tests of the following technologies.

Some of them have not been updated since my last year project where my team was supposed to build a public & private cloud.
Everything is hosted onPremise on my workstation.

### Workstation Environment
Workstation Specification : 
CPU : 7950x 16 cores - 32 threads
RAM : DDR5 128 GB
Storage : 9 To

## Lab overview
You will find multiple technologies tests.
Each part is set to have a markdown reviewing with some explanations and some commands to configure it, and some tests commands to validate that everything is running as intended.

### Linux CLI
This one is
Here you will find the recap of some of the work done during my studies at CFA Insta.
These files contains mostly linux environnement files, AND they are not intended to be use in PRODUCTION.

00-linux-cli => created during the studies, not improved. And mostly used to help some students to understand some commands regarding linux based commands. Manage users & group rights, network setup, ssh configurations with certificates, upgrade linux Kernel and more.

### DNS

01-DNS => The idea is to start with a DNS configuration. It is the central unit for IT infrastructure.

It is divided in 2 part, a regular DNS and a DNS set to use Dynamic DNS (DDNS) which allow to enable DHCP and to set an also dynamically set a DNS configuration for each new host based on their hostname.

Next steps : Improve the current configuration to set a DNS over TLS with custom certificates

### Ansible

02-Ansible => Set during the last master project
 
This will setup a small infrastructure (not secured for production), and automate most of the processes.
The idea was to automate the deployment to automatically set a DNS hostname for each new server, to deploy a prometheus server, to deploy kubernetes clusters (ETCD master and nodes) and to deploy dedicated services.

Next steps : Deep dive into ansible to test the pull mode, to deepdive in 

### Docker

03-Docker => Here is a recap of how docker works. How to build simple images, and to deploy python application and a monitoring stack Prometheus, grafana, node-exporters on a dedicated network.

Next steps : currently reviewing to add custom web certificates with an nginx reverse proxy.

### Kubernetes

04-Kubernetes => Kubernetes setup with metallb and flannel. Deployment files for services. And configuration files for ansible automatic configuration.

Next steps : Improve to add Argo CD and Harbor to build images and deploy configuration. Improve configurations for deployments and secrets management with openBao.

### NFS 

06-NFS(storage) => The idea is to set a centralized storage for servers. Manage users rights and to automount it.

### Python

07-python => small pyton code to configure docker images for testing.

### PKI

Newest configuration setup. The idea is to secure all the previous applications with custom certificates, and to automate the renew of certificates for each services and secrets using openbao.
For now there is only a root CA, an intermediate CA for web apps, a second intermediate CA dedicated for Openbao certificates, and OpenBao Setup (for of hashicorp vault).

Next steps : Deploy Openbao on Kubernetes and set openbao agent to automate certificates and secrets renewal.

### Windows

HyperV and powershell script made only for some tests.

## Review and next steps

Currently building a gitlab with a CI CD, and terraform server to fully automate the configuration and to have a clean IAC environment. And also to configure loki and an alerter to have a complete monitoring service.

The next stepts will be to add graphical review of the infrastructure with flows.

Thank you for reviewing this documentation repo. I know this is intended only for configurations and projects, but github permit to show my tests and hosts them for free.

Enjoy :)
