import random

def jouer_devinette():
    secret = random.randint(1, 100)
    essais_max = 10
    essais = 0

    print("J'ai choisi un nombre entre 1 et 100. À toi de jouer !")

    while essais < essais_max:
        try:
            choix = int(input(f"Essai {essais + 1}/{essais_max} : "))
            essais += 1

            if choix < secret:
                print("Trop petit !")
            elif choix > secret:
                print("Trop grand !")
            else:
                print("Gagné !")
                return

        except ValueError:
            print("Veuillez entrer un nombre valide.")

    print(f"Perdu ! Le nombre était {secret}.")