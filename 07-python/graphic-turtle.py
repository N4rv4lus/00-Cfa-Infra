import turtle

#escalier(taille, nb)
def escalier(taille, nb):
    for i in range(0, nb):
        t.forward(taille)
        t.left(90)
        t.forward(taille)
        t.right(90)
        #taille = taille - 10
        taille -= 10
    t.forward(taille)

t = turtle.Turtle()

def carre(segment):
    for i in range(0, 4):
        t.forward(segment)
        t.right(90)

def carres(segment_depart, nb):
    #taille = (i+1)*segment_depart
    for i in range(0, nb):
        segment = (i+1)*(i+1)*segment_depart
        carre(segment)

#escalier(60, 5)
carres(10, 10)

turtle.done()
