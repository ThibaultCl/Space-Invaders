from src.Model import Jeu
from src.View import Fenetre
from random import randint


class Controller:
    """class controlant la vue et le modèle"""

    def __init__(self):
        self.run = False
        self.fin = False
        self.vague = 0
        self.direction = "droite"
        self.jeu = Jeu()
        self.fenetre = Fenetre(self)

    def moveVaisseau(self, direction, valeur):
        """déplacement du vaisseau"""
        self.jeu.vaisseau.move(direction, valeur)
        self.fenetre.cadre.show()

    def tirVaisseau(self):
        """tire d'un missile par le vaisseau"""
        if self.jeu.vaisseau.missile is None:
            self.jeu.vaisseau.tirMissile()
            self.fenetre.cadre.show()
            return 0
        else:
            return 1

    def moveMissile(self):
        """gère le déplacement du missile tiré par le vaisseau """
        if self.jeu.vaisseau.missile is not None and not self.fin:
            self.jeu.vaisseau.missile.move()
        self.fenetre.cadre.show()

    def touche(self, x, y):
        """methode appelé lorsque le missile touche un ennemi"""
        invader = self.findInvader(x, y)
        self.jeu.ennemis.remove(invader)
        self.jeu.vaisseau.missile = None
        self.jeu.score += 5
        self.fenetre.cadre.show()

    def delMissile(self):
        """supression du missile du vaisseau"""
        self.jeu.vaisseau.missile = None
        self.fenetre.cadre.show()

    def tirEnnemi(self, invader):
        """gère aléatoirement le tir d'un missile ennemi"""
        rnd = randint(0, 300)
        if rnd == 200 and invader.missile is None:
            invader.tirMissile()
            self.fenetre.cadre.show()
            return 0
        else:
            return 1

    def moveMissileEnnemi(self, x, y):
        """gère le déplacement d'un missile ennemi"""
        missile = self.findMissile(x, y)
        if missile is not None and not self.fin:
            missile.move()

    def delMissileEnnemi(self, x, y):
        """supprime un missile ennemi"""
        missile = self.findMissile(x, y)
        for invad in self.jeu.ennemis:
            if invad.missile is not None and missile is not None:
                if invad.missile.x == missile.x and invad.missile.y == missile.y:
                    invad.missile = None

    def moveEnnemi(self):
        """gère le déplacement des ennemis et du score"""
        movedir = self.direction
        if len(self.jeu.ennemis) > 0:
            self.jeu.score += 1
            for invad in self.jeu.ennemis:
                invad.move(movedir, 5)
                self.tirEnnemi(invad)
                if invad.x <= 80 or invad.x >= int(self.fenetre.width)-80:
                    if movedir == self.direction:
                        self.switchDir()
                        for invader in self.jeu.ennemis:
                            invader.move("bas", 20)
                if invad.y+invad.height/2 >= self.jeu.vaisseau.y-self.jeu.vaisseau.height/2:
                    self.finPartie()
        else:
            self.jeu.score += 2

        if self.jeu.score // 1000 > self.vague:
            if len(self.jeu.ennemis) == 0:
                self.jeu.wave()
                self.vague += 1
            else:
                if movedir != self.direction and self.direction == "droite":
                    self.jeu.wave()
                    self.vague += 1
        self.fenetre.cadre.show()

    def findInvader(self, x, y):
        """retourn un ennemi en fonction d'un (x, y)"""
        for invader in self.jeu.ennemis:
            if invader.x == x and invader.y == y:
                return invader

    def findMissile(self, x, y):
        """retourn un missile en fonction d'un (x, y)"""
        for invader in self.jeu.ennemis:
            if invader.missile is not None:
                if invader.missile.x == x and invader.missile.y == y:
                    return invader.missile
        return None

    def finPartie(self):
        """met fin à un partie"""
        self.fin = True
        self.run = False
        self.fenetre.cadre.finPartie()
        self.fenetre.cadre.show()

    def reset(self):
        """réinitialise toutes les données pour faire une nouvelle partie"""
        self.jeu.vaisseau.x = 400
        self.jeu.vaisseau.y = 550
        self.jeu.ennemis = []
        self.jeu.__init__()
        self.jeu.score = 0
        self.vague = 0
        self.direction = "droite"
        self.run = False
        self.fin = False
        self.fenetre.cadre.finPartie()
        self.fenetre.cadre.show()

    def switchDir(self):
        """switch la direction de déplacement des ennemis"""
        if self.direction == "droite":
            self.direction = "gauche"
        elif self.direction == "gauche":
            self.direction = "droite"


if __name__ == "__main__":
    controller = Controller()
    controller.fenetre.fenetre.mainloop()
