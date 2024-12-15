import pygame
from level import *
import random
from competences import *

pygame.init()

screen_info = pygame.display.Info()
screen_width = screen_info.current_w
screen_height = screen_info.current_h

#screen_width = 600
#screen_height = 600

# Calcul des tailles pour 42 lignes et 72 colonnes
CELL_SIZE = min(screen_height // 42, screen_width // 72)  # Taille de la cellule pour 42x72 grille
GRID_SIZE = 72  # Nombre de colonnes
LARGEUR_GRILLE = GRID_SIZE * CELL_SIZE  # Largeur totale de la grille
HEIGHT = 42 * CELL_SIZE  # Hauteur totale de la grille
WIDTH = LARGEUR_GRILLE  # Largeur de la fenêtre
FPS = 30
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)


class Unit:
    """
    Classe pour représenter une unité.

    ...
    Attributs
    ---------
    x : int
        La position x de l'unité sur la grille.
    y : int
        La position y de l'unité sur la grille.
    health : int
        La santé de l'unité.
    attack_power : int
        La puissance d'attaque de l'unité.
    team : str
        L'équipe de l'unité ('player' ou 'enemy').
    is_selected : bool
        Si l'unité est sélectionnée ou non.

    Méthodes
    --------
    move(dx, dy)
        Déplace l'unité de dx, dy.
    attack(target)
        Attaque une unité cible.
    draw(screen)
        Dessine l'unité sur la grille.
    """

    def __init__(self, x, y, health, attack_power, team, competences, chakra, affinite, image, vitesse):
        """
        Construit une unité avec une position, une santé, une puissance d'attaque et une équipe.

        Paramètres
        ----------
        x : int
            La position x de l'unité sur la grille.
        y : int
            La position y de l'unité sur la grille.
        health : int
            La santé de l'unité.
        attack_power : int
            La puissance d'attaque de l'unité.
        team : str
            L'équipe de l'unité ('player' ou 'enemy').
        """
        self.x = x
        self.y = y
        self.health = health
        self.attack_power = attack_power
        self.team = team  # 'player' ou 'enemy'
        self.is_selected = False
        #self.type_attaque = type_attaque
        self.chakra=chakra
        self.affinite=affinite
        self.image = pygame.image.load(image)
        self.image=pygame.transform.scale(self.image, (CELL_SIZE, CELL_SIZE))
        self.vitesse=vitesse
        self.competences = Competence(affinite)

    def move(self, dx, dy,map_instance,screen):
        """Déplace l'unité de dx, dy."""
        L=map_instance.Liste_obstacles
        L_eau=map_instance.Liste_vide
        depla = True
        life=True


            # Charger l'image du crân

        L = map_instance.Liste_obstacles
        L_eau = map_instance.Liste_vide
        max_moves = self.vitesse# Nombre maximum de cases que l'unité peut parcourir
        #print(max_moves)

        # Calculer les positions accessibles
        possible_moves = []
        for dx in range(-max_moves, max_moves + 1):
            for dy in range(-max_moves, max_moves + 1):
                if abs(dx) + abs(dy) <= max_moves:
                    new_x = self.x + dx
                    new_y = self.y + dy
                    if 0 <= new_x < LARGEUR_GRILLE / CELL_SIZE and 0 <= new_y < HEIGHT / CELL_SIZE:
                        if ([new_x, new_y]) not in L :
                           # print(new_x,new_y)
                            possible_moves.append((new_x, new_y))

        # Initialiser le sélecteur bleu
        selector_x, selector_y = self.x, self.y
        if(self.team=="player"):
            running = True
            while running :
                for move_x, move_y in possible_moves:
                    rect = pygame.Rect(move_x * CELL_SIZE, move_y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                    pygame.draw.rect(screen, (200,255, 0), rect, 1)  # Jaune non rempli

                # Afficher le sélecteur bleu
                selector_rect = pygame.Rect(selector_x * CELL_SIZE, selector_y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(screen, (0, 0, 255), selector_rect, 2)  # Bleu



                pygame.display.flip()

                # Gérer les événements Pygame
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                    elif event.type == pygame.KEYDOWN:
                        # Déplacement du sélecteur
                        if event.key == pygame.K_LEFT:
                            selector_x = max(0, selector_x - 1)
                        elif event.key == pygame.K_RIGHT:
                            selector_x = min(LARGEUR_GRILLE // CELL_SIZE - 1, selector_x + 1)
                        elif event.key == pygame.K_UP:
                            selector_y = max(0, selector_y - 1)
                        elif event.key == pygame.K_DOWN:
                            selector_y = min(HEIGHT // CELL_SIZE - 1, selector_y + 1)

                        # Valider le déplacement avec Entrée
                        elif event.key == pygame.K_RETURN:
                            if (selector_x, selector_y) in possible_moves:
                                self.x = selector_x
                                self.y = selector_y

                                for i in range(len(L_eau)):
                                    if (self.x == L_eau[i][0] and self.y  == L_eau[i][1]):
                                        life = False
                                if (life):
                                    running = False
                                else:
                                    self.health = 0
                                    running = False
                                   # Quitter la boucle après le déplacement




    def show_attack(self, screen):
        # Récupérer les chemins d'images pour les attaques depuis les compétences
        image_paths = [self.competences.image_path_attaque1, self.competences.image_path_attaque2]
        
        # Police pour les titres et sous-titres
        font_title = pygame.font.Font(None, 36)  # Police pour le titre
        font_subtitle = pygame.font.Font(None, 15)  # Police pour les sous-titres
        text_color = (196, 15, 0)  # Couleur du texte
        
        # Charger et redimensionner les images des attaques
        images = [pygame.image.load(path) for path in image_paths]
        image_size = (100, 100)  # Taille des images des attaques
        images = [pygame.transform.scale(img, image_size) for img in images]
        
        # Titres des attaques
        image_titles = [self.competences.nom_attaque1, self.competences.nom_attaque2]
        
        # Position des images
        dx = self.x * CELL_SIZE
        dy = self.y * CELL_SIZE
        
        # Calculer l'espacement et la position initiale pour les boutons
        image_spacing = 20
        start_x = dx + 20
        start_y = dy + 50
        
        # Créer les rectangles pour chaque image de bouton
        button_rects = []
        for i in range(len(images)):
            button_rect = pygame.Rect(start_x + i * (image_size[0] + image_spacing), start_y, *image_size)
            button_rects.append(button_rect)
        
        # Définir le rectangle qui contient tout le cadre de sélection des attaques
        frame_rect = pygame.Rect(dx, dy, 500, 200)
        
        # Couleurs du cadre
        background_color = (30, 30, 30)  # Gris foncé pour le fond
        frame_color = (133, 133, 133)  # Gris pour le cadre
        frame_width = 2  # Largeur du cadre
        
        # Créer une surface transparente pour le fond du cadre
        transparent_surface = pygame.Surface((frame_rect.width, frame_rect.height), pygame.SRCALPHA)
        frame_color_with_alpha = (frame_color[0], frame_color[1], frame_color[2], 128)  # Opacité à 50%
        transparent_surface.fill(frame_color_with_alpha)
        
        # Dessiner la surface transparente sur l'écran
        screen.blit(transparent_surface, (frame_rect.x, frame_rect.y))
        
        # Dessiner les bordures du cadre
        pygame.draw.rect(screen, frame_color, frame_rect, width=frame_width)
        
        # Dessiner le titre "Techniques d'affinité"
        title_surface = font_title.render(f"Techniques d'affinité: {self.affinite}", True, text_color)
        title_x = frame_rect.x + (frame_rect.width - title_surface.get_width()) // 2
        title_y = frame_rect.y + 10
        screen.blit(title_surface, (title_x, title_y))
        
        # Dessiner les images des attaques et leurs sous-titres
        for i, (img, rect) in enumerate(zip(images, button_rects)):
            # Dessiner l'image du bouton
            screen.blit(img, rect.topleft)
            
            # Dessiner le sous-titre (nom de l'attaque)
            subtitle_surface = font_subtitle.render(image_titles[i], True, text_color)
            subtitle_x = rect.x + (rect.width - subtitle_surface.get_width()) // 2
            subtitle_y = rect.y + rect.height + 10  # Décalage vers le bas sous l'image
            screen.blit(subtitle_surface, (subtitle_x, subtitle_y))
        
        # Rafraîchir l'affichage pour rendre visible
        pygame.display.flip()
        

    def attack(self, target):
        """Attaque une unité cible."""
        target.health -= 1
    def special_attack(self, target,pv_attaque):
        """Attaque une unité cible."""
        target.health -=pv_attaque

    def draw(self, screen):

        if self.team == 'player' and self.image:

            screen.blit(self.image, (self.x * CELL_SIZE, self.y * CELL_SIZE))
        else:
            # Afficher l'image de l'ennemi
            screen.blit(self.image, (self.x * CELL_SIZE, self.y * CELL_SIZE))
    
    
    def affiche_stat(self,screen):
        # Texte à afficher
        WHITE = (255, 255, 255)
        BLACK = (0, 0, 0)
        VERT = (255, 255, 255)
        ROUGE = (255, 255, 255)
        color = (0, 0, 0)
        
        # Définition de la police de texte
        font = pygame.font.Font(None, 22)
        nb_player = 0
        nb_player_line = 0
        for player in self.player_units:
            texte = f"{player.chakra} "
            text_surface = font.render(texte, True, VERT)
            self.screen.blit(text_surface, (player.x * (CELL_SIZE)+CELL_SIZE, player.y * (CELL_SIZE)+CELL_SIZE))

            texte = f"{player.health} "
            text_surface = font.render(texte, True, VERT)
            self.screen.blit(text_surface, (player.x * (CELL_SIZE) + CELL_SIZE, player.y * (CELL_SIZE) -CELL_SIZE))


        for player in self.enemy_units:
            texte = f"{player.chakra} "
            text_surface = font.render(texte, True, VERT)
            self.screen.blit(text_surface, (player.x * (CELL_SIZE) + CELL_SIZE, player.y * (CELL_SIZE) + CELL_SIZE))

            texte = f"{player.health} "
            text_surface = font.render(texte, True, VERT)
            self.screen.blit(text_surface, (player.x * (CELL_SIZE) + CELL_SIZE, player.y * (CELL_SIZE) - CELL_SIZE))

