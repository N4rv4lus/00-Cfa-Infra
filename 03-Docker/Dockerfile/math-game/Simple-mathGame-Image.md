# Here is a small guide to build your first image with docker

## Create the directory and push the files
First create a new directory to store the files that will permit to build the image :
```shell
mkdir /docker-test/math-game
```
Now put your code in it : 
```shell
nano /docker-test/math-game/math-game.py
```
And copy/paste the file from the repo /math-game/math-game.py
```python
import random

NOMBRE_MIN = (1)
NOMBRE_MAX = (100)
NB_QUESTIONS = 10

#calculez : 1 + 5

def poser_question():
    a = random.randint(NOMBRE_MIN, NOMBRE_MAX)
    b = random.randint(NOMBRE_MIN, NOMBRE_MAX)
    o = random.randint(0, 1)
    while a == b:
        b=random.randint(NOMBRE_MIN, NOMBRE_MAX)
    operateur_str = "+"
    if o == 1:
        operateur_str = "*"
    reponse_str = input(f"Calculez: {a} {operateur_str} {b} = ")
    reponse_int = int(reponse_str)
    calcul = a+b
    if o == 1:
        calcul = a*b
    if reponse_int == calcul:
       # print("Réponse correcte")
        return True
    #else:
       # print("Réponse Incorrect")
    return False

nb_points = 0
for i in range(0, NB_QUESTIONS):
    print(f"Question n* {i+1} sur {NB_QUESTIONS}:")
    if poser_question():
        print("Réponse correcte")
        nb_points += 1
    else:
        print("Réponse incorrecte")
    print()

#votre note
print(f"Votre note est : {nb_points}/{NB_QUESTIONS}")

moyenne = int(NB_QUESTIONS/2)

if nb_points == NB_QUESTIONS:
    print("Excellent !")
elif nb_points == 0:
    print("Révisez vos maths !")
elif nb_points < moyenne:
    print(f"Peut mieux faire.")
elif nb_points > moyenne:
    print("Pas mal")
```

Now create you dockerfile : 
```shell
nano /docker-test/math-game/Dockerfile
```
And copy/paste the file from the repo /math-game/math-game.py
```Dockerfile
# syntax=docker/dockerfile:1

FROM rockylinux:9.3

# install app
RUN dnf upgrade -y && dnf install python3 python3-pip -y

# Copy script

COPY math-game.py /
```

Here is an explanation of the Dockerfile :
- " # syntax=docker/dockerfile:1 " is the way of how docker build will read this file
- "FROM rockylinux:9.3" set the image you will be using for this new image with the code you want to be inside the image
- "RUN dnf upgrade -y && dnf install python3 python3-pip -y" RUN will tell docker build to run this command (here is an upgrade and the installation of python to execute the "game")
- "COPY math-game.py /" is divied in 2 part, COPY will tell docker build to copy the file "math-game.py" in the new image directory, here it is "/"

## Create the image

1st search for the base image, here it's rockylinux9.3
```shell
docker search rockylinux9.3
```
This should be the output :
```shell
NAME                     DESCRIPTION   STARS     OFFICIAL
quiniana/rockylinux9.3                 0
```

Now go in the directory and run :
```shell
cd /docker-test/math-game/
docker run -it test-rocky:latest .
```
The name "test-rocky" will be your image name, and the ":latest" is a mention to have the latest image.
Now check the image :
```shell
docker image ls
```
And it should output : 
```shell
REPOSITORY                         TAG       IMAGE ID       CREATED          SIZE
test-rocky                         latest    c71fa700af71   43 minutes ago   375MB
prom/prometheus                    latest    503e04849f1c   2 weeks ago      295MB
grafana/grafana                    latest    dfed5fef9fdb   3 weeks ago      564MB
prom/node-exporter                 latest    aaa0ee0c2359   4 weeks ago      25MB
quay.io/prometheus/node-exporter   latest    aaa0ee0c2359   4 weeks ago      25MB
nginx                              latest    b52e0b094bc0   5 weeks ago      192MB
ubuntu                             latest    a04dc4851cbc   7 weeks ago      78.1MB
hello-world                        latest    74cc54e27dc4   7 weeks ago      10.1kB
```
Now run it and execute the small game :
```shell
docker run -it test-rocky:latest
```
Execute the script and try to win : 
```shell
python3 math-game.py
```
Here is a small exemple of the game :
```shell
Question n* 1 sur 10:
Calculez: 5 + 25 = 30
Réponse correcte

Question n* 2 sur 10:
Calculez: 92 * 70 = 200
Réponse incorrecte

Question n* 3 sur 10:
Calculez: 60 * 12 = 720
Réponse correcte

Question n* 4 sur 10:
Calculez: 2 + 26 = 28
Réponse correcte

Question n* 5 sur 10:
Calculez: 91 + 19 = 109
Réponse incorrecte

Question n* 6 sur 10:
Calculez: 12 + 46 = 58
Réponse correcte

Question n* 7 sur 10:
Calculez: 76 * 12 = 340
Réponse incorrecte

Question n* 8 sur 10:
Calculez: 39 + 41 = 60
Réponse incorrecte

Question n* 9 sur 10:
Calculez: 28 * 83 = 857
Réponse incorrecte

Question n* 10 sur 10:
Calculez: 47 * 96 = 58
Réponse incorrecte

Votre note est : 4/10
Peut mieux faire.
[root@3fdda3bb968c /]# exit
```






