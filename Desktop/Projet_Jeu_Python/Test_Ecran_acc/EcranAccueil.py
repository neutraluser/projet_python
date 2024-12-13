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

    def afficher_texte(self, texte, taille, couleur, x, y, police_path=None):
        if police_path:
            font = pygame.font.Font(police_path, taille)
        else:
            font = pygame.font.Font(None, taille)  # Police par défaut

        surface = font.render(texte, True, couleur)
        rect = surface.get_rect(center=(x, y))
        self.screen.blit(surface, rect)

    def boucle_principale(self):
        clock = pygame.time.Clock()
        
        # Dimensions des boutons
        bouton_play_largeur = 200
        bouton_play_hauteur = 50
        bouton_play_x = (WIDTH - bouton_play_largeur) // 2
        bouton_play_y = (HEIGHT // 2) + 100
    
        bouton_regles_largeur = 200
        bouton_regles_hauteur = 50
        bouton_regles_x = (WIDTH - bouton_regles_largeur) // 2
        bouton_regles_y = bouton_play_y + bouton_play_hauteur + 20
    
        while self.running:
            # Afficher l'image de fond
            self.screen.blit(self.background, (0, 0))
    
            # Texte principal
            self.afficher_texte("Mon Jeu de Stratégie", 80, BLACK, WIDTH // 2, HEIGHT // 4, "police/police3.ttf")
    
            # Instructions
            self.afficher_texte("Appuyez sur PLAY pour commencer", 50, WHITE, WIDTH // 2, HEIGHT // 2 - 50)
    
            # Bouton "Play"
            pygame.draw.rect(self.screen, GREEN, (bouton_play_x, bouton_play_y, bouton_play_largeur, bouton_play_hauteur))
            self.afficher_texte("PLAY", 40, BLACK, bouton_play_x + bouton_play_largeur // 2, bouton_play_y + bouton_play_hauteur // 2)
    
            # Bouton "Règles"
            pygame.draw.rect(self.screen, BLUE, (bouton_regles_x, bouton_regles_y, bouton_regles_largeur, bouton_regles_hauteur))
            self.afficher_texte("RÈGLES", 40, WHITE, bouton_regles_x + bouton_regles_largeur // 2, bouton_regles_y + bouton_regles_hauteur // 2)
    
            pygame.display.flip()
    
            # Gestion des événements
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    # Vérifie si le clic est dans le bouton "Play"
                    if bouton_play_x <= x <= bouton_play_x + bouton_play_largeur and bouton_play_y <= y <= bouton_play_y + bouton_play_hauteur:
                        self.running = False
                        return "play"  # Indique que le jeu doit commencer
                    # Vérifie si le clic est dans le bouton "Règles"
                    elif bouton_regles_x <= x <= bouton_regles_x + bouton_regles_largeur and bouton_regles_y <= y <= bouton_regles_y + bouton_regles_hauteur:
                        self.running = False
                        return "regles"  # Indique que l'écran des règles doit s'afficher
    
            clock.tick(FPS)

