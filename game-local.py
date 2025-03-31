import random
import os
import time
import sys

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def position_aleatoire(lignes, colonnes, exclusions):
    while True:
        pos = (random.randint(0, lignes - 1), random.randint(0, colonnes - 1))
        if pos not in exclusions:
            return pos

def jouer(role, lignes, colonnes, nombre_obstacles, limite_tour, tours_max=100):
    # Utilisez tours_max comme limite pour le nombre de tours
    # Le reste de la fonction reste inchangé
    # Initialisation positions
    occupied_positions = set()
    
    joueur_x, joueur_y = position_aleatoire(lignes, colonnes, occupied_positions)
    occupied_positions.add((joueur_x, joueur_y))
    
    pnj_x, pnj_y = position_aleatoire(lignes, colonnes, occupied_positions)
    occupied_positions.add((pnj_x, pnj_y))
    
    # Création des obstacles
    obstacles = []
    for _ in range(nombre_obstacles):
        obs_x, obs_y = position_aleatoire(lignes, colonnes, occupied_positions)
        obstacles.append((obs_x, obs_y))
        occupied_positions.add((obs_x, obs_y))
    
    # Compteur de tours et temps
    num_tour = 1
    
    def afficher_plateau(temps_restant=0):
        clear_screen()
        print("\n" + "=" * 60)
        if role == "loup":
            print("                  VOUS ÊTES LE LOUP")
        else:
            print("                VOUS ÊTES UN VILLAGEOIS")
        print("=" * 60 + "\n")
        
        # Afficher à la fois le tour et le temps restant
        print(f"Tour: {num_tour}   Temps restant: {temps_restant}s")
        print("\nPlateau jeu:")
        
        # Bordure supérieure
        print("   " + "".join(f" {j} " for j in range(colonnes)))
        print("  +" + "-" * (colonnes * 3) + "+")
        
        for i in range(lignes):
            print(f"{i} |", end="")
            for j in range(colonnes):
                if (i, j) == (joueur_x, joueur_y):
                    print(" 🐺 " if role == "loup" else " 🙂 ", end="")
                elif (i, j) == (pnj_x, pnj_y):
                    if role == "loup": 
                        distance_x = abs(joueur_x - pnj_x)
                        distance_y = abs(joueur_y - pnj_y)
                        est_visible = distance_x <= 1 and distance_y <= 1 and not (distance_x == 1 and distance_y == 1)
                        if est_visible:
                            print(" 🙂 ", end="")
                        else:
                            print(" ⬜ ", end="")
                    else:
                        print(" 🐺 ", end="")
                elif (i, j) in obstacles:
                    print(" 🧱 ", end="")
                else:
                    print(" ⬜ ", end="")
            print("|")
        
        # Bordure inférieure
        print("  +" + "-" * (colonnes * 3) + "+")
        print()
        
        # Affichage vision du loup
        if role == "loup":
            print("Vision du loup:")
            vois_villageois = False
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                new_x, new_y = joueur_x + dx, joueur_y + dy
                if 0 <= new_x < lignes and 0 <= new_y < colonnes:
                    if (new_x, new_y) == (pnj_x, pnj_y):
                        vois_villageois = True
            
            if vois_villageois:
                print("Le villageois est à une case de vous !")
            else:
                print("Aucun villageois à proximité.")
        print()
    
    # Début jeu
    print("\nDébut du jeu !")
    
    # Boucle principale du jeu
    while True:
        # Affichage initial du plateau avec le temps complet
        temps_restant = limite_tour
        afficher_plateau(temps_restant)
        
        # Vérification du nombre maximum de tours
        if num_tour > tours_max:
            if role == "loup":
                print("\n❌ Défaite ! Vous n'avez pas réussi à attraper le villageois à temps.")
            else:
                print("\n🏆 Victoire ! Vous avez survécu jusqu'à la fin du jeu !")
            break
        
        # Vérif victoire / défaite
        if (joueur_x, joueur_y) == (pnj_x, pnj_y):
            if role == "loup":
                print("\n🎮 Victoire ! Vous avez attrapé le villageois ! 🏆")
            else:
                print("\n☠️ Défaite ! Vous avez été mangé par le loup ! ☠️")
            break
        
        # Gestion du temps pour le tour
        start_time = time.time()
        print(f"Déplacez-vous (z=haut, s=bas, q=gauche, d=gauche, entrer pour passer)")
        print("Appuyez sur 'x' pour quitter le jeu")
        
        mouvement = None
        last_update = start_time  # Pour suivre la dernière fois que nous avons mis à jour l'affichage
        
        # Boucle de détection des touches avec mise à jour du temps
        while temps_restant > 0 and mouvement is None:
            # Mise à jour du temps restant
            current_time = time.time()
            elapsed = current_time - start_time
            temps_restant = max(0, limite_tour - int(elapsed))
            
            # Réafficher le plateau à chaque seconde pour voir le temps restant précisément
            if int(current_time - last_update) >= 1:  # Mise à jour chaque seconde au lieu de toutes les 5 secondes
                last_update = current_time
                afficher_plateau(temps_restant)
                print(f"Déplacez-vous (z=haut, s=bas, q=gauche, d=droite, entrer pour passer)")
                print("Appuyez sur 'x' pour quitter le jeu")
            
            # Détection des touches - amélioré pour être plus réactif
            if os.name == 'nt':  # Pour Windows
                import msvcrt
                if msvcrt.kbhit():
                    key = msvcrt.getch().decode('utf-8').lower()
                    if key in ['z', 's', 'q', 'd', '', 'x']:
                        mouvement = key
                        break
            else:  # Pour Unix/Linux
                import select
                i, o, e = select.select([sys.stdin], [], [], 0.1)
                if i:
                    key = sys.stdin.readline().strip().lower()
                    if key in ['z', 's', 'q', 'd', '', 'x']:
                        mouvement = key
                        break
            
            # Petite pause pour éviter d'utiliser 100% du CPU
            time.sleep(0.1)
        
        # Si le temps est écoulé
        if temps_restant <= 0 or mouvement is None:
            print("\nTemps écoulé ! Vous passez votre tour.")
            time.sleep(1)
            num_tour += 1
            continue
        
        # Gestion de la touche 'x' pour quitter
        if mouvement == 'x':
            if input("\nVoulez-vous vraiment quitter la partie ? (o/n): ").lower() == 'o':
                return
            else:
                # Continuer le jeu si l'utilisateur ne veut pas quitter
                continue
        
        # Calcul du nouveau mouvement
        nouveau_x, nouveau_y = joueur_x, joueur_y
        
        if mouvement == "z" and joueur_x > 0:
            nouveau_x -= 1
        elif mouvement == "s" and joueur_x < lignes - 1:
            nouveau_x += 1
        elif mouvement == "q" and joueur_y > 0:
            nouveau_y -= 1
        elif mouvement == "d" and joueur_y < colonnes - 1:
            nouveau_y += 1
        elif mouvement == "":
            print("\nVous passez votre tour.")
            num_tour += 1
            time.sleep(1)
            continue
        else:
            print("\nDéplacement invalide.")
            time.sleep(1)
            continue
        
        # Vérif si la case cible contient un obstacle
        if (nouveau_x, nouveau_y) in obstacles:
            print("\nDéplacement impossible ! Il y a un obstacle.")
            time.sleep(1)
        else:
            joueur_x, joueur_y = nouveau_x, nouveau_y
            num_tour += 1
            
            # Vérification immédiate si le joueur a gagné après le mouvement
            if (joueur_x, joueur_y) == (pnj_x, pnj_y):
                afficher_plateau(temps_restant)
                if role == "loup":
                    print("\n🎮 Victoire ! Vous avez attrapé le villageois ! 🏆")
                else:
                    print("\n☠️ Défaite ! Vous avez été mangé par le loup ! ☠️")
                break

