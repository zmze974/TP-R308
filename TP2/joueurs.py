"""
TP2 - Partie B : les joueurs.

Le principe : que ce soit un humain ou l'ordinateur, le jeu appelle
toujours la meme methode prochain_coup(grille, symbole), et cette methode
renvoie une case sous la forme (x, y).

Du coup le jeu n'a pas besoin de savoir QUI joue : il demande juste
"ton coup ?" et il recoit une case. C'est ca, la programmation objet.
"""

import random

from grille import VIDE


class Joueur:
    """Le modele commun a tous les joueurs."""

    def __init__(self, nom):
        self.nom = nom

    def prochain_coup(self, grille, symbole):
        """Doit renvoyer (x, y). Chaque type de joueur le fait a sa facon."""
        raise NotImplementedError("Cette methode doit etre ecrite dans la classe fille")


class JoueurHumain(Joueur):
    """Un vrai joueur, qui tape son coup au clavier."""

    def prochain_coup(self, grille, symbole):
        # On redemande tant que la personne tape autre chose qu'un nombre.
        # (Les cases hors grille ou deja prises sont verifiees par le jeu.)
        while True:
            try:
                ligne = int(input(f"{self.nom}, quelle ligne ? (0, 1 ou 2) : "))
                colonne = int(input(f"{self.nom}, quelle colonne ? (0, 1 ou 2) : "))
                return (ligne, colonne)
            except ValueError:
                print("Il faut taper un nombre entier : 0, 1 ou 2.")
            except EOFError:
                # Ca arrive seulement si le clavier est ferme (ou si on a
                # envoye les reponses d'un coup) : on arrete proprement.
                print("\nPlus de saisie possible, on arrete le jeu.")
                raise SystemExit(0)


class JoueurIA(Joueur):
    """Un ordinateur qui joue completement au hasard."""

    def prochain_coup(self, grille, symbole):
        # On demande a la grille la liste des cases vides,
        # puis on en tire une au hasard.
        libres = grille.cases_libres()
        if not libres:
            return (0, 0)  # plus de case libre : le jeu s'arrete de toute facon
        return random.choice(libres)


class JoueurIAMalin(Joueur):
    """L'IA bonus : elle gagne si elle peut, sinon elle bloque l'adversaire."""

    def prochain_coup(self, grille, symbole):
        # 1. Est-ce que je peux gagner tout de suite ?
        coup = self._coup_gagnant(grille, symbole)
        if coup is not None:
            return coup

        # 2. Est-ce que l'adversaire peut gagner au prochain coup ?
        #    Si oui, je lui prends la case.
        adversaire = "O" if symbole == "X" else "X"
        coup = self._coup_gagnant(grille, adversaire)
        if coup is not None:
            return coup

        # 3. Sinon, au hasard, comme l'IA simple.
        libres = grille.cases_libres()
        if not libres:
            return (0, 0)
        return random.choice(libres)

    def _coup_gagnant(self, grille, symbole):
        """Cherche une case qui fait gagner tout de suite 'symbole'.

        On essaie chaque case vide sur une COPIE de la grille :
        si ca donne 3 alignes, on renvoie cette case.
        Si aucune ne marche, on renvoie None.
        """
        for (x, y) in grille.cases_libres():
            essai = grille.copie()
            essai.jouer(x, y, symbole)
            if essai.est_gagnant(symbole):
                return (x, y)
        return None
