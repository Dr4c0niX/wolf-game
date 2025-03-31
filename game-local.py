import random
import os

LIGNES = 5  
COLONNES = 5  
NOMBRE_OBSTACLES = 3  

# Rôle
while True:
    role = input("Choisissez votre rôle (loup / villageois) : ").strip().lower()
    if role in ["loup", "villageois"]:
        break
    print("Veuillez entrer 'loup' ou 'villageois'.")

# Position aléatoire
def position_aleatoire(exclusions):
    while True:
        pos = (random.randint(0, LIGNES - 1), random.randint(0, COLONNES - 1))
        if pos not in exclusions:
            return pos

# Initialisation positions
occupied_positions = set()

joueur_x, joueur_y = position_aleatoire(occupied_positions)
occupied_positions.add((joueur_x, joueur_y))

pnj_x, pnj_y = position_aleatoire(occupied_positions)
occupied_positions.add((pnj_x, pnj_y))

obstacles = []
for _ in range(NOMBRE_OBSTACLES):
    obs_x, obs_y = position_aleatoire(occupied_positions)
    obstacles.append((obs_x, obs_y))
    occupied_positions.add((obs_x, obs_y))

# Affichage plateau avec vision loup + obstacles
def afficher_plateau():
    os.system("cls" if os.name == "nt" else "clear")  
    print("Plateau jeu :")
    for i in range(LIGNES):
        for j in range(COLONNES):
            if (i, j) == (joueur_x, joueur_y):
                print("🐺" if role == "loup" else "🙂", end=" ") 
            elif (i, j) == (pnj_x, pnj_y):
                if role == "loup": 
                    distance_x = abs(joueur_x - pnj_x)
                    distance_y = abs(joueur_y - pnj_y)
                    if distance_x <= 1 and distance_y <= 1:
                        print("🙂", end=" ")  
                    else:
                        print("⬜", end=" ")  
                else:
                    print("🐺", end=" ")  
            elif (i, j) in obstacles:
                print("🧱", end=" ")  
            else:
                print("⬜", end=" ")  
        print()
    print()

    # Affichage vision loup
    if role == "loup":
        print("Vision du loup :")
        vois_villageois = False
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            if (joueur_x + dx, joueur_y + dy) == (pnj_x, pnj_y):
                vois_villageois = True
        if vois_villageois:
            print("Le villageois est **à une case de vous** !")
        else:
            print("Aucun villageois à proximité.")

# Début jeu
print("\n Début du jeu !")
while True:
    afficher_plateau()

    # Vérif victoire / défaite
    if (joueur_x, joueur_y) == (pnj_x, pnj_y):
        if role == "loup":
            print("Victoire loup !")
        else:
            print("Défaite villageois !")
        break

    # Déplacement joueur
    mouvement = input("Déplacez-vous (z=haut, s=bas, q=gauche, d=droite, entrer pour passer) : ").strip().lower()

    nouveau_x, nouveau_y = joueur_x, joueur_y 

    if mouvement == "z" and joueur_x > 0:
        nouveau_x -= 1
    elif mouvement == "s" and joueur_x < LIGNES - 1:
        nouveau_x += 1
    elif mouvement == "q" and joueur_y > 0:
        nouveau_y -= 1
    elif mouvement == "d" and joueur_y < COLONNES - 1:
        nouveau_y += 1
    elif mouvement == "":
        print("Tour passé.")
    else:
        print("Déplacement invalide.")

    # Vérif si la case cible contient un obstacle
    if (nouveau_x, nouveau_y) in obstacles:
        print(" Déplacement impossible !")
    else:
        joueur_x, joueur_y = nouveau_x, nouveau_y  

print("Fin du jeu !")


