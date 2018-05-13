class Spaceship:
    """ classe définissant le vaisseau du joueur"""

    def __init__(self):
        self.x = 400
        self.y = 550
        self.width = 30
        self.height = 30
        self.missile = None

    def move(self, direction, valeur):
        """méthode gérant le déplacement horizontal du vaisseau"""
        if direction == "gauche":
            self.x -= valeur
            return 0
        elif direction == "droite":
            self.x += valeur
            return 0
        else:
            return 1

    def tirMissile(self):
        """méthode créant un nouveau missile"""
        if self.missile is None:
            self.missile = Missile("haut", self.x, self.y-self.height/2)


class Invader:
    """classe définissant les ennemis"""

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 30
        self.height = 30
        self.missile = None

    def move(self, direction, valeur):
        """méthode gérant le déplacement de l'ennemi"""
        if direction == "gauche":
            self.x -= valeur
            return 0
        elif direction == "droite":
            self.x += valeur
            return 0
        elif direction == "haut":
            self.y -= valeur
            return 0
        elif direction == "bas":
            self.y += valeur
            return 0
        else:
            return 1

    def tirMissile(self):
        """méthode créant un nouveau missile"""
        if self.missile is None:
            self.missile = Missile("bas", float(self.x), self.y+self.height/2)


class Missile:
    """classe définissant les missiles"""

    def __init__(self, direction, x, y):
        self.direction = direction
        self.width = 3
        self. height = 20
        self.x = x
        self.y = y-self.height/2

    def move(self):
        """méthode gérant le déplacement du missile"""
        if self.direction == "haut":
            self.y -= 10
            return 0
        elif self.direction == "bas":
            self.y += 10
            return 0
        else:
            return 1


class Jeu:
    """classe gérant tous les modèles du jeu"""

    def __init__(self):
        self.nbLigneEnnemi = 3
        self.nbColonneEnnemi = 9
        self.vaisseau = Spaceship()
        self.ennemis = []
        self.score = 0

        for i in range(0, self.nbLigneEnnemi):
            for j in range(0, self.nbColonneEnnemi):
                self.ennemis.append(Invader(100+j*50, 25+i*50))

    def wave(self):
        for i in range(0, self.nbLigneEnnemi):
            for j in range(0, self.nbColonneEnnemi):
                self.ennemis.append(Invader(100+j*50, 25-i*50))

