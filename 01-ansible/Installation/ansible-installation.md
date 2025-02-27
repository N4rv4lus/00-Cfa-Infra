# Ansible Installation and configuration



## Getting started

Here is a small procedure to install ansible and make fun projects with it like configuring server, deploying agents, kubernetes Pods etc

## Installation

1st install epel-release

```
sudo dnf install epel-release -y
```

2nd step install ansible

```
sudo dnf install ansible -y
```

3rd step make a directory "group_vars" in /etc/ansible/group_vars

```
sudo mkdir /etc/ansible/group_vars
```

4th step create a host file where you will be storing and configuring your hosts files

```
sudo mkdir /etc/ansible/hosts
```

## add your hosts : 

Here a small cli to exchange rsa keys between ansible and the host where you will be launching playbook and commands

```
cat ~/.ssh/id_rsa.pub | ssh host-user@hostname "mkdir -p ~/.ssh && touch ~/.ssh/authorized_keys && chmod -R go= ~/.ssh && cat >> ~/.ssh/authorized_keys"
```

now configure your hosts file, you can find an exemple in ansible/ansible-hosts-file/hosts.yml
Here is a small exemple of what should look like : 

```
[group-name]
hostname
```

Now you can check that your host is accessible : 

```
ansible -m ping all
```
