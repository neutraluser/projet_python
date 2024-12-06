#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 13 19:05:05 2024

@author: camelia
"""

import pygame
import random

from unit import *

class cases:
    """
    Classe pour représenter les différentes cases.

    ...
    Attributs
    ---------
    x : int
        La position x de la case sur la grille.
    y : int
        La position y de la case sur la grille.
    soin : int
        La quantité de pv que redonne la case.
    pic : int
        La quantité de pv que fait perdre la case
    is_selected : bool
        Si l'unité est sélectionnée ou non.
    case_type : str, optional
        Le type de la case ('soin', 'pic', 'cachecache').
    image : pygame.Surface, optional
        L'image associée à la case.

    Méthodes
    --------
    case_soin(self, joueur)
        Case qui redonne des PVs.
    case_pic(self, joueur)
        Case qui retire des PVs.
    case_cachecache(self, joueur, ennemie)
        Case non-atteignable par les attaques des autres joueurs
    afficher_case(screen)
        Dessine la case sur la grille.
        
    Joueur est un objet de la classe unit
    """
    
    def __init__(self, x, y, soin, pic, case_type=None, image=None):
        """
        Construit une case avec une position, .

        Paramètres
        ----------
        x : int
            La position x de la case sur la grille.
        y : int
            La position y de la case sur la grille.
        soin : int
            La quantité de pv que redonne la case.
        pic : int
            La quantité de pv que fait perdre la case
        case_type : str, optional
            Le type de la case ('soin', 'pic', 'cachecache').
        image : pygame.Surface, optional
            L'image associée à la case.
        """
        self.x = x
        self.y = y
        self.soin = soin
        self.pic = pic
        self.case_type = case_type
        self.image = image
        self.is_selected = False
        
    def case_soin (self, joueur):
        """Case qui redonne des PV
        joueur : position (x,y) du joueur ??
        """
        if abs(self.x - joueur.x) <= 1 and abs(self.y - joueur.y) <= 1:
            joueur.health += self.soin  
            # pas sure du joueur.health, est-ce que j'ai le droit de l'utiliser même
            #si il est dans une autre classe ? je veux que mon perso perde 
        
    def case_pic(self, joueur):
        """Case qui retire des PV
        joueur : position (x,y) du joueur ??
        """
        if abs(self.x - joueur.x) <= 1 and abs(self.y - joueur.y) <= 1:
            joueur.health -= self.soin 
            joueur.x, joueur.y = joueur.position_précedente  # Revenir à la position précédente

        
    def case_cachecache(self, joueur):
        """Case qui rend le joueur intouchable par les attaques des autres joueurs
        """
        if abs(self.x - joueur.x) <= 1 and abs(self.y - joueur.y) <= 1:
            joueur.est_cache = True  # le code comprend que le joueur est caché
        else:
            joueur.est_cache = False  # Désactive le camouflage si le joueur quitte la case
            print("Le joueur est sur une case cache-cache, il ne peut pas être attaqué.")
        
    def afficher_case(self, screen):
        """Dessine la case avec son image sur l'écran."""
        if self.image:
            screen.blit(self.image, (self.x * CELL_SIZE, self.y * CELL_SIZE))
        

def generer_cases(images):
    """
    Génère les cases sur la grille avec des types aléatoires et des images.

    Paramètres
    ----------
    images : dict
        Dictionnaire contenant les images associées à chaque type de case.

    Retourne
    --------
    list[cases]
        Liste des objets cases générés.
    """
    cases_types = (
        ["soin"] * 2 +
        ["pic"] * 3 +
        ["cachecache"] * 3
    )
    random.shuffle(cases_types)

    positions = [(x, y) for x in range(GRID_SIZE) for y in range(GRID_SIZE)]
    random.shuffle(positions)

    all_cases = []
    for case_type in cases_types:
        x, y = positions.pop()
        if case_type == "soin":
            case = cases(x, y, soin=5, pic=0, case_type="soin", image=images["soin"])
        elif case_type == "pic":
            case = cases(x, y, soin=0, pic=5, case_type="pic", image=images["pic"])
        elif case_type == "cachecache":
            case = cases(x, y, soin=0, pic=0, case_type="cachecache", image=images["cachecache"])
        all_cases.append(case)

    return all_cases
            

        
        
        
        