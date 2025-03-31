import tkinter as tk
from tkinter import messagebox, ttk
import tkinter.font as tkFont
import random
import os
import time
import sys
import threading

class ConfigJeuTk:
    """Fenêtre de configuration du jeu"""
    def __init__(self, master):
        self.master = master
        self.master.title("Configuration de la partie - Loup-Garou")
        self.master.geometry("500x500")
        self.master.configure(bg="#2E2E2E")
        
        # Récupérer les paramètres de l'environnement
        self.role = os.environ.get('PLAYER_ROLE', "villageois")
        if self.role == "loup-garou":
            self.role = "loup"  # Convertir pour compatibilité
        self.player_name = os.environ.get('PLAYER_NAME', "Joueur")
        
        # Valeurs par défaut
        self.lignes = 10
        self.colonnes = 10
        self.nombre_obstacles = 5
        self.duree_tour = 30  # secondes
        self.nombre_tours_max = 100
        
        self.config_ok = False
        
        # Police et style
        self.font = tkFont.Font(family="Helvetica", size=12)
        self.title_font = tkFont.Font(family="Helvetica", size=14, weight="bold")
        
        # Création de l'interface
        self.create_widgets()
        
    def create_widgets(self):
        # Frame principale
        main_frame = tk.Frame(self.master, bg="#2E2E2E", padx=20, pady=20)
        main_frame.pack(fill="both", expand=True)
        
        # Titre
        title = tk.Label(main_frame, text="Configuration de la partie",
                      font=self.title_font, bg="#2E2E2E", fg="white")
        title.pack(pady=(0, 20))
        
        # Informations sur le joueur
        info_frame = tk.Frame(main_frame, bg="#2E2E2E", pady=10)
        info_frame.pack(fill="x")
        
        tk.Label(info_frame, text=f"Joueur: {self.player_name}",
               font=self.font, bg="#2E2E2E", fg="white").pack(anchor="w")
        tk.Label(info_frame, text=f"Rôle: {'Villageois' if self.role == 'villageois' else 'Loup'}",
               font=self.font, bg="#2E2E2E", fg="white").pack(anchor="w")
        
        # Séparateur
        separator = tk.Frame(main_frame, height=2, bg="#555555")
        separator.pack(fill="x", pady=10)
        
        # Frame pour les paramètres
        param_frame = tk.Frame(main_frame, bg="#2E2E2E")
        param_frame.pack(fill="both", expand=True, pady=10)
        
        # Taille du plateau (lignes x colonnes)
        tk.Label(param_frame, text="Taille du plateau:", 
                font=self.font, bg="#2E2E2E", fg="white").grid(row=0, column=0, sticky="w", pady=5)
        
        size_frame = tk.Frame(param_frame, bg="#2E2E2E")
        size_frame.grid(row=0, column=1, sticky="w", pady=5)
        
        self.lignes_var = tk.IntVar(value=self.lignes)
        self.cols_var = tk.IntVar(value=self.colonnes)
        
        tk.Label(size_frame, text="Lignes:", bg="#2E2E2E", fg="white").pack(side="left")
        rows_spinbox = tk.Spinbox(size_frame, from_=5, to=20, width=5, 
                                textvariable=self.lignes_var, bg="#404040", fg="white")
        rows_spinbox.pack(side="left", padx=(5, 15))
        
        tk.Label(size_frame, text="Colonnes:", bg="#2E2E2E", fg="white").pack(side="left")
        cols_spinbox = tk.Spinbox(size_frame, from_=5, to=20, width=5,
                                textvariable=self.cols_var, bg="#404040", fg="white")
        cols_spinbox.pack(side="left", padx=5)
        
        # Nombre d'obstacles
        tk.Label(param_frame, text="Nombre d'obstacles:",
                font=self.font, bg="#2E2E2E", fg="white").grid(row=1, column=0, sticky="w", pady=5)
        
        self.obstacles_var = tk.IntVar(value=self.nombre_obstacles)
        obstacles_spinbox = tk.Spinbox(param_frame, from_=0, to=50, width=5, 
                                     textvariable=self.obstacles_var, bg="#404040", fg="white")
        obstacles_spinbox.grid(row=1, column=1, sticky="w", pady=5)
        
        # Durée d'un tour (secondes)
        tk.Label(param_frame, text="Durée d'un tour (secondes):",
                font=self.font, bg="#2E2E2E", fg="white").grid(row=2, column=0, sticky="w", pady=5)
        
        self.duree_var = tk.IntVar(value=self.duree_tour)
        duree_spinbox = tk.Spinbox(param_frame, from_=5, to=120, width=5, 
                                  textvariable=self.duree_var, bg="#404040", fg="white")
        duree_spinbox.grid(row=2, column=1, sticky="w", pady=5)
        
        # Nombre de tours maximum
        tk.Label(param_frame, text="Nombre de tours maximum:",
                font=self.font, bg="#2E2E2E", fg="white").grid(row=3, column=0, sticky="w", pady=5)
        
        self.tours_max_var = tk.IntVar(value=self.nombre_tours_max)
        tours_spinbox = tk.Spinbox(param_frame, from_=10, to=500, width=5, 
                                  textvariable=self.tours_max_var, bg="#404040", fg="white")
        tours_spinbox.grid(row=3, column=1, sticky="w", pady=5)
        
        # Boutons
        buttons_frame = tk.Frame(main_frame, bg="#2E2E2E")
        buttons_frame.pack(pady=20)
        
        start_btn = tk.Button(buttons_frame, text="Commencer la partie", 
                             font=self.font, bg="#3498db", fg="white",
                             activebackground="#2980b9", activeforeground="white",
                             command=self.lancer_jeu, padx=20, pady=10)
        start_btn.pack(side="left", padx=10)
        
        cancel_btn = tk.Button(buttons_frame, text="Annuler", 
                              font=self.font, bg="#e74c3c", fg="white",
                              activebackground="#c0392b", activeforeground="white",
                              command=self.annuler, padx=20, pady=10)
        cancel_btn.pack(side="left", padx=10)
    
    def lancer_jeu(self):
        """Récupère les paramètres et lance le jeu"""
        # Vérification des valeurs saisies
        if not (5 <= self.lignes_var.get() <= 20 and 5 <= self.cols_var.get() <= 20):
            messagebox.showwarning("Taille de plateau invalide", 
                                  "La taille du plateau doit être entre 5x5 et 20x20.")
            return
        
        max_obstacles = (self.lignes_var.get() * self.cols_var.get()) // 3
        if self.obstacles_var.get() > max_obstacles:
            messagebox.showwarning("Trop d'obstacles", 
                                 f"Le nombre maximum d'obstacles pour cette taille de plateau est {max_obstacles}.")
            self.obstacles_var.set(max_obstacles)
            return
        
        # Récupération des paramètres
        self.lignes = self.lignes_var.get()
        self.colonnes = self.cols_var.get()
        self.nombre_obstacles = self.obstacles_var.get()
        self.duree_tour = self.duree_var.get()
        self.nombre_tours_max = self.tours_max_var.get()
        
        self.config_ok = True
        self.master.destroy()
    
    def annuler(self):
        """Annule et ferme la fenêtre"""
        self.config_ok = False
        self.master.destroy()

