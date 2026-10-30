"""
TP2 - Le programme a lancer : python3 main.py

C'est le menu. Il sert a choisir QUI joue contre QUI, et combien de parties.
Tout le reste du travail est deja fait dans grille.py, joueurs.py et jeu.py.
"""

from jeu import Jeu
from joueurs import JoueurHumain, JoueurIA, JoueurIAMalin


def demander_nombre_de_parties():
    """Demande combien de parties on veut jouer (1 par defaut)."""
    reponse = input("Combien de parties ? (Entree = 1) : ").strip()
    if reponse == "":
        return 1
    try:
        nombre = int(reponse)
        if nombre < 1:
            return 1
        return nombre
    except ValueError:
        return 1


def main():
    print("==============================")
    print("   MORPION - TP2 R3.08")
    print("==============================")
    print("1. Deux joueurs (humain contre humain)")
    print("2. Moi contre l'ordinateur (IA au hasard)")
    print("3. Ordinateur contre ordinateur")
    print("4. Moi contre l'ordinateur qui bloque (IA maligne)")
    print("5. IA au hasard contre IA maligne")
    print()

    choix = input("Ton choix (1 a 5) : ").strip()

    if choix == "1":
        joueur_x = JoueurHumain("Joueur 1")
        joueur_o = JoueurHumain("Joueur 2")
    elif choix == "2":
        joueur_x = JoueurHumain("Toi")
        joueur_o = JoueurIA("Ordinateur")
    elif choix == "3":
        joueur_x = JoueurIA("Ordinateur 1")
        joueur_o = JoueurIA("Ordinateur 2")
    elif choix == "4":
        joueur_x = JoueurHumain("Toi")
        joueur_o = JoueurIAMalin("Ordinateur malin")
    elif choix == "5":
        joueur_x = JoueurIA("Ordinateur au hasard")
        joueur_o = JoueurIAMalin("Ordinateur malin")
    else:
        print("Choix inconnu, on lance 'toi contre l'ordinateur' par defaut.")
        joueur_x = JoueurHumain("Toi")
        joueur_o = JoueurIA("Ordinateur")

    nombre = demander_nombre_de_parties()

    jeu = Jeu(joueur_x, joueur_o)

    # Si on joue beaucoup de parties d'ordinateur contre ordinateur,
    # afficher chaque grille rendrait le terminal illisible : on se tait.
    if nombre > 3 and not isinstance(joueur_x, JoueurHumain) and not isinstance(joueur_o, JoueurHumain):
        jeu.bavard = False

    jeu.jouer_series(nombre)


if __name__ == "__main__":
    main()
