import pygame

def fireball_animation(player ,enemys ,screen, fireball_image, trajectory, cell_size ,pv_attack):
    """Anime une boule de feu suivant une trajectoire."""
    """Anime une boule de feu suivant une trajectoire en utilisant une capture d'écran."""

    # Faire une capture de la fenêtre
    background = screen.copy()  # Capture l'état actuel de la fenêtre
    player.chakra -=player.type_attaque[pv_attack][2][0]

    for i, point in enumerate(trajectory):
        # Convertir les coordonnées de la grille en pixels
        x_pixel = point[0] * cell_size
        y_pixel = point[1] * cell_size
        for enemy in enemys:
            if(point[0 ]==enemy.x and point[1 ]==enemy.y):
                print(player.type_attaque[pv_attack][2][0])
                player.special_attack(enemy ,player.type_attaque[pv_attack][2][0])


        # Redessiner l'arrière-plan depuis la capture d'écran
        screen.blit(background, (0, 0))

        # Dessiner la boule de feu à la position actuelle
        screen.blit(fireball_image, (x_pixel, y_pixel))

        # Mettre à jour l'affichage
        pygame.display.flip()

        # Attendre un court instant pour l'animation
        pygame.time.delay(50)
    # Dernière mise à jour pour s'assurer que l'image finale reste affichée
    escape_event = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_ESCAPE})
    pygame.event.post(escape_event)

    pygame.display.flip()


def calculate_trajectory(start, end):
    """Calcule les points d'une trajectoire en ligne droite entre deux positions."""
    x1, y1 = start
    x2, y2 = end

    # Utilisation de l'algorithme de Bresenham pour une ligne droite
    points = []
    dx = x2 - x1
    dy = y2 - y1
    steps = max(abs(dx), abs(dy))

    for step in range(steps + 1):
        t = step / steps
        x = round(x1 + t * dx)
        y = round(y1 + t * dy)
        points.append((x, y))

    return points