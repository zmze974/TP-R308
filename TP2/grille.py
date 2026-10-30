"""
TP2 - Partie A : la classe Grille.

Une grille de morpion, c'est juste un tableau de 3 lignes sur 3 colonnes.
En Python, on le range dans une liste qui contient 3 listes, et chaque
petite liste contient 3 cases.

    self.cases[0]  -> la premiere ligne  (3 cases)
    self.cases[1]  -> la deuxieme ligne
    self.cases[2]  -> la troisieme ligne

Pour parler d'une case on utilise deux nombres : (ligne, colonne).
La case en haut a gauche, c'est donc (0, 0) et celle en bas a droite (2, 2).
On commence a 0 parce que Python compte comme ca.
"""

VIDE = " "  # ce qu'on met dans une case ou personne n'a encore joue


class Grille:
    """Le plateau de jeu : 9 cases, 2 joueurs, 1 gagnant."""

    TAILLE = 3  # 3 lignes et 3 colonnes

    def __init__(self):
        # On fabrique 3 lignes, et dans chaque ligne 3 cases vides.
        # La double boucle "for ... in range" evite d'ecrire 9 fois VIDE.
        self.cases = [[VIDE for _ in range(self.TAILLE)] for _ in range(self.TAILLE)]

    # ------------------------------------------------------------------
    # Petites methodes utiles (elles servent aux autres methodes)
    # ------------------------------------------------------------------

    def dedans(self, x, y):
        """Vrai si la case (x, y) existe vraiment dans la grille.

        Ca evite les plantages quand quelqu'un tape 3, -1 ou autre chose
        qui n'existe pas dans une grille de 3 sur 3.
        """
        return (
            isinstance(x, int)
            and isinstance(y, int)
            and 0 <= x < self.TAILLE
            and 0 <= y < self.TAILLE
        )

    def est_libre(self, x, y):
        """Vrai si la case existe ET qu'elle est encore vide."""
        return self.dedans(x, y) and self.cases[x][y] == VIDE

    def cases_libres(self):
        """La liste de toutes les cases vides, sous la forme [(x, y), ...]."""
        libres = []
        for x in range(self.TAILLE):
            for y in range(self.TAILLE):
                if self.cases[x][y] == VIDE:
                    libres.append((x, y))
        return libres

    def copie(self):
        """Une photocopie de la grille.

        L'ordinateur s'en sert pour essayer des coups "pour de faux" :
        il joue sur la copie, regarde ce que ca donne, et jette la copie.
        La vraie grille, elle, ne bouge pas.
        """
        nouvelle = Grille()
        for x in range(self.TAILLE):
            for y in range(self.TAILLE):
                nouvelle.cases[x][y] = self.cases[x][y]
        return nouvelle

    # ------------------------------------------------------------------
    # Les methodes demandees dans l'enonce
    # ------------------------------------------------------------------

    def jouer(self, x, y, joueur):
        """Place le symbole du joueur ("X" ou "O") dans la case (x, y).

        Renvoie True si le coup est accepte, False s'il est refuse
        (case deja prise, ou case qui n'existe pas).
        """
        if not self.dedans(x, y):
            return False  # hors de la grille : on refuse
        if self.cases[x][y] != VIDE:
            return False  # case deja occupee : on refuse
        self.cases[x][y] = joueur
        return True

    def est_gagnant(self, j):
        """Vrai si le joueur j a aligne 3 symboles identiques.

        Il y a 8 facons de gagner : 3 lignes, 3 colonnes, 2 diagonales.
        On les teste toutes, c'est le plus simple a comprendre.
        """
        # Les 3 lignes
        for x in range(self.TAILLE):
            if (
                self.cases[x][0] == j
                and self.cases[x][1] == j
                and self.cases[x][2] == j
            ):
                return True

        # Les 3 colonnes
        for y in range(self.TAILLE):
            if (
                self.cases[0][y] == j
                and self.cases[1][y] == j
                and self.cases[2][y] == j
            ):
                return True

        # La diagonale qui part d'en haut a gauche
        if self.cases[0][0] == j and self.cases[1][1] == j and self.cases[2][2] == j:
            return True

        # La diagonale qui part d'en haut a droite
        if self.cases[0][2] == j and self.cases[1][1] == j and self.cases[2][0] == j:
            return True

        return False

    def est_plein(self):
        """Vrai si plus aucune case n'est libre (donc match nul)."""
        return len(self.cases_libres()) == 0

    def afficher(self):
        """Affiche la grille dans le terminal, avec des traits entre les cases."""
        for x in range(self.TAILLE):
            # On relie les 3 cases de la ligne avec des "|"
            print(" " + " | ".join(self.cases[x]))
            # Un trait de separation entre les lignes, sauf apres la derniere
            if x < self.TAILLE - 1:
                print("---+---+---")

    # ------------------------------------------------------------------

    def reinitialiser(self):
        """Remet toutes les cases a vide (pour rejouer une partie)."""
        for x in range(self.TAILLE):
            for y in range(self.TAILLE):
                self.cases[x][y] = VIDE
