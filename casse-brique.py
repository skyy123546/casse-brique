#Création d'un casse brique basique en une centaine de lignes avec reset, restart et système de score#
#utilisation de tkinter, messagebox et random uniquement#


##############importation des librairies nécessaires#############################################################
import tkinter as tk
from tkinter import messagebox
import random
###########################################################################################################################
################initialisation de toutes les variables utilisées dans les fonctions#############################
f = tk.Tk()             #création de la fenêtre de jeu
f.title('Casse Brique')             #ajout d'un titre à la fenêtre de jeu


c = tk.Canvas(width=800, height=800, background='grey')             #création du canvas ou feuille de dessin
c.pack()


r = c.create_rectangle(400, 760, 500, 780, fill = 'red', outline='black')               #création de la raquette
b = c.create_oval(400, 400, 425, 425, fill='blue', outline='black')             #création de la balle


score = 0
score_label = tk.Label(f, text=f"Score : {score}", foreground='black', background='white', font=('Arial', '20')) #ajout du score
score_label.pack()


touches = set()    #ajout d'une dimension de stockage des touches du clavier (limité à une touche par stockage)
pas = 7             #ajout de la vitesse de déplacement de la balle
dbx, dby = pas, pas   #ajout de la vitesse x et y de la balle influencées par la vitesse de déplacement de la balle
####################################################################################################################
######Création des fonctions de déplacement, mouvement, collisions, reset, restart et création de bricks#######
def input(event):               #création du stockage d'une touche du clavier lorsque l'on enfonce celle-ci
    touches.add(event.keysym)


def output(event):       #création de la destruction de la touche du clavier enfoncée dans l'espace de stockage
    try:
        touches.remove(event.keysym)
    except:
        pass


def replay(): #ajout d’un msg demandant au joueur s'il veut rejouer et soit redémarrant le jeu soit le détruisant
    if messagebox.askyesno("Rejouer", "Voulez vous rejouer ?"):
        game_reset()
    else:
        f.destroy()	#la fenêtre se ferme


def game_reset():     #réinitialisation de toutes les variables à leur valeur de départ lorsque le jeu redémarre
    global dbx, dby, score, touches
    dbx, dby = pas, pas
    touches = set() #vraiment à ne pas oublier VRAIMENT!!!
    score = 0	#score initial
    c.coords(r, 400, 760, 500, 780)
    c.coords(b, 400, 400, 425, 425)
    score_label['text'] = "Score : 0"
    bricks()   ################## on avait oublié de réinitialiser les briques!!! mais attention il peut encore y avoir des bugs de briques qui ne se détruisent pas lorsque la balle les touche à la prochaine game, pourtant il y en a qui se détruisent du 1er coup… j’ai pas pu encore trouver comment résoudre le bug… 


def update_score():
    global score
    score_label.config(text=f"Score : {score}")


def movement():     #création mouvement raquette, balle, collisions entre ceux-ci et collisions balle et bricks
    global dbx, dby, score
    raquette = c.coords(r)
    balle = c.coords(b)


    if 'q' in touches and raquette[0] > 0:
        c.move(r, -10, 0)
    if 'd' in touches and raquette[2] < 800:
        c.move(r, 10, 0)


    if balle[0] < 0:
        dbx = pas
    if balle[1] < 0:
        dby = pas
    if balle[2] > 800:
        dbx = -pas
    if balle[3] > 800:
        replay()


    if (balle[0] + balle[2]) / 2 > raquette[0] and (balle[0] + balle[2]) / 2 < raquette[2] and balle[3] > raquette[1]:
        dby = -pas


    c.move(b, dbx, dby)
    f.after(30, movement)


    coll = c.find_overlapping(*balle)
    if len(coll) >= 2:
        if coll[1] == 2:
            pass
        if coll[1] > 2:
            print(coll[1])   #/non obligatoire juste pour faire apparaître virtuellement la collision\
            c.delete(coll[1])
            dby = pas
            score += 1
            update_score()
            if score == 40:
                replay()


def bricks():               #création des bricks et ajout d'une couleur aléatoire à chaque démarrage du jeu
    couleur = ['red', 'green', 'blue']
    i = random.randint(0, 2)
    for y in range(0, 120, 30):
        for x in range(0, 800, 80):
            c.create_rectangle(x, y, x + 80, y + 30, fill=couleur[i], outline='black')
###################################################################################################################
############appelle des fonctions, des touches du clavier ainsi que de la fenêtre de jeu######################
movement()
bricks()
f.bind('<KeyPress>', input)
f.bind('<KeyRelease>', output)
f.mainloop()
##################################################################################################################
