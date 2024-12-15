import pygame
import time

def calculate_trajectory(start, end):
    """
    Calcule une liste de points (x, y) entre start et end pour tracer une trajectoire en ligne droite.
    start et end sont des tuples (x_start, y_start) et (x_end, y_end).
    """
    x1, y1 = start
    x2, y2 = end

    points = []
    dx = x2 - x1
    dy = y2 - y1
    steps = max(abs(dx), abs(dy))

    if steps == 0:
        # Si la cible est la même case, pas de trajectoire nécessaire.
        points.append((x1, y1))
        return points

    for step in range(steps + 1):
        t = step / steps
        x = round(x1 + t * dx)
        y = round(y1 + t * dy)
        points.append((x, y))

    return points

def fireball_animation(screen, attack_image, trajectory, cell_size):
    """
    Anime l'attaque (par exemple une boule de feu) se déplaçant le long de 'trajectory'.
    trajectory est une liste de tuples (x, y).
    attack_image est déjà chargée et redimensionnée.
    """
    # On copie l'écran pour restaurer l'arrière-plan à chaque frame
    background = screen.copy()

    for i, point in enumerate(trajectory):
        x_pixel = point[0] * cell_size
        y_pixel = point[1] * cell_size

        # Redessiner l'arrière-plan
        screen.blit(background, (0, 0))

        # Dessiner l'image de l'attaque
        screen.blit(attack_image, (x_pixel, y_pixel))

        pygame.display.flip()
        pygame.time.delay(100)  # Ajustez ce délai pour la vitesse de l'animation
