#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec  7 13:34:50 2024

@author: camelia
"""

import pygame
from unit import *

class EcranAccueil:
    def __init__(self, screen):
        self.screen = screen
        self.running = True
        # Charger l'image de fond
        self.background = pygame.image.load("Ecran_acc/fond3.png")
        self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))  
        

    def afficher_texte(self, texte, taille, couleur, x, y, police_path = None):
        # Si une police personnalisée est donnée, l'utiliser, sinon utiliser la police par défaut
        if police_path:
            font = pygame.font.Font(police_path, taille)
        else:
            font = pygame.font.Font(None, taille)  # Police par défaut

        surface = font.render(texte, True, couleur)
        rect = surface.get_rect(center=(x, y))
        self.screen.blit(surface, rect)

    def boucle_principale(self):
        clock = pygame.time.Clock()
        
        # Dimensions du bouton
        bouton_largeur = 200
        bouton_hauteur = 50
        bouton_x = (WIDTH - bouton_largeur) // 2
        bouton_y = (HEIGHT // 2) + 100

        while self.running:
            
            # Afficher l'image de fond
            self.screen.blit(self.background, (0, 0))

            # Texte principal
            self.afficher_texte("Mon Jeu de Stratégie", 80, BLACK, WIDTH // 2, HEIGHT // 4, "police/police3.ttf")

            # Instructions
            self.afficher_texte("Appuyez sur PLAY pour commencer", 80, WHITE, WIDTH // 2, HEIGHT // 2)

            # Bouton "Play"
            pygame.draw.rect(self.screen, GREEN, (bouton_x, bouton_y, bouton_largeur, bouton_hauteur))
            self.afficher_texte("PLAY", 40, BLACK, bouton_x + bouton_largeur // 2, bouton_y + bouton_hauteur // 2)

            pygame.display.flip()

            # Gestion des événements
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    # Vérifie si le clic est dans le bouton
                    if bouton_x <= x <= bouton_x + bouton_largeur and bouton_y <= y <= bouton_y + bouton_hauteur:
                        self.running = False  # Quitter la boucle et passer à l'écran du jeu
                        return True  # Indiquer que le jeu peut démarrer

            clock.tick(FPS)

