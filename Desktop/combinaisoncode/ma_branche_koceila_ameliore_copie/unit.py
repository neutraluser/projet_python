import pygame
import random

pygame.init()

screen_info = pygame.display.Info()
screen_width = screen_info.current_w
screen_height = screen_info.current_h

# Calcul des tailles pour 42 lignes et 72 colonnes
CELL_SIZE = min(screen_height // 42, screen_width // 72)
GRID_SIZE = 72
LARGEUR_GRILLE = GRID_SIZE * CELL_SIZE
HEIGHT = 42 * CELL_SIZE
WIDTH = LARGEUR_GRILLE
FPS = 30
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)


class Unit:
    """
    Classe pour représenter une unité.
    """

    def __init__(self, x, y, health, attack_power, team, type_attaque, chakra, affinite,sprite_path=None):
        """
        Construit une unité avec une position, une santé, une puissance d'attaque et une équipe.
        """
        self.x = x
        self.y = y
        self.health = health
        self.attack_power = attack_power
        self.team = team
        self.is_selected = False
        self.type_attaque = type_attaque
        self.chakra = chakra
        self.affinite = affinite
        self.hide_subtitles = False
        self.mouse_clicked = False
        self.sprite = None
        if sprite_path:
            try:
                self.sprite = pygame.image.load(sprite_path)
                self.sprite = pygame.transform.scale(self.sprite, (CELL_SIZE , CELL_SIZE))
            except pygame.error as e:
                print(f"Erreur de chargement du sprite : {e}")
            
    def move(self, dx, dy):
        """Déplace l'unité de dx, dy."""
        L = [
            [0, 13], [1, 13], [7, 13], [8, 13], [4, 22], [3, 22], [20, 19], [20, 18], [20, 17],
            [21, 17], [22, 17], [22, 18], [22, 19], [18, 5], [19, 5], [18, 4], [18, 3], [18, 2],
            [18, 1], [17, 1], [16, 1], [16, 2], [16, 3], [16, 4]
        ]
        depla = True
        for i in range(len(L)):
            if (self.x + dx == L[i][0] and self.y + dy == L[i][1]):
                depla = False
        if depla:
            if 0 <= self.x + dx < LARGEUR_GRILLE / CELL_SIZE and 0 <= self.y + dy < HEIGHT / CELL_SIZE:
                self.x += dx
                self.y += dy

    def show_attack(self, screen):
        image_paths = [self.type_attaque.image_path_attaque1,self.type_attaque.image_path_attaque2]
        # Police
        font_title = pygame.font.Font(None, 36)  # Police pour le titre
        font_subtitle = pygame.font.Font(None, 15)
        text_color = (196, 15, 0)
        images = [pygame.image.load(path) for path in image_paths]
        button_rects = []
        # Redimensionner les images
        image_size = (100, 100)
        images = [pygame.transform.scale(img, image_size) for img in images]
        image_titles = [self.type_attaque.nom_attaque1, self.type_attaque.nom_attaque1]
        dx = self.x * 30
        dy = self.y * 30

        # Positionnement des images et titres
        image_spacing = 20
        start_x = dx + 20
        start_y = dy + 50
        for i in range(len(images)):
            button_rect = pygame.Rect(start_x + i * (image_size[0] + image_spacing), start_y, *image_size)
            button_rects.append(button_rect)
        frame_rect = pygame.Rect(dx, dy, 500, 200)
        background_color = (30, 30, 30)  # Gris foncé
        frame_color = (0, 0, 0)  # Rouge
        frame_width = 500
        pygame.draw.rect(screen, frame_color, frame_rect, frame_width)
        rectangle = pygame.draw.rect(screen, frame_color, frame_rect, frame_width)

        # dessiner une image
        # image = pygame.image.load("image_tech/technique_back.jpg")  # Remplacez "image.png" par le nom de votre fichier
        # image = pygame.transform.scale(image, (500, 200))
        # screen.blit(image, (frame_rect.x, frame_rect.y))

        # Dessiner le titre
        title_surface = font_title.render("Techniques d'affinite " + self.affinite, True, text_color)
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
                            # print(f"Le bouton {i + 1} a été cliqué !")
                            highlight_color = (0, 255, 0)
                            pygame.draw.rect(screen, highlight_color, rect, 4)
                            pygame.display.flip()
                            running = False
                            return i

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False

        pygame.display.flip()

    def clear_attack_bar(self, screen, button_rects):
        """
        Efface la barre des attaques en supprimant les boutons et leurs sous-titres.
        """
        for rect in button_rects:
            pygame.draw.rect(screen, BLACK, rect)
        pygame.display.flip()

    def play_sign_sequence(self, screen, image_paths, button_rects, delay=300):
        """
        Plays a sequence of images (the signs) with a delay between each image,
        overlaying them on the competence buttons.

        Parameters:
            ----------
            screen : pygame.Surface
            Surface on which to display the images.
            image_paths : list[str]
            List of paths to images to display.
            button_rects : list[pygame.Rect]
            List of rectangles representing the position and size of the competence buttons.
            delay : int
            Time (in milliseconds) between each image.
        """
        images = []
        for path in image_paths:
            try:
                img = pygame.image.load(path)
                img = pygame.transform.scale(img, (100, 100))  # Match competence button size
                images.append(img)
            except pygame.error as e:
                print(f"Error loading sign image {path}: {e}")
                placeholder = pygame.Surface((100, 100))
                placeholder.fill((0, 0, 0))  # Black placeholder
                images.append(placeholder)

        for img, rect in zip(images, button_rects):
               # Overlay the sign on the corresponding competence button
               screen.blit(img, rect.topleft)
               pygame.display.flip()
               pygame.time.delay(delay)


    def attack(self, target, pv):
        """
        Attacks a target unit.

        Parameters:
            ----------
        target : Unit
            The unit being attacked.
            pv : int
            The index of the competence being used.
        """
        # Validate pv index
        print(f"Liste des compétences disponibles : {[c.nom for c in self.type_attaque]}")

        if pv < 0 or pv >= len(self.type_attaque):
            print(f"Invalid competence index {pv}. Attack aborted.")
            return

        # Perform attack
        competence = self.type_attaque[pv]
        print(f"{self.team} unit attacking {target.team} unit with {competence.nom}.")
        target.health -= competence.puissance
        print(f"{self.team} attaque {target.team} pour {competence.puissance} dégâts !")
        print(f"PV restants de l'ennemi : {target.health}")
        if target.health <= 0:
            print(f"{target.team} unit defeated!")


    def draw(self, screen):
    
    
        if self.team == 'player' and self.sprite:
        # Afficher le sprite pour les joueurs
            screen.blit(self.sprite, (self.x * CELL_SIZE, self.y * CELL_SIZE))
        else:
        # Définir une couleur pour les ennemis ou les joueurs par défaut
            color = RED if self.team == 'enemy' else BLUE
        
        # Ajouter un contour vert si l'unité est sélectionnée
            if self.is_selected:
                pygame.draw.rect(screen, GREEN, (self.x * CELL_SIZE, self.y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        
        # Dessiner un cercle pour représenter l'unité
            pygame.draw.circle(
                screen,
                color,
                (self.x * CELL_SIZE + CELL_SIZE // 2, self.y * CELL_SIZE + CELL_SIZE // 2),
            CELL_SIZE // 3
        )

        
        
    def affiche_stat(self, screen):
        # Texte à afficher
        font = pygame.font.Font(None, 22)
        nb_player = 0
        nb_player_line = 0
        for player in self.player_units:
            for i in range(0, player.health, 10):
                image = pygame.image.load("coeur.png")
                image = pygame.transform.scale(image, (10, 10))
                x_offset = player.x * (LARGEUR_GRILLE / (CELL_SIZE - 6)) + i
                y_offset = player.y * (HEIGHT / GRID_SIZE)
                self.screen.blit(image, (x_offset - 30, y_offset + 40))
            nb_player += 1
            nb_player_line += 35
