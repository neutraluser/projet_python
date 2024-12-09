import pygame
import random
from Ecran_acceuil import selectionner_personnage
from unit import *
from level import *
from competences import Competence
from Personnage import *
# List of competences
competences_feu = [
    Competence(nom="Boule de Feu", puissance=90, defense=10, cout_chakra=20, image_path="image_tech/Katon-Goukakyuu-no-Jutsu.jpg"),
    Competence(nom="Nuées Ardentes", puissance=80, defense=20, cout_chakra=25, image_path="image_tech/Haisekish__1.png"),
    Competence(nom="Boule de Feu", puissance=90, defense=10, cout_chakra=20, image_path="image_tech/Katon-Goukakyuu-no-Jutsu.jpg"),
    Competence(nom="Nuées Ardentes", puissance=80, defense=20, cout_chakra=25, image_path="image_tech/Haisekish__1.png")
]

competences_eau = [
    Competence(nom="dragon_aqueu", puissance=100, defense=30, cout_chakra=40, image_path="image_tech/dragon_aqueu.png"),
    Competence(nom="Grande_Cataracte", puissance=70, defense=20, cout_chakra=15, image_path="image_tech/Grande_Cataracte.png"),
    Competence(nom="Tsunami", puissance=100, defense=30, cout_chakra=40, image_path="image_tech/Suiton-Tsunami.png"),
    Competence(nom="Torrent", puissance=70, defense=20, cout_chakra=15, image_path="image_tech/Suiton-Torrent.png")
]

competences_foudre = [
    Competence(nom="Éclair", puissance=85, defense=15, cout_chakra=20, image_path="image_tech/Foudre-Eclair.png"),
    Competence(nom="Tempête", puissance=95, defense=25, cout_chakra=30, image_path="image_tech/Foudre-Tempete.png"),
    Competence(nom="Éclair", puissance=85, defense=15, cout_chakra=20, image_path="image_tech/Foudre-Eclair.png"),
    Competence(nom="Tempête", puissance=95, defense=25, cout_chakra=30, image_path="image_tech/Foudre-Tempete.png")
]

# Characters
personnage_feu = Personnage("Feu", 100, 200, competences_feu, "Feu","sprites/feu.webp")
personnage_eau = Personnage("Eau", 120, 180, competences_eau, "Eau","sprites/eau.webp")
personnage_foudre = Personnage("Foudre", 110, 190, competences_foudre, "Foudre","sprites/foudre.webp")
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

    def __init__(self, screen, joueur):
        """
        Construit le jeu avec la surface de la fenêtre.

        Paramètres
        ----------
        screen : pygame.Surface
            La surface de la fenêtre du jeu.
        """
        #===========la liste des attaques sont données comme suit==============>
        #[nom],[image],[Puissance d’attaque],[terrain	Puissance de défence],[Cout chakra]
        '''attaque_basique_feu=[[["Katon-boule de feu"],["image_tech/Katon-Goukakyuu-no-Jutsu.jpg"],[90],[0],[20],[50]],
                             [["Katon - Nuées ardentes"],["image_tech/Haisekish__1.png"], [80], [10], [2], [20]],
                             [["Katon - balsamine"],["image_tech/Katon_-_Balsamine_Pourpre.png"], [50], [0], [2], [5]],
                             [["Katon - Embrasement"],["image_tech/Katon_-_G_ka_Mekkyaku.png"], [100], [5], [30], [60]],]
        affinite="Katon"

        attaque_basique_feu = [
            [["Katon-boule de feu"], ["image_tech/Katon-Goukakyuu-no-Jutsu.jpg"], [90], [0], [20], [50]],
            [["Katon - Nuées ardentes"], ["image_tech/Haisekish__1.png"], [80], [10], [2], [20]],
            [["Katon - balsamine"], ["image_tech/Katon_-_Balsamine_Pourpre.png"], [50], [0], [2], [5]],
            [["Katon - Embrasement"], ["image_tech/Katon_-_G_ka_Mekkyaku.png"], [100], [5], [30], [60]], ]
        affinite = "Katon"'''
        self.screen = screen #position(x,y)
        self.player_units = [
            Unit(0, 6, joueur.health, 90, "player", joueur.competences, joueur.chakra, joueur.affinite,joueur.sprite_path),
            Unit(0, 6, joueur.health, 90, "player", joueur.competences, joueur.chakra, joueur.affinite,joueur.sprite_path)
        ]
        self.enemy_units = [
            Unit(6, 6, 120, 80, "enemy", competences_feu, 200, "Feu"),
            Unit(7, 6, 120, 80, "enemy", competences_feu, 200, "Feu")
        ]
        


    def handle_player_turn(self):
        """Handles the player's turn."""
        for selected_unit in self.player_units:
            has_acted = False
            selected_unit.is_selected = True
            self.flip_display()

            while not has_acted:
                # Initialiser pv_attack avec une valeur par défaut
                pv_attack = selected_unit.attack_power
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()

                    if event.type == pygame.KEYDOWN:
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

                        if event.key == pygame.K_a:  # Touche 'A'
                            pv_attack = selected_unit.show_attack(self.screen)

                        if event.key == pygame.K_SPACE:
                            for enemy in self.enemy_units:
                                if abs(selected_unit.x - enemy.x) <= 1 and abs(selected_unit.y - enemy.y) <= 1:
                                    selected_unit.attack(enemy, pv_attack)

                                    if enemy.health <= 0:
                                        print(f"Enemy unit at ({enemy.x}, {enemy.y}) defeated.")
                                        self.enemy_units.remove(enemy)
                                        break  # Stop attacking if the enemy is removed

                            has_acted = True
                            selected_unit.is_selected = False


    def handle_enemy_turn(self):
        """Simple AI for enemy turns."""
        for enemy in self.enemy_units:
            if not self.player_units:
                print("All player units have been defeated!")
                return

            target = random.choice(self.player_units)
            pv = random.randint(0, len(enemy.type_attaque) - 1)

            dx = 1 if enemy.x < target.x else -1 if enemy.x > target.x else 0
            dy = 1 if enemy.y < target.y else -1 if enemy.y > target.y else 0
            enemy.move(dx, dy)
            
            if abs(enemy.x - target.x) <= 1 and abs(enemy.y - target.y) <= 1:
                enemy.attack(target, pv)

                if target.health <= 0:
                    print(f"Player unit at ({target.x}, {target.y}) defeated.")
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
               # pygame.draw.rect(self.screen, WHITE, rect, 1)


        # Affiche les unités
        for unit in self.player_units + self.enemy_units:
            unit.draw(self.screen)




        pygame.display.flip()


def main():

    # Initialisation de Pygame
    pygame.init()
    # Instanciation de la fenêtre
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Mon jeu de stratégie")
    
    # Character selection
    personnage_choisi = selectionner_personnage()
    print(f"Personnage sélectionné : {personnage_choisi}")
    
    # Map character to actual instance
    personnages_mapping = {
        "Feu": personnage_feu,
        "Eau": personnage_eau,
        "Foudre": personnage_foudre,
    }
    joueur = personnages_mapping[personnage_choisi]

    # Instanciation du jeu
    print(type(screen))
    game = Game(screen, joueur)
    #initalisation de l'environement et son
    #play_music(screen)

    # Boucle principale du jeu
    while True:
        game.handle_player_turn()
        game.handle_enemy_turn()
if __name__ == "__main__":
    main()