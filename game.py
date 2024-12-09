import pygame
import random

from unit import *
from level import *
from EcranAccueil import *

class Game:
    """
    Classe pour représenter le jeu.

    ...
    Attributs
    ---------
    screen: pygame.Surface
        La surface de la fenêtre du jeu.
    player_units : list[Unit]
        La liste des unités du joueur.
    enemy_units : list[Unit]
        La liste des unités de l'adversaire.
    """

    def __init__(self, screen):
        """
        Construit le jeu avec la surface de la fenêtre.

        Paramètres
        ----------
        screen : pygame.Surface
            La surface de la fenêtre du jeu.
        """
        #===========la liste des attaques sont données comme suit==============>
        #[nom],[image],[Puissance d’attaque],[terrain	Puissance de défence],[Cout chakra]
        attaque_basique_feu=[[["Katon-boule de feu"],["image_tech/Katon-Goukakyuu-no-Jutsu.jpg"],[90],[0],[20],[50]],
                             [["Katon - Nuées ardentes"],["image_tech/Haisekish__1.png"], [80], [10], [2], [20]],
                             [["Katon - balsamine"],["image_tech/Katon_-_Balsamine_Pourpre.png"], [50], [0], [2], [5]],
                             [["Katon - Embrasement"],["image_tech/Katon_-_G_ka_Mekkyaku.png"], [100], [5], [30], [60]],]
        affinite= "Katon"

        attaque_basique_feu = [
            [["Katon-boule de feu"], ["image_tech/Katon-Goukakyuu-no-Jutsu.jpg"], [90], [0], [20], [50]],
            [["Katon - Nuées ardentes"], ["image_tech/Haisekish__1.png"], [80], [10], [2], [20]],
            [["Katon - balsamine"], ["image_tech/Katon_-_Balsamine_Pourpre.png"], [50], [0], [2], [5]],
            [["Katon - Embrasement"], ["image_tech/Katon_-_G_ka_Mekkyaku.png"], [100], [5], [30], [60]], ]
        affinite = "Katon"
        self.screen = screen #position(x,y)
        self.player_units = [Unit(0, 6, 100, 2, 'player',attaque_basique_feu,200,affinite),
                             Unit(1, 0, 100, 2, 'player',attaque_basique_feu,200,affinite)]

        self.enemy_units = [Unit(6, 6, 120, 0, 'enemy',attaque_basique_feu,200,affinite),
                            Unit(7, 6, 120, 1, 'enemy',attaque_basique_feu,200,affinite)]

    def handle_player_turn(self):
        L=[]
        """Tour du joueur"""
        for selected_unit in self.player_units:

            # Tant que l'unité n'a pas terminé son tour
            has_acted = False# tour pas terminé
            selected_unit.is_selected = True
            self.flip_display()# mis a jour de l'affichage
            while not has_acted:

                # Important: cette boucle permet de gérer les événements Pygame
                for event in pygame.event.get():

                    # Gestion de la fermeture de la fenêtre
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()

                    # Gestion des touches du clavier
                    if event.type == pygame.KEYDOWN:

                        # Déplacement (touches fléchées)
                        dx, dy = 0, 0
                        if event.key == pygame.K_LEFT:
                            dx = -1
                        elif event.key == pygame.K_RIGHT:
                            dx = 1
                        elif event.key == pygame.K_UP:
                            dy = -1
                        elif event.key == pygame.K_DOWN:
                            dy = 1
                        selected_unit.move(dx, dy)
                        self.flip_display()
                        pv_attack=selected_unit.attack_power

                        if event.key == pygame.K_a:  # Touche 'A'
                             pv_attack=selected_unit.show_attack(self.screen)
                             #self.flip_display()
                        if event.key == pygame.K_o:  # Touche 'A'
                             L.append([selected_unit.x,selected_unit.y])
                             print(L)

                        # Attaque (touche espace) met fin au tour
                        if event.key == pygame.K_SPACE:
                            for enemy in self.enemy_units:
                                if abs(selected_unit.x - enemy.x) <= 1 and abs(selected_unit.y - enemy.y) <= 1:
                                    selected_unit.attack(enemy,pv_attack)
                                    if enemy.health <= 0:
                                        self.enemy_units.remove(enemy)

                            has_acted = True
                            selected_unit.is_selected = False

    def handle_enemy_turn(self):
        """IA très simple pour les ennemis."""
        for enemy in self.enemy_units:

            # Déplacement aléatoire
            target = random.choice(self.player_units)
            dx = 1 if enemy.x < target.x else -1 if enemy.x > target.x else 0
            dy = 1 if enemy.y < target.y else -1 if enemy.y > target.y else 0
            enemy.move(dx, dy)

            # Attaque si possible
            if abs(enemy.x - target.x) <= 1 and abs(enemy.y - target.y) <= 1:
                enemy.attack(target)
                if target.health <= 0:
                    self.player_units.remove(target)

    def flip_display(self):
        """Affiche le jeu."""
        WHITE = (255, 255, 255)
        BLACK = (0, 0, 0)

        # Affiche la grille
        self.screen.fill(BLACK)
        level_map(self.screen, HEIGHT, LARGEUR_GRILLE)
        Unit.affiche_stat(self, self.screen)
        for x in range(0, LARGEUR_GRILLE, CELL_SIZE):
            for y in range(0, HEIGHT, CELL_SIZE):
                rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(self.screen, WHITE, rect, 1)


        # Affiche les unités
        for unit in self.player_units + self.enemy_units:
            unit.draw(self.screen)




        pygame.display.flip()


def main():
    # Initialisation de Pygame
    pygame.init()

    # Création de la fenêtre avec les dimensions de l'écran (via les constantes de Unit)
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Mon jeu de stratégie")

    # Afficher l'écran d'accueil
    ecran_accueil = EcranAccueil(screen)
    
    # Si le bouton PLAY est cliqué, le jeu commence
    if ecran_accueil.boucle_principale():
        # Maintenant, on peut importer Game ici, après que l'écran d'accueil est terminé
        from game import Game  # Importation de Game après l'écran d'accueil
        
        # Lancer le jeu une fois que l'écran d'accueil est terminé
        game = Game(screen)

        # Boucle principale du jeu
        while True:
            game.handle_player_turn()
            game.handle_enemy_turn()

if __name__ == "__main__":
    main()