#!/usr/bin/env python3
# the first line is made to run the script everywhere
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




