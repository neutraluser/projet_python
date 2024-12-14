#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 14 17:07:17 2024

@author: camelia
"""

import pygame
from unit import *
from EcranAccueil import *

class EcranRegles:
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
        
        bouton_retour_largeur = 200
        bouton_retour_hauteur = 50
        bouton_retour_x = (WIDTH - bouton_retour_largeur) // 2
        bouton_retour_y = HEIGHT - 100

        while self.running:
            # Afficher l'image de fond
            self.screen.blit(self.background, (0, 0))

            # Afficher les règles
            self.afficher_texte("Voici les règles du jeu :", 50, WHITE, WIDTH // 2, 100)
            self.afficher_texte("1. Déplacez vos personnages.", 40, WHITE, WIDTH // 2, 200)
            self.afficher_texte("2. Combattez vos adversaires.", 40, WHITE, WIDTH // 2, 250)
            self.afficher_texte("3. Gagnez en capturant l'objectif.", 40, WHITE, WIDTH // 2, 300)

            # Bouton "Retour"
            pygame.draw.rect(self.screen, RED, (bouton_retour_x, bouton_retour_y, bouton_retour_largeur, bouton_retour_hauteur))
            self.afficher_texte("RETOUR", 40, BLACK, bouton_retour_x + bouton_retour_largeur // 2, bouton_retour_y + bouton_retour_hauteur // 2)

            pygame.display.flip()

            # Gestion des événements
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    # Vérifie si le clic est dans le bouton "Retour"
                    if bouton_retour_x <= x <= bouton_retour_x + bouton_retour_largeur and bouton_retour_y <= y <= bouton_retour_y + bouton_retour_hauteur:
                        self.running = False  # Quitter l'écran des règles
                        return "retour"

            clock.tick(FPS)
