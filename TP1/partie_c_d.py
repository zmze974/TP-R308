# PARTIES C et D : Manipulation et Pendu

import random

# Choisit un mot au hasard dans la liste
def choisir_mot(liste_mots):
    return random.choice(liste_mots).upper()

# Crée le masque avec des "_"
def creer_masque(mot):
    return ["_"] * len(mot)

# Jeu du pendu avec 7 erreurs maximum
def jouer_pendu():

    # Liste des mots possibles
    mots_possibles = ["PYTHON", "CLAVIER", "RESEAU", "PROGRAMME"]

    # Préparation du jeu
    mot_secret = choisir_mot(mots_possibles)
    masque = creer_masque(mot_secret)

    erreurs = 0
    erreurs_max = 7
    lettres_tentees = []

    print("--- DEBUT DU PENDU ---")

    # Boucle principale du jeu
    while "_" in masque and erreurs < erreurs_max:

        # Affichage des informations de la partie
        print("\nMot :", " ".join(masque))
        print(f"Erreurs : {erreurs}/{erreurs_max}")
        print("Lettres proposées :", lettres_tentees)

        # Saisie du joueur
        lettre = input("Propose une lettre : ").strip().upper()

        # Vérifie que l'utilisateur saisit une seule lettre
        if len(lettre) != 1 or not lettre.isalpha():
            print("Veuillez entrer une seule lettre.")
            continue

        # Vérifie si la lettre a déjà été proposée
        if lettre in lettres_tentees:
            print("Lettre déjà proposée.")
            continue

        # Ajout de la lettre dans l'historique
        lettres_tentees.append(lettre)

        # Si la lettre est présente dans le mot
        if lettre in mot_secret:
            print("Bonne lettre !")

            # Révélation des positions de la lettre
            for i in range(len(mot_secret)):
                if mot_secret[i] == lettre:
                    masque[i] = lettre

        # Si la lettre n'est pas dans le mot
        else:
            print("Mauvaise lettre.")
            erreurs += 1

    # Fin de partie : victoire ou défaite
    if "_" not in masque:
        print(f"\nGagné ! Le mot était {mot_secret}.")
    else:
        print(f"\nPerdu ! Le mot était {mot_secret}.")

# Zone de test
if __name__ == "__main__":
    jouer_pendu()