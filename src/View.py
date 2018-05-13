from tkinter import *


class Fenetre:
    """class générant une vue graphique"""

    def __init__(self, controller):
        self.controller = controller
        self.width = "800"
        self.height = "600"
        self.fenetre = Tk()
        self.fenetre.title("Space invaders")
        self.fenetre.geometry(self.width+"x"+self.height+"+100+100")
        self.fenetre.resizable(False, False)

        self.cadre = Cadre(self.fenetre, self.controller, self.width, self.height, relief='solid', borderwidth=1)
        self.cadre.show()

        self.menubar = BarMenu(self.fenetre, self.cadre, activeborderwidth=0, relief="flat")
        self.fenetre.config(menu=self.menubar)


class Cadre(Frame):
    """class gérant le contenu de la fenêtre"""

    def __init__(self, fenetre, controller, width, height, **kwargs):
        self.controller = controller
        self.width = width
        self.height = height
        Frame.__init__(self, fenetre, **kwargs)
        self.pack()

        self.canevas = Canvas(self, height=self.height, width=self.width, background="white")
        self.vaisseau = None
        self.missile = None
        self.ennemis = []
        self.missileEnnemis = []
        self.score = None
        self.canevas.focus_set()
        self.canevas.pack(side="bottom")

    def moveEnnemi(self):
        """ gère le déplacement des ennemis"""
        if self.controller.run:
            self.controller.moveEnnemi()
            self.after(40, self.moveEnnemi)

    def moveMissileEnnemis(self):
        """ gère le déplacement des missiles ennemis"""
        if self.controller.run:
            if len(self.missileEnnemis) != 0:
                for vMissile in self.missileEnnemis:
                    coord = self.canevas.coords(vMissile)
                    x = coord[0] - (coord[0] - coord[2])/2
                    y = coord[1] - (coord[1] - coord[3])/2
                    if coord[1] < int(self.height):
                        self.controller.moveMissileEnnemi(x, y)
                        if self.toucheMissileEnnemi(coord):
                            break
                    else:
                        self.controller.delMissileEnnemi(x, y)
            self.after(15, self.moveMissileEnnemis)

    def toucheMissileEnnemi(self, coordMissile):
        """ test si un missile ennemi touche le vaisseau"""
        coordVaisseau = self.canevas.coords(self.vaisseau)
        if coordMissile[2] > coordVaisseau[0] and coordMissile[0] < coordVaisseau[2] and coordMissile[3] > coordVaisseau[1]:
            self.controller.finPartie()
            return True
        else:
            return False

    def moveVaisseau(self, direction):
        coordVaisseau = self.canevas.coords(self.vaisseau)
        valeur = 20
        if direction == "gauche" and coordVaisseau[0]-valeur > 0:
            self.controller.moveVaisseau(direction, valeur)
        elif direction == "droite" and coordVaisseau[2] + valeur < int(self.width):
            self.controller.moveVaisseau(direction, valeur)

    def moveMissile(self):
        """gère le déplacement du missile du vaisseau"""
        if self.missile is not None:
            coordMissile = self.canevas.coords(self.missile)
            if coordMissile[3] > 0:
                self.controller.moveMissile()
                self.toucheMissile()
                self.after(20, self.moveMissile)
            else:
                self.controller.delMissile()

    def toucheMissile(self):
        """vérifie si le missile touche un ennemi"""
        coord = self.canevas.coords(self.missile)
        for invad in self.ennemis:
            coordInvad = self.canevas.coords(invad)
            if coord[3] < coordInvad[3] and coord[3] > coordInvad[1] and coord[0] >= coordInvad[0] and coord[2] <= coordInvad[2]:
                self.controller.touche(coordInvad[0]+(coordInvad[2]-coordInvad[0])/2, coordInvad[1]+(coordInvad[3]-coordInvad[1])/2)
                break

    def clavier(self, event):
        """gestion des événements venant du clavier"""
        if event.keysym == 'Left':
            self.moveVaisseau("gauche")
        elif event.keysym == 'Right':
            self.moveVaisseau("droite")
        elif event.keysym == 'space':
            if self.controller.tirVaisseau() == 0:
                self.moveMissile()

    def show(self):
        """affichage des objets du modele"""
        listObjet = self.canevas.find_all()
        for obj in listObjet:
            self.canevas.delete(obj)
        self.ennemis=[]
        self.missileEnnemis = []
        self.vaisseau = None
        self.missile = None
        self.score = None

        x1 = self.controller.jeu.vaisseau.x - self.controller.jeu.vaisseau.width/2
        y1 = self.controller.jeu.vaisseau.y - self.controller.jeu.vaisseau.height/2
        x2 = self.controller.jeu.vaisseau.x + self.controller.jeu.vaisseau.width/2
        y2 = self.controller.jeu.vaisseau.y + self.controller.jeu.vaisseau.height/2
        self.vaisseau = self.canevas.create_rectangle((x1, y1), (x2, y2), fill="red")
        if self.controller.jeu.vaisseau.missile is not None:
            x1 = self.controller.jeu.vaisseau.missile.x
            y1 = self.controller.jeu.vaisseau.missile.y - self.controller.jeu.vaisseau.missile.height/2
            x2 = self.controller.jeu.vaisseau.missile.x
            y2 = self.controller.jeu.vaisseau.missile.y + self.controller.jeu.vaisseau.missile.height/2
            self.missile = self.canevas.create_line((x1, y1), (x2, y2), width=self.controller.jeu.vaisseau.missile.width)

        for invad in self.controller.jeu.ennemis:
            self.ennemis.append(self.canevas.create_rectangle((invad.x-invad.width/2, invad.y-invad.height/2), (invad.x+invad.width/2, invad.y+invad.height/2), fill="yellow"))
            if invad.missile is not None:
                x1 = invad.missile.x
                y1 = invad.missile.y - invad.missile.height / 2
                x2 = invad.missile.x
                y2 = invad.missile.y + invad.missile.height / 2
                self.missileEnnemis.append(self.canevas.create_line((x1, y1), (x2, y2), width=invad.missile.width))

        self.score = self.canevas.create_text(5, 5, text="Score : "+str(self.controller.jeu.score), anchor="nw", font=('Arial', '12'))

        if self.controller.fin:
            self.canevas.create_text(int(self.width)/2, int(self.height)/2, text='GAME OVER !', anchor="s", font=('Arial', '50', 'bold'))

    def start(self):
        """ démarrage de la partie"""
        if not self.controller.run:
            self.controller.run = True
            self.canevas.bind('<Key>', self.clavier)
            self.moveEnnemi()
            self.moveMissileEnnemis()

    def finPartie(self):
        self.canevas.unbind('<Key>')


class BarMenu(Menu):
    """class gérant la barre de menu"""

    def __init__(self, fenetre, cadre, **kwargs):
        Menu.__init__(self, fenetre, **kwargs)
        self.actionMenu = Menu(self, tearoff=0, relief="flat", activeborderwidth=0)
        self.actionMenu.add_command(label="Nouvelle partie", command=lambda: cadre.controller.reset())
        self.actionMenu.add_command(label="Démarrer la partie", command=lambda: cadre.start())
        self.actionMenu.add_command(label="Quitter", command=fenetre.quit)
        self.add_cascade(label="Action", menu=self.actionMenu)
