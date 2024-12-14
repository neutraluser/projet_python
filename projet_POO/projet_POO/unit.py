import pygame
import random
from Personnage import *

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
        self.attack_power = attack_power if attack_power else type_attaque[0].puissance
        self.team = team
        self.is_selected = False
        self.type_attaque = type_attaque
        self.chakra = chakra
        self.affinite = affinite
        self.hide_subtitles = False
        self.mouse_clicked = False
        self.sprite = None
        self.evaded_this_turn = False
        
        if sprite_path:
            try:
                self.sprite = pygame.image.load(sprite_path)
                self.sprite = pygame.transform.scale(self.sprite, (CELL_SIZE , CELL_SIZE))
            except pygame.error as e:
                print(f"Erreur de chargement du sprite : {e}")
    def can_evade(self, player_units):
    # Détection d'une attaque imminente
        for player in player_units:
            if abs(self.x - player.x) <= 1 and abs(self.y - player.y) <= 1:
                if random.random() < 0.4:# 30% de chance d'esquive
                    return True
                    
        return False
            
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
        """
        Affiche les attaques disponibles et permet au joueur d'en choisir une.
        """
        # Extract image paths and titles from competences
        image_paths = [competence.image_path for competence in self.type_attaque]
        image_titles = [competence.nom for competence in self.type_attaque]

        # Font settings
        font_subtitle = pygame.font.Font(None, 15)
        text_color = (196, 15, 0)

        # Load and scale images
        images = []
        for path in image_paths:
            try:
                img = pygame.image.load(path)
                img = pygame.transform.scale(img, (100, 100))
                images.append(img)
            except pygame.error as e:
                print(f"Error loading image {path}: {e}")
                placeholder = pygame.Surface((100, 100))
                placeholder.fill((255, 0, 0))
                images.append(placeholder)

        # Position images and titles
        dx = self.x * CELL_SIZE
        dy = self.y * CELL_SIZE
        image_spacing = 20
        start_x = dx + 20
        start_y = dy + 50

        button_rects = []
        for i, img in enumerate(images):
            button_rect = pygame.Rect(start_x + i * (100 + image_spacing), start_y, 100, 100)
            button_rects.append(button_rect)

        # Draw images and titles
        for i, (img, rect) in enumerate(zip(images, button_rects)):
            screen.blit(img, rect.topleft)
            subtitle_surface = font_subtitle.render(image_titles[i], True, text_color)
            subtitle_x = rect.x + (rect.width - subtitle_surface.get_width()) // 2
            subtitle_y = rect.y + rect.height + 20
            screen.blit(subtitle_surface, (subtitle_x, subtitle_y))

        pygame.display.flip()

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                   mouse_pos = pygame.mouse.get_pos()
                   for i, rect in enumerate(button_rects):
                       if rect.collidepoint(mouse_pos):
                           print(f"Competence {i + 1} clicked!")

                           # Play sequence within the same window
                           sequences = [
                                   ["signes/belier.png", "signes/tigre.png", "signes/chien.png", "signes/rat.png"],
                                   ["signes/boeuf.png", "signes/singe.png", "signes/serpent.png", "signes/coq.png"],
                                   ["signes/tigre.png", "signes/rat.png", "signes/sanglier.png", "signes/tigre.png"],
                                   ["signes/lievre.png", "signes/tigre.png", "signes/cheval.png", "signes/boeuf.png"]
                                   ]
                           self.play_sign_sequence(screen, sequences[i], button_rects)
                           return i

                elif event.type == pygame.KEYDOWN:
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

    def ajuster_degats(self, competence):
        """
        Ajuste les dégâts reçus en fonction de l'affinité de la compétence.
        """
        modifiers = {
            "Feu": {"Eau": 0.8, "Foudre": 1.2},
            "Eau": {"Feu": 1.4, "Foudre": 0.8},
            "Foudre": {"Eau": 1.1, "Feu": 0.9},
        }

        if competence.affinite in modifiers and self.affinite in modifiers[competence.affinite]:
            return competence.puissance * modifiers[competence.affinite][self.affinite]
        return competence.puissance
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
        
        if target.team == "enemy" and target.can_evade([self]):
            print(f"{target.team} tente d'esquiver l'attaque {competence.nom}.")
            target.evade()
            return  # Annule l'attaque si l'esquive est réussie
        print(f"{self.team} unit attacking {target.team} unit with {competence.nom}.")
        damage = target.ajuster_degats(competence)
        target.health -= damage
        target.health = max(0, int(target.health))
        print(f"{self.team} attaque {target.team} pour {competence.puissance} dégâts !")
        print(f"PV restants de l'ennemi : {target.health}")
        if target.health <= 0:
            print(f"{target.team} unit defeated!")


    def draw(self, screen):
    
    
        if self.team == 'player' and self.sprite:
        # Afficher le sprite pour les joueurs
            screen.blit(self.sprite, (self.x * CELL_SIZE, self.y * CELL_SIZE))
        elif self.team == 'enemy' and self.sprite:
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

    def evade(self):
        
    
    #Effectue un déplacement défensif pour esquiver une attaque imminente.
    
    # Liste des directions possibles
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        random.shuffle(directions)  # Mélanger les directions pour éviter les modèles prévisibles

        for dx, dy in directions:
            new_x = self.x + dx
            new_y = self.y + dy
        # Vérifie si le déplacement est valide (hors des obstacles et dans les limites)
            if 0 <= new_x < LARGEUR_GRILLE // CELL_SIZE and 0 <= new_y < HEIGHT // CELL_SIZE:
                self.move(dx, dy)
                print(f"{self.team} esquive et se déplace vers ({self.x}, {self.y}).")
                return
        print(f"{self.team} n'a pas pu esquiver. Aucune direction valide.")
    
        
    def affiche_stat(screen, units):
        # Texte à afficher
        font = pygame.font.Font(None, 22)
        health_per_heart = 20  # Chaque cœur représente 20 points de vie

        
        for unit in units:
            num_hearts = int(unit.health // health_per_heart)

        # Charger l'image du cœur
            heart_image = pygame.image.load("coeur.png")
            heart_image = pygame.transform.scale(heart_image, (10, 10))

        # Position de départ pour les cœurs
            x_offset = unit.x * CELL_SIZE
            y_offset = unit.y * CELL_SIZE - 20

            for i in range(num_hearts):
                # Calcule la position du cœur (les cœurs s'alignent horizontalement)
                heart_x = x_offset + (i * 12)  # Décalage horizontal entre les cœurs
                screen.blit(heart_image, (heart_x, y_offset))
            