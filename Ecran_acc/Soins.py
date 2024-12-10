#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  9 11:31:04 2024

@author: camelia
"""

import pygame
import random
import os  # Pour gérer les chemins des fichiers

from unit import *  # Assurez-vous que cette importation est correcte

# Chemin vers le dossier contenant l'image des soins
IMAGE_PATH = "icone/coeur.png"

class Soins:
    """
    Classe pour représenter les différentes cases de soin.
    
    Attributs :
    ----------
    x : int
        La position x de la case sur la grille.
    y : int
        La position y de la case sur la grille.
    soin : int
        La quantité de PV que redonne la case.
    is_selected : bool
        Si la case est sélectionnée ou non.
    case_type : str, optionnel
        Le type de la case ('soin').
    image : pygame.Surface, optionnel
        L'image associée à la case.
    
    Méthodes :
    --------
    case_soin(self, joueur)
        Redonne des PVs à un joueur ou un ennemi si il passe sur la case.
    afficher_case(screen)
        Dessine la case sur la grille.
    """
    
    def __init__(self, x, y, soin, case_type="soin", image=None):
        """
        Construit une case de soin avec une position et un soin à appliquer.

        Paramètres :
        ----------
        x : int
            La position x de la case sur la grille.
        y : int
            La position y de la case sur la grille.
        soin : int
            La quantité de PV que redonne la case.
        case_type : str, optionnel
            Le type de la case ('soin').
        image : pygame.Surface, optionnel
            L'image associée à la case.
        """
        self.x = x
        self.y = y
        self.soin = soin
        self.case_type = case_type
        self.image = image
        self.is_selected = False # pour savoir si la case est selectionner
        self.used = False  # pour savoir si la case a déjà été utilisée
        
    def case_soin(self, joueur):
        """Redonne des PV à un joueur ou un ennemi."""
        if not self.used:  # Si la case n'a pas encore été utilisée
            if abs(self.x - joueur.x) <= 1 and abs(self.y - joueur.y) <= 1:
                joueur.health += self.soin
                self.used = True  # Marque la case comme utilisée
                print(f"{joueur.team} a regagné {self.soin} PV !")
                return True  # Indique que la case a été utilisée
        return False

    def afficher_case(self, screen):
        """Dessine la case avec son image sur l'écran."""
        if self.image and not self.used:  # N'affiche la case que si elle n'a pas été utilisée:
            # Redimensionner l'image à la taille d'un carreau de la grille
            resized_image = pygame.transform.scale(self.image, (CELL_SIZE, CELL_SIZE))  # Redimensionnement
            screen.blit(resized_image, (self.x * CELL_SIZE, self.y * CELL_SIZE))
            

def generer_cases(images):
    """
    Génère les cases sur la grille avec des types aléatoires et des images.

    Paramètres :
    ----------
    images : dict
        Dictionnaire contenant les images associées à chaque type de case.

    Retourne :
    --------
    list[Soins]
        Liste des objets Soins générés.
    """
    cases_types = ["soin"] * 15  # 15 cases de soins
    random.shuffle(cases_types)

    # Générer des positions aléatoires sur la grille
    positions = [(x, y) for x in range(GRID_SIZE) for y in range(GRID_SIZE)]
    random.shuffle(positions)

    all_cases = []
    for case_type in cases_types:
        x, y = positions.pop()
        if case_type == "soin":
            # Assurez-vous que l'image "coeur.png" est correctement chargée
            case = Soins(x, y, soin=1, case_type="soin", image=images["soin"])
            all_cases.append(case)

    return all_cases

def charger_images():
    """
    Charge toutes les images nécessaires pour le jeu, y compris celles des soins.

    Retourne :
    --------
    dict
        Dictionnaire contenant les images associées à chaque type de case.
    """
    images = {}
    
    # Chargement de l'image "coeur.png" depuis le dossier "icone"
    try:
        images["soin"] = pygame.image.load(IMAGE_PATH).convert_alpha()
    except pygame.error as e:
        print(f"Erreur lors du chargement de l'image de soin: {e}")
    
    return images
