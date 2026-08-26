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

## PATH 
Now we will see how to add access to specific command, files, directories to a group and then affect it to the users (mostly automatic if the user is in the group)
Here we will add command 



First we will make a new directory specifically for create links for commands to add them to this specific group :
sudo mkdir /opt/cmd-new-user

Now we will change the ownership of the new directory to root & new-user group : 
sudo chown root:new-user /opt/cmd-new-user/

Now we affect to the owner the rights to execute, read&write with 7, then for the group to read&execute with 5, and for the other 0 so nothing they cannot access it, read it, execute it :
```shell
sudo chmod 750 /opt/cmd-new-user
```
Now we'll be creating the link to the commands we want that the "new-user" group can use :
```shell
sudo ln -s /sbin/reboot /opt/cmd-new-user/sysctl
sudo ln -s /sbin/reboot /opt/cmd-new-user/reboot
```
Now reload the bash source for the current environnement of the correct user, here it is "new-user"
Here is the command to edit your bash environnement, and apply it :
```shell
echo 'export PATH="/opt/cmd-new-user:$PATH"' >> ~/.bashrc
source ~/.bashrc
```
And check it with :
```shell
echo $PATH
```
This is the output you should have :
```shell
/opt/cmd-new-user:/opt/cmd-new-user:/usr/local/bin:/usr/bin:/bin:/usr/local/games:/usr/games
```
So as you can see there is a new path "/opt/cmd-new-user".
But as he is not in the sudoers group and the 2 commands are stored in the /sbin that is locked to the sudoers group you cannot run them with that user/group.

## Add a user in a group
So here we will be adding a user in the group we just created :
```shell
sudo usermod -aG new-user test-test
```
You can check that the user "test-test" have been added in the new group with :
```shell
groups test-test
```
Here is the output : 
```shell
test-test : test-test users new-user
```
Now you still have to refresh the current shell :
```shell
echo 'export PATH="/opt/cmd-new-user:$PATH"' >> ~/.bashrc
source ~/.bashrc
echo $PATH #still here to check the output
```
Here is the output :
```shell
/opt/cmd-new-user:/usr/local/bin:/usr/bin:/bin:/usr/local/games:/usr/games
```
We can check by pushing a script inside this directory, all the users in the group can execute the scripts or specific commands we don't want to store in /bin or /sbin.
Since last time we have pushed a new script in this directory "math-game.py", and since the user "test-test" is in the group new-user and it's shell have been refreshed the user can run the script where ever he wants.
First check the script with :
```shell
ls -als /opt/cmd-new-user/
```
Here is the output : 
```shell
total 12
4 drwxr-x--- 2 root new-user 4096 Apr 15 16:06 .
4 drwxr-xr-x 4 root root     4096 Apr 14 22:14 ..
4 -rwxr-xr-x 1 root root     1421 Apr 15 16:06 math-game.py
0 lrwxrwxrwx 1 root root       12 Apr 14 22:17 reboot -> /sbin/reboot
0 lrwxrwxrwx 1 root root       12 Apr 14 22:18 sysctl -> /sbin/sysctl
```
Now run :
```shell
math-game.py
```
Here is the output :
```python
Question n* 1 sur 10:
Calculez: 50 + 31 = 81
Réponse correcte

Question n* 2 sur 10:
Calculez: 39 * 26 =
```