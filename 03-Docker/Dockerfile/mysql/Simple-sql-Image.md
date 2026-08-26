# Here is a small guide to build your first sql image with docker

## Create the directory and MYSQL Containers files
First create a new directory to store the files that will permit to build the image :
```shell
mkdir /docker-test/mysql
```

Here is the dockerfile overview :

We selected mysql image (it should pull the latest available form dockerhub)
Then the "WORKDIR" is the directory where the database will be running/stored.
The user for the container is "mysql".
And then there are environnement variables for sql engine :
We defined the "root password" but it will be modified when the sql engine will start because it is not a secured one and a good practice (remember this is just a lab), you should setup a secret.
The other environnement variables are for the production user : 
- db_user
- password = 0000
- one exemple for the database

The last part is the dedicated port to be open for mysql.

```Dockerfile
# syntax=docker/dockerfile:1

FROM mysql

WORKDIR /database

USER mysql

ENV MYSQL_ROOT_PASSWORD=0000

ENV MYSQL_USER=db_user
ENV MYSQL_PASSWORD=0000
ENV MYSQL_DATABASE=my_database

EXPOSE 3306

# no tested
## init.sql /docker-entrypoint-initdb.d/
```

## Build & test mysql container image
Now build it
```shell
docker build -t test-mysql:latest .
```
And now run it :
```shell
docker run --name new-test-mysql -d -p 127.0.0.1:3306:3306 test-mysql
```
And when it will be running you can connect to the sql database instance with the classic command :
```shell
mysql -h localhost -P 3306 -u db_user -p
```

If you have issues, you can check the containers logs with :
```shell
docker logs new-test-mysql
```