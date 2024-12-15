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
        self.background = pygame.image.load("Ecran_acc/wp2004925.webp")
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
            self.afficher_texte("Voici les règles du jeu :", 50, WHITE, WIDTH // 2, 100,"police/police3.ttf")
            self.afficher_texte("Le but du jeu est de vaincre l'intelligence artificielle dans un jeu de stratégie.", 40, WHITE, WIDTH // 2, 150)
            self.afficher_texte("Déplacement : Vous pouvez vous déplacer avec les flèches directionnelles : haut, bas, gauche, et droite.", 40, WHITE, WIDTH // 2, 200)
            self.afficher_texte("Attaque : Pour lancer une attaque :Appuyez sur le bouton A. Sélectionnez une attaque en appuyant ", 40, WHITE, WIDTH // 2, 250)
            self.afficher_texte("sur 1, 2 ou 3 Assurez-vous que l'ennemi se trouve dans la zone d'attaque avant de relâcher.", 40, WHITE, WIDTH // 2, 300)
            self.afficher_texte("Attention : La neige ralentit vos mouvements. L'eau peut vous tuer instantanément.", 40, WHITE, WIDTH // 2, 350)
            self.afficher_texte(
                "Bonne chance, soldat !",
                40, WHITE, WIDTH // 2, 400)

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
