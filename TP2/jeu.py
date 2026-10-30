"""
TP2 - Partie C : le jeu complet.

Cette classe fait tourner une partie de bout en bout :
- elle fait jouer les deux joueurs chacun a son tour,
- elle verifie que le coup est valide (et sinon, le meme joueur rejoue),
- elle s'arrete quand quelqu'un gagne ou quand la grille est pleine,
- elle compte les points sur plusieurs parties (bonus).
"""

from grille import Grille


class Jeu:
    """Le chef d'orchestre du morpion."""

    def __init__(self, joueur_x, joueur_o, bavard=True):
        # joueur_x joue les X, joueur_o joue les O
        self.joueur_x = joueur_x
        self.joueur_o = joueur_o
        # bavard = False : on n'affiche rien (pratique pour 20 parties d'affilee)
        self.bavard = bavard
        # Le tableau des scores. Les cles sont les symboles, pas les noms :
        # comme ca ca marche meme si les deux joueurs s'appellent pareil.
        self.scores = {"X": 0, "O": 0}
        self.nuls = 0
        self.parties_jouees = 0

    # ------------------------------------------------------------------

    def _verifier(self, grille, coup):
        """Verifie un coup. Renvoie (True, "") si valide, (False, raison) sinon."""
        # Le coup doit etre un couple de deux nombres : (x, y)
        if not isinstance(coup, (tuple, list)) or len(coup) != 2:
            return False, "le coup n'est pas de la forme (ligne, colonne)"

        x, y = coup

        if not isinstance(x, int) or not isinstance(y, int):
            return False, "la ligne et la colonne doivent etre des nombres entiers"

        if not grille.dedans(x, y):
            return False, f"la case ({x}, {y}) n'existe pas, la grille va de 0 a 2"

        if not grille.est_libre(x, y):
            return False, f"la case ({x}, {y}) est deja occupee"

        return True, ""

    # ------------------------------------------------------------------

    def jouer_partie(self):
        """Joue UNE partie entiere.

        Renvoie "X" ou "O" si ce joueur gagne, None si match nul.
        """
        grille = Grille()
        # Les deux joueurs ranges dans l'ordre de jeu : X commence.
        joueurs = [(self.joueur_x, "X"), (self.joueur_o, "O")]
        tour = 0
        refus = 0  # nombre de coups refuses d'affilee

        while True:
            joueur, symbole = joueurs[tour % 2]  # pair -> X, impair -> O

            if self.bavard:
                print()
                grille.afficher()
                print(f"Au tour de {joueur.nom} ({symbole}).")

            coup = joueur.prochain_coup(grille, symbole)
            valide, raison = self._verifier(grille, coup)

            if not valide:
                # Coup refuse : on affiche pourquoi et le MEME joueur rejoue.
                # Comme on ne change pas 'tour', c'est bien le meme joueur.
                refus += 1
                if refus >= 20:
                    # Securite : un joueur qui n'envoie QUE des coups invalides
                    # ferait tourner le programme a l'infini. On coupe.
                    if self.bavard:
                        print("20 coups refuses d'affilee : partie abandonnee.")
                    self.nuls += 1
                    self.parties_jouees += 1
                    return None
                if self.bavard:
                    print(f"Coup refuse : {raison}. {joueur.nom} rejoue.")
                continue

            refus = 0  # le coup etait bon, on remet le compteur a zero

            x, y = coup
            grille.jouer(x, y, symbole)

            # Est-ce que ce coup fait gagner ?
            if grille.est_gagnant(symbole):
                self.scores[symbole] += 1
                self.parties_jouees += 1
                if self.bavard:
                    print()
                    grille.afficher()
                    print(f"{joueur.nom} ({symbole}) gagne la partie !")
                return symbole

            # Sinon, la grille est-elle pleine ? Alors match nul.
            if grille.est_plein():
                self.nuls += 1
                self.parties_jouees += 1
                if self.bavard:
                    print()
                    grille.afficher()
                    print("Match nul : plus aucune case libre.")
                return None

            tour += 1  # au joueur suivant

    # ------------------------------------------------------------------

    def jouer_series(self, nombre_de_parties=1):
        """Joue plusieurs parties et tient le score (bonus du TP)."""
        for numero in range(1, nombre_de_parties + 1):
            if self.bavard:
                print(f"\n===== Partie {numero} sur {nombre_de_parties} =====")
            self.jouer_partie()
        self.afficher_score()
        return self.scores

    def afficher_score(self):
        """Affiche le score final, avec les vrais noms des joueurs."""
        print("\n----- SCORE -----")
        print(f"{self.joueur_x.nom} (X) : {self.scores['X']} victoire(s)")
        print(f"{self.joueur_o.nom} (O) : {self.scores['O']} victoire(s)")
        print(f"Matchs nuls        : {self.nuls}")
        print(f"Parties jouees     : {self.parties_jouees}")
        print("-----------------")
