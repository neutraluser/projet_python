import pygame
import random

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

    def __init__(self, x, y, health, attack_power, team,type_attaque,chakra,affinite):
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
        self.type_attaque=type_attaque
        self.chakra=chakra
        self.affinite=affinite

    def move(self, dx, dy):
        """Déplace l'unité de dx, dy."""
        L=[[0, 13], [1, 13], [7, 13], [8, 13], [4, 22], [3, 22], [20, 19], [20, 18], [20, 17], [21, 17], [22, 17], [22, 18], [22, 19], [18, 5], [19, 5], [18, 4], [18, 3], [18, 2], [18, 1], [17, 1], [16, 1], [16, 2], [16, 3], [16, 4]]
        depla=True
        for i in range(len(L)):
            if (self.x + dx ==L[i][0] and self.y + dy ==L[i][1]):
                depla = False
        if(depla ):
            if 0 <= self.x + dx < LARGEUR_GRILLE/CELL_SIZE  and 0 <= self.y + dy < HEIGHT/CELL_SIZE :
                self.x += dx
                self.y += dy
    def show_attack(self,screen):
        image_paths = [self.type_attaque[0][1][0],self.type_attaque[1][1][0], self.type_attaque[2][1][0],self.type_attaque[3][1][0]]
        # Police
        font_title = pygame.font.Font(None, 36)  # Police pour le titre
        font_subtitle = pygame.font.Font(None, 15)
        text_color = (196, 15,0)
        images = [pygame.image.load(path) for path in image_paths]
        button_rects = []
        # Redimensionner les images
        image_size = (100, 100)
        images = [pygame.transform.scale(img, image_size) for img in images]
        image_titles = [self.type_attaque[0][0][0],self.type_attaque[1][0][0], self.type_attaque[2][0][0],self.type_attaque[3][0][0]]
        dx=self.x*30
        dy=self.y*30

        # Positionnement des images et titres
        image_spacing = 20
        start_x = dx + 20
        start_y = dy + 50
        for i in range(len(images)):
            button_rect = pygame.Rect(start_x + i * (image_size[0] + image_spacing), start_y, *image_size)
            button_rects.append(button_rect)
        frame_rect = pygame.Rect(dx,dy, 500, 200)
        background_color = (30, 30, 30)  # Gris foncé
        frame_color = (0,0,0)  # Rouge
        frame_width =500
        pygame.draw.rect(screen, frame_color, frame_rect, frame_width)
        rectangle=pygame.draw.rect(screen, frame_color, frame_rect, frame_width)

        # dessiner une image
        #image = pygame.image.load("image_tech/technique_back.jpg")  # Remplacez "image.png" par le nom de votre fichier
        #image = pygame.transform.scale(image, (500, 200))
        #screen.blit(image, (frame_rect.x, frame_rect.y))

        # Dessiner le titre
        title_surface = font_title.render("Techniques d'affinite "+self.affinite, True, text_color)
        title_x = frame_rect.x + (frame_rect.width - title_surface.get_width()) // 2
        title_y = frame_rect.y + 10
        screen.blit(title_surface, (title_x, title_y))

        # Dessiner les images et les sous-titres
        for i, (img, rect) in enumerate(zip(images, button_rects)):
            # Dessiner l'image
            screen.blit(img, rect.topleft)

            # Dessiner le sous-titre
            subtitle_surface = font_subtitle.render(image_titles[i], True, text_color)
            subtitle_x = rect.x + (rect.width - subtitle_surface.get_width()) // 2
            subtitle_y = rect.y + rect.height + 20
            screen.blit(subtitle_surface, (subtitle_x, subtitle_y))
        running = True
        pygame.display.flip()
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                # Détecter les clics sur les boutons
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    for i, rect in enumerate(button_rects):
                        if rect.collidepoint(mouse_pos):
                            print(f"Le bouton {i + 1} a été cliqué !")
                            highlight_color = (0, 255, 0)
                            pygame.draw.rect(screen, highlight_color, rect, 4)
                            pygame.display.flip()
                            running = False
                            return i
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False


        pygame.display.flip()

    def attack(self, target,pv):
        """Attaque une unité cible."""
        if abs(self.x - target.x) <= 1 and abs(self.y - target.y) <= 1:
            target.health -= self.type_attaque[pv][2][0]

    def draw(self, screen):
        """Affiche l'unité sur l'écran."""
        color = BLUE if self.team == 'player' else RED
        if self.is_selected:
            pygame.draw.rect(screen, GREEN, (self.x * CELL_SIZE,
                             self.y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        pygame.draw.circle(screen, color, (self.x * CELL_SIZE + CELL_SIZE //
                           2, self.y * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 3)
    def affiche_stat(self,screen):
        # Texte à afficher
        WHITE = (255, 255, 255)
        BLACK = (0, 0, 0)
        VERT = (255, 255, 255)
        ROUGE = (255, 255, 255)
        color = (0, 0, 0)
        #barre_de_vie = pygame.draw.rect(self.screen, color, pygame.Rect(400, 0, WIDTH, HEIGHT))

        # Définition de la police de texte
        font = pygame.font.Font(None, 22)
        nb_player = 0
        nb_player_line = 0
        for player in self.player_units:
            #texte = f"Charter player---> {nb_player}"
            #text_surface = font.render(texte, True, VERT)
            #self.screen.blit(text_surface, (GRID_SIZE * CELL_SIZE, nb_player_line))

            #texte = f"x:{player.x}  y:{player.y}  Pv:{player.health}  Pwr:{player.attack_power} "
            #text_surface = font.render(texte, True, VERT)
            #self.screen.blit(text_surface, (GRID_SIZE * CELL_SIZE, nb_player_line + 15))

            for i in range(0, player.health, 10):
                image = pygame.image.load("icone/coeur.png")  # Charge l'image
                image = pygame.transform.scale(image, (10, 10))  # Redimensionne l'image

                # Calcule les coordonnées décalées en fonction de `i`
                x_offset = player.x * (LARGEUR_GRILLE / (CELL_SIZE - 6)) + i # Décalage horizontal
                y_offset = player.y * (HEIGHT / (GRID_SIZE))  # Pas de décalage vertical ici, mais vous pouvez l'ajouter

                # Affiche l'image à la position décalée
                self.screen.blit(image, (x_offset-30, y_offset+40))



            nb_player = nb_player + 1
            nb_player_line = nb_player_line + 35
        nb_player = 0
        for player in self.enemy_units:
            #texte = f"Charter enemy---> {nb_player}"
            #text_surface = font.render(texte, True, ROUGE)
            #self.screen.blit(text_surface, (GRID_SIZE * CELL_SIZE, nb_player_line))

            #texte = f"x:{player.x}  y:{player.y}  Pv:{player.health}  Pwr:{player.attack_power} "
            #text_surface = font.render(texte, True, ROUGE)
            #self.screen.blit(text_surface, (GRID_SIZE * CELL_SIZE, nb_player_line + 15))

            nb_player = nb_player + 1
            nb_player_line = nb_player_line + 35


        #surface = pygame.display.set_mode((400, 300))



