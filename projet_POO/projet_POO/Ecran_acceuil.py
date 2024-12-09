import pygame
import sys

pygame.init()

# Dimensions dynamiques basées sur la logique de unit.py
screen_info = pygame.display.Info()
screen_width = screen_info.current_w
screen_height = screen_info.current_h
CELL_SIZE = min(screen_height // 42, screen_width // 72)  # Taille de la cellule pour 42x72 grille
GRID_SIZE = 72  # Nombre de colonnes
LARGEUR_GRILLE = GRID_SIZE * CELL_SIZE  # Largeur totale de la grille
HEIGHT = 42 * CELL_SIZE  # Hauteur totale de la grille
WIDTH = LARGEUR_GRILLE  # Largeur de la fenêtre

# Initialiser l'écran avec les dimensions calculées
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Écran de sélection de personnage")

# Couleurs
WHITE = (255, 255, 255)

# Charger une image de fond
background = pygame.image.load("background.webp")  # Remplace par ton image
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

# Chargement des images
perso_feu = pygame.image.load("perso feu.webp")
perso_eau = pygame.image.load("perso eau.webp")
perso_foudre = pygame.image.load("foudre.webp")

# Calcul des tailles dynamiques des personnages
image_width = WIDTH // 5
image_height = HEIGHT // 2
perso_feu = pygame.transform.scale(perso_feu, (image_width, image_height))
perso_eau = pygame.transform.scale(perso_eau, (image_width, image_height))
perso_foudre = pygame.transform.scale(perso_foudre, (image_width, image_height))

# Calcul des positions des images
spacing = WIDTH // 10
positions = [
    (spacing, (HEIGHT - image_height) // 2),
    (2 * spacing + image_width, (HEIGHT - image_height) // 2),
    (3 * spacing + 2 * image_width, (HEIGHT - image_height) // 2),
]

# Noms des personnages
personnages = ["Feu", "Eau", "Foudre"]

def afficher_ecran_selection():
    """
    Affiche l'écran de sélection des personnages.
    """
    # Afficher le fond
    screen.blit(background, (0, 0))
    
    # Afficher les images et les noms des personnages
    font = pygame.font.Font(None, 50)
    images = [perso_feu, perso_eau, perso_foudre]
    for i, (img, pos) in enumerate(zip(images, positions)):
        screen.blit(img, pos)
        nom = font.render(personnages[i], True, WHITE)
        nom_x = pos[0] + (image_width - nom.get_width()) // 2
        nom_y = pos[1] + image_height + 10
        screen.blit(nom, (nom_x, nom_y))
    
    pygame.display.flip()

def selectionner_personnage():
    running = True
    personnage_choisi = None
    while running:
        afficher_ecran_selection()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                for i, (x, y) in enumerate(positions):
                    if x <= mouse_x <= x + image_width and y <= mouse_y <= y + image_height:
                        personnage_choisi = personnages[i]
                        running = False  # Quit loop after selection

    return personnage_choisi


if __name__ == "__main__":
    selectionner_personnage()
