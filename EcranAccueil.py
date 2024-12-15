#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec  7 13:34:50 2024

@author: camelia
"""
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0,0,255)
RED = (255,0,0)
GREEN = (0,255,0)


import pygame
from unit import *  # Importe les constantes nécessaires
from EcranRegles import *  # Importe la classe EcranRegles

class EcranAccueil:
    def __init__(self, screen):
        self.screen = screen
        self.running = True
        self.background = pygame.image.load("Ecran_acc/fond3.png")
        self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))

    def afficher_texte(self, texte, taille, couleur, x, y, police_path=None):
        if police_path:
            font = pygame.font.Font(police_path, taille)
        else:
            font = pygame.font.Font(None, taille)

        surface = font.render(texte, True, couleur)
        rect = surface.get_rect(center=(x, y))
        self.screen.blit(surface, rect)

    def boucle_principale(self):
        clock = pygame.time.Clock()

        bouton_play_largeur = 200
        bouton_play_hauteur = 50
        bouton_play_x = (WIDTH - bouton_play_largeur) // 2
        bouton_play_y = (HEIGHT // 2) + 100

        bouton_regles_largeur = 200
        bouton_regles_hauteur = 50
        bouton_regles_x = (WIDTH - bouton_regles_largeur) // 2
        bouton_regles_y = bouton_play_y + bouton_play_hauteur + 20

        while self.running:
            self.screen.blit(self.background, (0, 0))

            self.afficher_texte("Abyssal combat ", 80, BLACK, WIDTH // 2, HEIGHT // 4, "police/police3.ttf")
            self.afficher_texte("Appuyez sur PLAY pour commencer", 50, WHITE, WIDTH // 2, HEIGHT // 2 - 50)

            pygame.draw.rect(self.screen, GREEN, (bouton_play_x, bouton_play_y, bouton_play_largeur, bouton_play_hauteur))
            self.afficher_texte("PLAY", 40, BLACK, bouton_play_x + bouton_play_largeur // 2, bouton_play_y + bouton_play_hauteur // 2)

            pygame.draw.rect(self.screen, BLUE, (bouton_regles_x, bouton_regles_y, bouton_regles_largeur, bouton_regles_hauteur))
            self.afficher_texte("RÈGLES", 40, WHITE, bouton_regles_x + bouton_regles_largeur // 2, bouton_regles_y + bouton_regles_hauteur // 2)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    if bouton_play_x <= x <= bouton_play_x + bouton_play_largeur and bouton_play_y <= y <= bouton_play_y + bouton_play_hauteur:
                        self.running = False
                        return "play"
                    elif bouton_regles_x <= x <= bouton_regles_x + bouton_regles_largeur and bouton_regles_y <= y <= bouton_regles_y + bouton_regles_hauteur:
                        # Instancier l'écran des règles et lancer sa boucle
                        ecran_regles = EcranRegles(self.screen)
                        result = ecran_regles.boucle_principale()
                        if result == "retour":
                            continue  # Retourne à l'écran d'accueil

            clock.tick(FPS)



