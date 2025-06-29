generate rsa key (public & private)
```shell
ssh-keygen.exe -t rsa -b 4096
```
-t = algo
-b size wanted

send public key
```shell
scp user-folder\.ssh\id_rsa.pub account-remote-server@yourIP:/home/user-dir/.ssh/authorized_keys
```
add passphrase

now use remote regular command
```shell
ssh account@hosts-ip-or-name
```

now enter your passphrase