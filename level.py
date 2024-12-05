import pygame


def play_music(screen):
    pygame.mixer.music.load("track/Sonic 1 Music Marble Zone.mp3")
    pygame.mixer.music.play()
def level_map(screen,HEIGHT,WIDTH ):
    image = pygame.image.load("maps/map1_1.jpg")  # Remplacez "image.png" par le nom de votre fichier
    image = pygame.transform.scale(image, (WIDTH,HEIGHT))
    screen.blit(image, (0,0))

    #image_obstacle = pygame.image.load("maps/obstacle/mer.png")  # Remplacez "image.png" par le nom de votre fichier
    #image_obstacle  = pygame.transform.scale(image_obstacle, (200, 100))
    #screen.blit(image_obstacle , (450, 240))


