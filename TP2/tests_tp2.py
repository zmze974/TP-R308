"""
TP2 - Les jeux d'essai du sujet, verifies automatiquement.

Lance-le avec :  python3 tests_tp2.py
Chaque ligne affiche OK ou ECHEC. A la fin, tu vois le total.
"""

from grille import Grille, VIDE
from joueurs import JoueurIA, JoueurIAMalin
from jeu import Jeu


reussis = 0
rates = 0


def verifier(nom_du_test, resultat, attendu):
    """Compare ce qu'on obtient avec ce que l'enonce demande."""
    global reussis, rates
    if resultat == attendu:
        reussis += 1
        print(f"OK    {nom_du_test}")
    else:
        rates += 1
        print(f"ECHEC {nom_du_test}  -> obtenu {resultat!r}, attendu {attendu!r}")


# ----------------------------------------------------------------------
# PARTIE A
# ----------------------------------------------------------------------
print("\n=== Partie A : la grille ===")

g = Grille()
verifier("grille vide au depart", g.cases, [[VIDE] * 3 for _ in range(3)])

g.jouer(0, 0, "X")
g.jouer(0, 1, "O")
g.jouer(1, 1, "X")
print("Affichage attendu par l'enonce :")
g.afficher()

verifier("case occupee refusee", g.jouer(0, 0, "O"), False)
verifier("case hors grille refusee", g.jouer(3, 0, "O"), False)
verifier("case negative refusee", g.jouer(-1, 0, "O"), False)
verifier("X pas encore gagnant", g.est_gagnant("X"), False)

g.jouer(2, 2, "X")
verifier("X gagne avec la diagonale", g.est_gagnant("X"), True)

# Grille pleine sans gagnant ? On remplit un plateau de match nul.
nul = Grille()
for (x, y, s) in [
    (0, 0, "X"), (0, 1, "O"), (0, 2, "X"),
    (1, 0, "X"), (1, 1, "O"), (1, 2, "O"),
    (2, 0, "O"), (2, 1, "X"), (2, 2, "X"),
]:
    nul.jouer(x, y, s)
verifier("grille pleine detectee", nul.est_plein(), True)
verifier("aucun gagnant sur cette grille", nul.est_gagnant("X"), False)

verifier("grille vide n'est pas pleine", Grille().est_plein(), False)


# ----------------------------------------------------------------------
# BONUS 1 : l'IA qui bloque
# ----------------------------------------------------------------------
print("\n=== Bonus : l'IA qui bloque ===")

grille_test = Grille()
grille_test.jouer(0, 0, "X")
grille_test.jouer(0, 1, "X")  # X menace la case (0, 2)
grille_test.jouer(1, 1, "O")
coup = JoueurIAMalin("IA").prochain_coup(grille_test, "O")
verifier("l'IA bloque X en (0, 2)", coup, (0, 2))

grille_test2 = Grille()
grille_test2.jouer(0, 0, "O")
grille_test2.jouer(0, 1, "O")  # O peut gagner en (0, 2)
grille_test2.jouer(1, 0, "X")
grille_test2.jouer(1, 1, "X")
coup = JoueurIAMalin("IA").prochain_coup(grille_test2, "O")
verifier("l'IA gagne en (0, 2) au lieu de bloquer", coup, (0, 2))


# ----------------------------------------------------------------------
# PARTIE C : 20 parties IA contre IA, et l'IA maligne face a l'IA au hasard
# ----------------------------------------------------------------------
print("\n=== Partie C : 20 parties ordinateur contre ordinateur ===")

jeu = Jeu(JoueurIA("IA 1"), JoueurIA("IA 2"), bavard=False)
for _ in range(20):
    resultat = jeu.jouer_partie()
    if resultat not in ("X", "O", None):
        verifier("resultat de partie valide", resultat, "X, O ou None")
        break

verifier("20 parties jouees", jeu.parties_jouees, 20)
verifier("victoires + nuls = 20", jeu.scores["X"] + jeu.scores["O"] + jeu.nuls, 20)
print(f"      detail : X {jeu.scores['X']} victoire(s), O {jeu.scores['O']} victoire(s), "
      f"{jeu.nuls} nul(s)")

print("\n=== 20 parties IA maligne (O) contre IA au hasard (X) ===")

jeu2 = Jeu(JoueurIA("IA au hasard"), JoueurIAMalin("IA maligne"), bavard=False)
resultats = [jeu2.jouer_partie() for _ in range(20)]
print(f"      detail : IA au hasard {jeu2.scores['X']} victoire(s), "
      f"IA maligne {jeu2.scores['O']} victoire(s), {jeu2.nuls} nul(s)")
verifier("20 parties terminees par une victoire ou un nul",
         all(r in ("X", "O", None) for r in resultats), True)
# L'IA "maligne" gagne quand elle peut et bloque sinon, mais elle joue au
# hasard le reste du temps : elle peut donc perdre contre un coup fourbe.
# L'enonce ne demande pas qu'elle soit imbattable, juste qu'elle bloque.
verifier("l'IA maligne gagne plus souvent qu'elle ne perd",
         jeu2.scores["O"] > jeu2.scores["X"], True)


# ----------------------------------------------------------------------
# Le defi du formateur : coups pourris sans plantage
# ----------------------------------------------------------------------
print("\n=== Defi : coups bizarres, aucun plantage ===")


class JoueurFautif:
    """Un faux joueur qui envoie exprès des coups invalides."""

    def __init__(self, nom, coups):
        self.nom = nom
        self.coups = list(coups)

    def prochain_coup(self, grille, symbole):
        # Il envoie ses coups pourris un par un...
        if len(self.coups) > 1:
            return self.coups.pop(0)
        # ...puis, pour ne pas bloquer le jeu a l'infini, il finit par
        # jouer normalement dans une case libre.
        for x in range(3):
            for y in range(3):
                if grille.est_libre(x, y):
                    return (x, y)
        return (0, 0)


fautif = JoueurFautif("Fautif", [(0, 0), (0, 0), (3, 0), (-1, -1), (0, 1), (1, 1), (2, 2)])
jeu3 = Jeu(fautif, JoueurIA("IA"), bavard=False)
resultat = jeu3.jouer_partie()
verifier("partie terminee malgre les coups invalides", resultat in ("X", "O", None), True)

mauvais = JoueurFautif("Mauvais", [("a", "b")])
jeu4 = Jeu(mauvais, JoueurIA("IA"), bavard=False)
grille_vide = Grille()
verifier("coup non numerique refuse", jeu4._verifier(grille_vide, ("a", "b"))[0], False)
verifier("coup pas en couple refuse", jeu4._verifier(grille_vide, 3)[0], False)


class JoueurBloque:
    """Un joueur qui renvoie TOUJOURS le meme coup deja pris."""

    nom = "Bloque"

    def prochain_coup(self, grille, symbole):
        return (0, 0)


jeu5 = Jeu(JoueurBloque(), JoueurIA("IA"), bavard=False)
jeu5.jouer_partie()
# X joue (0,0), puis n'envoie plus que (0,0) : au bout de 20 refus, on coupe.
verifier("un joueur qui boucle est coupe (pas de blocage infini)",
         jeu5.parties_jouees, 1)


# ----------------------------------------------------------------------
print("\n==============================")
print(f"Resultat : {reussis} OK, {rates} ECHEC")
print("==============================\n")
