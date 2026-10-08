# PARTIE B : Devine le nombre

import random

def jouer_devinette():

    # Génère un nombre aléatoire entre 1 et 100
    secret = random.randint(1, 100)

    # Limite le nombre d'essais à 10
    essais_max = 10
    essais = 0

    print("J'ai choisi un nombre entre 1 et 100.")

    # Boucle principale du jeu
    while essais < essais_max:

        try:
            # Demande un nombre au joueur
            choix = int(input(f"Essai {essais + 1}/{essais_max} : "))
            essais += 1

            # Compare la valeur proposée au nombre secret
            if choix < secret:
                print("Trop petit !")

            elif choix > secret:
                print("Trop grand !")

            else:
                print("Gagné !")
                return

        # Gestion d'une saisie incorrecte
        except ValueError:
            print("Veuillez entrer un nombre entier.")

    # Le joueur n'a pas trouvé après 10 essais
    print(f"Perdu ! Le nombre était {secret}.")

# Zone de test
if __name__ == "__main__":
    jouer_devinette()