def main():
    # Vérifier si des paramètres ont été passés via les variables d'environnement
    role_from_env = os.environ.get('PLAYER_ROLE')
    player_name = os.environ.get('PLAYER_NAME')
    
    # Si des paramètres sont fournis, lancer directement le jeu
    if role_from_env:
        if role_from_env == "villageois" or role_from_env == "loup-garou":
            # Récupérer les paramètres de configuration
            lignes = int(os.environ.get('GRID_ROWS', 5))
            colonnes = int(os.environ.get('GRID_COLS', 5))
            nombre_obstacles = int(os.environ.get('OBSTACLES', 3))
            limite_tour = int(os.environ.get('TURN_DURATION', 30))
            tours_max = int(os.environ.get('MAX_TURNS', 100))
            
            # Convertir loup-garou en loup pour compatibilité
            actual_role = "villageois" if role_from_env == "villageois" else "loup"
            
            # Lancer le jeu avec les paramètres configurés
            print(f"Lancement du jeu pour {player_name} en tant que {actual_role}")
            print(f"Configuration: Plateau {lignes}×{colonnes}, {nombre_obstacles} obstacles, {limite_tour}s par tour, max {tours_max} tours")
            jouer(actual_role, lignes, colonnes, nombre_obstacles, limite_tour, tours_max)
            return

if __name__ == "__main__":
    main()