class WolfGameTk:
    def __init__(self, root, config):
        self.root = root
        self.root.title("Jeu du Loup-Garou - Mode Solo")
        self.root.geometry("800x600")
        
        # Paramètres du jeu depuis la configuration
        self.role = config['role']
        self.player_name = config['player_name']
        self.lignes = config['lignes']
        self.colonnes = config['colonnes']
        self.nombre_obstacles = config['nombre_obstacles']
        self.tour_limite = config['nombre_tours_max']  # Nombre de tours max
        self.duree_tour = config['duree_tour']  # Durée d'un tour en secondes
        self.num_tour = 1
        
        # Initialiser les attributs pour le timer AVANT de créer l'interface
        self.temps_restant = self.duree_tour  # Durée initiale
        self.timer_id = None  # Pour stocker la référence au timer
        
        # Couleurs et style
        self.BACKGROUND_COLOR = "#2E2E2E"
        self.TEXT_COLOR = "#FFFFFF"
        self.CELL_EMPTY = "#505050"
        self.CELL_OBSTACLE = "#8B4513"
        self.CELL_PLAYER = "#3498db" if self.role == "villageois" else "#e74c3c"
        self.CELL_PNJ = "#e74c3c" if self.role == "villageois" else "#3498db"
        
        self.root.configure(bg=self.BACKGROUND_COLOR)
        self.font = tkFont.Font(family="Helvetica", size=12)
        
        # Initialiser les positions
        self.initialiser_jeu()
        
        # Créer l'interface
        self.creer_interface()
        
        # Lier les touches du clavier
        self.root.bind("<KeyPress>", self.gerer_touche)
        
        # Message de bienvenue
        messagebox.showinfo("Jeu du Loup-Garou", 
                            f"Bienvenue {self.player_name} !\n"
                            f"Vous jouez le rôle de {'Villageois' if self.role == 'villageois' else 'Loup'}.\n\n"
                            "Utilisez les touches fléchées ou ZQSD pour vous déplacer.")
        self.root.focus_force()  # Force le focus sur la fenêtre principale
            
    def initialiser_jeu(self):
        """Initialise les positions des joueurs et obstacles"""
        occupied_positions = set()
        
        # Position du joueur
        self.joueur_x = random.randint(0, self.lignes - 1)
        self.joueur_y = random.randint(0, self.colonnes - 1)
        occupied_positions.add((self.joueur_x, self.joueur_y))
        
        # Position du PNJ
        while True:
            self.pnj_x = random.randint(0, self.lignes - 1)
            self.pnj_y = random.randint(0, self.colonnes - 1)
            if (self.pnj_x, self.pnj_y) not in occupied_positions:
                break
        occupied_positions.add((self.pnj_x, self.pnj_y))
        
        # Création des obstacles
        self.obstacles = []
        for _ in range(self.nombre_obstacles):
            while True:
                obs_x = random.randint(0, self.lignes - 1)
                obs_y = random.randint(0, self.colonnes - 1)
                if (obs_x, obs_y) not in occupied_positions:
                    self.obstacles.append((obs_x, obs_y))
                    occupied_positions.add((obs_x, obs_y))
                    break
    
    def creer_interface(self):
        """Crée l'interface graphique du jeu"""
        # Frame principale
        main_frame = tk.Frame(self.root, bg=self.BACKGROUND_COLOR)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Titre et info
        title_frame = tk.Frame(main_frame, bg=self.BACKGROUND_COLOR)
        title_frame.pack(fill="x", pady=10)
        
        role_text = "LOUP" if self.role == "loup" else "VILLAGEOIS"
        title_label = tk.Label(title_frame, 
                              text=f"Jeu du Loup-Garou - {self.player_name} - Vous êtes {role_text}",
                              font=tkFont.Font(family="Helvetica", size=16, weight="bold"),
                              bg=self.BACKGROUND_COLOR, fg=self.TEXT_COLOR)
        title_label.pack()
        
        self.info_label = tk.Label(title_frame, 
                                  text=f"Tour: {self.num_tour}/{self.tour_limite} | Temps: {self.temps_restant}s",
                                  font=self.font, bg=self.BACKGROUND_COLOR, fg=self.TEXT_COLOR)
        self.info_label.pack(pady=5)
        
        # Créer le plateau de jeu
        self.plateau_frame = tk.Frame(main_frame, bg=self.BACKGROUND_COLOR, bd=2, relief=tk.RIDGE)
        self.plateau_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Dimensionnement des cellules
        for i in range(self.lignes):
            self.plateau_frame.grid_rowconfigure(i, weight=1, minsize=30)
        for j in range(self.colonnes):
            self.plateau_frame.grid_columnconfigure(j, weight=1, minsize=30)
        
        # Créer les cellules du plateau avec les gestionnaires d'événements de clic
        self.cellules = {}
        for i in range(self.lignes):
            for j in range(self.colonnes):
                cell = tk.Frame(self.plateau_frame, bg=self.CELL_EMPTY, bd=1, relief=tk.RAISED)
                cell.grid(row=i, column=j, sticky="nsew", padx=1, pady=1)
                # Ajouter les coordonnées comme propriétés de la cellule
                cell.coord_x = i
                cell.coord_y = j
                # Ajouter le gestionnaire de clic
                cell.bind("<Button-1>", lambda e, x=i, y=j: self.gerer_clic(x, y))
                self.cellules[(i, j)] = cell
        
        # Reste du code de création d'interface...
        # ...
        
        # Mettre à jour l'affichage initial
        self.actualiser_plateau()
        
        # Liaisons de touches spécifiques pour garantir qu'elles sont détectées
        self.root.bind("z", self.gerer_touche)
        self.root.bind("Z", self.gerer_touche)
        self.root.bind("q", self.gerer_touche)
        self.root.bind("Q", self.gerer_touche)
        self.root.bind("s", self.gerer_touche)
        self.root.bind("S", self.gerer_touche)
        self.root.bind("d", self.gerer_touche)
        self.root.bind("D", self.gerer_touche)
        self.root.bind("<Up>", self.gerer_touche)
        self.root.bind("<Down>", self.gerer_touche)
        self.root.bind("<Left>", self.gerer_touche)
        self.root.bind("<Right>", self.gerer_touche)
        
        self.demarrer_timer()
    
    def actualiser_plateau(self):
        """Met à jour l'affichage du plateau"""
        for i in range(self.lignes):
            for j in range(self.colonnes):
                cell = self.cellules.get((i, j))
                if not cell:
                    continue
                
                # Par défaut: case vide
                cell.configure(bg=self.CELL_EMPTY)
                if cell.winfo_children():
                    for widget in cell.winfo_children():
                        widget.destroy()
                
                # Joueur
                if (i, j) == (self.joueur_x, self.joueur_y):
                    cell.configure(bg=self.CELL_PLAYER)
                    tk.Label(cell, text="🙂" if self.role == "villageois" else "🐺",
                            font=tkFont.Font(family="Segoe UI Emoji", size=14),
                            bg=self.CELL_PLAYER).pack(expand=True)
                
                # PNJ (adversaire)
                elif (i, j) == (self.pnj_x, self.pnj_y):
                    # Si loup, le villageois n'est visible que s'il est adjacent
                    if self.role == "loup":
                        distance_x = abs(self.joueur_x - self.pnj_x)
                        distance_y = abs(self.joueur_y - self.pnj_y)
                        est_visible = distance_x <= 1 and distance_y <= 1 and not (distance_x == 1 and distance_y == 1)
                        
                        if est_visible:
                            cell.configure(bg=self.CELL_PNJ)
                            tk.Label(cell, text="🙂",
                                    font=tkFont.Font(family="Segoe UI Emoji", size=14),
                                    bg=self.CELL_PNJ).pack(expand=True)
                    else:
                        # Le villageois voit toujours le loup
                        cell.configure(bg=self.CELL_PNJ)
                        tk.Label(cell, text="🐺",
                                font=tkFont.Font(family="Segoe UI Emoji", size=14),
                                bg=self.CELL_PNJ).pack(expand=True)
                
                # Obstacle
                elif (i, j) in self.obstacles:
                    cell.configure(bg=self.CELL_OBSTACLE)
                    tk.Label(cell, text="🧱",
                            font=tkFont.Font(family="Segoe UI Emoji", size=14),
                            bg=self.CELL_OBSTACLE).pack(expand=True)
                
                # Mise en évidence des cases adjacentes cliquables
                elif self.est_case_adjacente(i, j):
                    # Ajouter une légère surbrillance pour les cases adjacentes cliquables
                    cell.configure(bg="#606060")  # Une nuance légèrement plus claire
                    
                    # Ajouter un symbole de flèche indiquant une direction possible
                    direction = ""
                    if i < self.joueur_x:
                        direction = "↑"  # flèche vers le haut
                    elif i > self.joueur_x:
                        direction = "↓"  # flèche vers le bas
                    elif j < self.joueur_y:
                        direction = "←"  # flèche vers la gauche
                    elif j > self.joueur_y:
                        direction = "→"  # flèche vers la droite
                    
                    if direction:
                        tk.Label(cell, text=direction,
                                font=tkFont.Font(family="Helvetica", size=10),
                                bg="#606060", fg="#AAAAAA").pack(expand=True)
        
        # Mettre à jour le texte d'information avec le temps restant
        self.info_label.config(text=f"Tour: {self.num_tour}/{self.tour_limite} | Temps: {self.temps_restant}s")
        
        # Vision du loup (message) - Modifier pour inclure le temps
        if self.role == "loup":
            # Vérifier si le villageois est adjacent
            vois_villageois = False
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                new_x, new_y = self.joueur_x + dx, self.joueur_y + dy
                if 0 <= new_x < self.lignes and 0 <= new_y < self.colonnes:
                    if (new_x, new_y) == (self.pnj_x, self.pnj_y):
                        vois_villageois = True
            
            if vois_villageois:
                self.info_label.config(text=f"Tour: {self.num_tour}/{self.tour_limite} | Temps: {self.temps_restant}s - Le villageois est proche !")
    
    def demarrer_timer(self):
        """Démarre le compte à rebours pour le tour actuel"""
        if self.temps_restant > 0:
            self.temps_restant -= 1
            self.actualiser_plateau()  # Mettre à jour l'affichage
            self.timer_id = self.root.after(1000, self.demarrer_timer)  # Rappel après 1 seconde
        else:
            # Temps écoulé: passer au tour suivant automatiquement
            self.temps_restant = self.duree_tour  # Réinitialiser le temps
            self.num_tour += 1
            
            # Vérifier si le nombre maximum de tours est atteint
            if self.num_tour > self.tour_limite:
                self.actualiser_plateau()
                if self.role == "loup":
                    messagebox.showinfo("Défaite !", "Vous n'avez pas réussi à attraper le villageois à temps.")
                else:
                    messagebox.showinfo("Victoire !", "Vous avez survécu jusqu'à la fin du jeu !")
                self.quitter_jeu()
                return
            
            # Sinon, continuer le jeu
            self.actualiser_plateau()
            self.demarrer_timer()
    
    def gerer_touche(self, event):
        """Gère les entrées clavier pour les déplacements"""
        # Annuler le timer actuel pour éviter des rappels multiples
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
        
        # S'assurer que la fenêtre a le focus
        self.root.focus_set()
        
        # Récupérer le caractère et le code de touche
        key = event.keysym.lower()
        char = event.char.lower() if hasattr(event, 'char') else ''
        
        print(f"Touche pressée: {key}, Caractère: {char}, KeyCode: {event.keycode if hasattr(event, 'keycode') else 'N/A'}")
        
        nouveau_x, nouveau_y = self.joueur_x, self.joueur_y
        
        # Détection plus robuste des touches
        if key == 'z' or key == 'up' or char == 'z':
            nouveau_x -= 1
        elif key == 's' or key == 'down' or char == 's':
            nouveau_x += 1
        elif key == 'q' or key == 'left' or char == 'q':
            nouveau_y -= 1
        elif key == 'd' or key == 'right' or char == 'd':
            nouveau_y += 1
        else:
            # Redémarrer le timer et retourner sans rien faire
            self.demarrer_timer()
            return
        
        # Vérifier si le déplacement est valide
        if (0 <= nouveau_x < self.lignes and 
            0 <= nouveau_y < self.colonnes and 
            (nouveau_x, nouveau_y) not in self.obstacles):
            
            # Effectuer le déplacement
            self.joueur_x, self.joueur_y = nouveau_x, nouveau_y
            self.num_tour += 1
            
            # Vérifier la fin de partie
            if (self.joueur_x, self.joueur_y) == (self.pnj_x, self.pnj_y):
                self.actualiser_plateau()
                if self.role == "loup":
                    messagebox.showinfo("Victoire !", "Vous avez attrapé le villageois !")
                else:
                    messagebox.showinfo("Défaite !", "Vous avez été mangé par le loup !")
                self.quitter_jeu()
                return
            
            # Fin de partie par limite de tours
            if self.num_tour > self.tour_limite:
                self.actualiser_plateau()
                if self.role == "loup":
                    messagebox.showinfo("Défaite !", "Vous n'avez pas réussi à attraper le villageois à temps.")
                else:
                    messagebox.showinfo("Victoire !", "Vous avez survécu jusqu'à la fin du jeu !")
                self.quitter_jeu()
                return
            
            # Réinitialiser le temps pour le tour suivant
            self.temps_restant = self.duree_tour
            
            # Mettre à jour l'affichage et redémarrer le timer
            self.actualiser_plateau()
        
        # Redémarrer le timer dans tous les cas
        self.demarrer_timer()
    
    def quitter_jeu(self):
        """Ferme la fenêtre et quitte le jeu"""
        # Arrêter le timer avant de quitter
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
        self.root.destroy()

    def est_case_adjacente(self, x, y):
        """Vérifie si la case est adjacente au joueur (déplacement valide)"""
        # Adjacent signifie que la case est à une distance de 1 dans une seule direction (pas en diagonale)
        distance_x = abs(self.joueur_x - x)
        distance_y = abs(self.joueur_y - y)
        
        # Case adjacente et non obstacle
        return ((distance_x == 1 and distance_y == 0) or 
                (distance_x == 0 and distance_y == 1)) and (x, y) not in self.obstacles

    def gerer_clic(self, x, y):
        """Gère le clic sur une case pour le déplacement"""
        # Vérifier si c'est une case adjacente et non un obstacle
        if self.est_case_adjacente(x, y):
            # Annuler le timer actuel pour éviter des rappels multiples
            if self.timer_id:
                self.root.after_cancel(self.timer_id)
            
            # Déplacer le joueur
            self.joueur_x, self.joueur_y = x, y
            self.num_tour += 1
            
            # Vérifier la fin de partie
            if (self.joueur_x, self.joueur_y) == (self.pnj_x, self.pnj_y):
                self.actualiser_plateau()
                if self.role == "loup":
                    messagebox.showinfo("Victoire !", "Vous avez attrapé le villageois !")
                else:
                    messagebox.showinfo("Défaite !", "Vous avez été mangé par le loup !")
                self.quitter_jeu()
                return
            
            # Fin de partie par limite de tours
            if self.num_tour > self.tour_limite:
                self.actualiser_plateau()
                if self.role == "loup":
                    messagebox.showinfo("Défaite !", "Vous n'avez pas réussi à attraper le villageois à temps.")
                else:
                    messagebox.showinfo("Victoire !", "Vous avez survécu jusqu'à la fin du jeu !")
                self.quitter_jeu()
                return
            
            # Réinitialiser le temps pour le tour suivant
            self.temps_restant = self.duree_tour
            
            # Mettre à jour l'affichage et redémarrer le timer
            self.actualiser_plateau()
            self.demarrer_timer()

def main():
    # Récupérer les paramètres d'environnement
    role = os.environ.get('PLAYER_ROLE', "villageois")
    if role == "loup-garou":
        role = "loup"  # Convertir pour compatibilité
    player_name = os.environ.get('PLAYER_NAME', "Joueur")
    
    # Lancer la fenêtre de configuration
    config_root = tk.Tk()
    config_app = ConfigJeuTk(config_root)
    config_root.mainloop()
    
    # Si la configuration a été annulée, quitter
    if not config_app.config_ok:
        return
    
    # Lancer le jeu avec les paramètres configurés
    game_config = {
        'role': role,
        'player_name': player_name,
        'lignes': config_app.lignes,
        'colonnes': config_app.colonnes,
        'nombre_obstacles': config_app.nombre_obstacles,
        'duree_tour': config_app.duree_tour,
        'nombre_tours_max': config_app.nombre_tours_max
    }
    
    root = tk.Tk()
    app = WolfGameTk(root, game_config)
    root.mainloop()

if __name__ == "__main__":
    main()