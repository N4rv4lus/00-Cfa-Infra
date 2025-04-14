Here you can create specific users and groups.
```shell
/sbin/groupadd -g 900 kubernetes
```
Now you've created a specific group you can create and add a user to this group (it was made that this user has the same UID as the group he's in)
And here the user created is a system user, you can not connect to him "/usr/sbin/nologin"
```shell
/sbin/useradd -r -u 900 -g 900 /usr/sbin/nologin kubernetes
```
Now to check that your user is in the write group there is a specific 
```shell
cat /etc/passwd | grep kub
```

You can also check this file specfically for groups : 
```shell
cat /etc/group
```

You can also create with :
```shell
sudo adduser new-user
```
It will create a specific user and a group with the same name and the same UID/GID.
Check that both group and users have been created : 
```shell
cat /etc/group | grep new-user
```
Here is the output : 
```shell
new-user:x:1003:1003:,,,:/home/new-user:/bin/bash
```
And for the user : 
```shell
cat /etc/passwd | grep new-user
```
Here is the group output :
(it will add the new-user in the users group, this is why you have our new-user mentionned in "users" group)
```shell
users:x:100:administrator,test-user,docker-test,new-user
new-user:x:1003:
```