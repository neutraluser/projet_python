import pygame
import random
from Ecran_acceuil import selectionner_personnage
from unit import *
from level import *
from competences import Competence
from Personnage import *
from trainer import *

# List of competences
competences_feu = [
    Competence(nom="Boule de Feu", puissance=30, defense=10, cout_chakra=80, image_path="image_tech/Katon-Goukakyuu-no-Jutsu.jpg",affinite="Feu"),
    Competence(nom="Nuées Ardentes", puissance=80, defense=20, cout_chakra=25, image_path="image_tech/Haisekish__1.png",affinite="Feu"),
    Competence(nom="Katon_Pourpre", puissance=90, defense=10, cout_chakra=20, image_path="image_tech/Katon_-_Balsamine_Pourpre.png",affinite="Feu"),
    Competence(nom="Katon_Mekkyaku", puissance=80, defense=20, cout_chakra=25, image_path="image_tech/Katon_-_G_ka_Mekkyaku.png",affinite="Feu")
]

competences_eau = [
    Competence(nom="dragon_aqueu", puissance=100, defense=30, cout_chakra=40, image_path="image_tech/dragon_aqueu.png",affinite="Eau"),
    Competence(nom="Grande_Cataracte", puissance=70, defense=20, cout_chakra=15, image_path="image_tech/Grande_Cataracte.png",affinite="Eau"),
    Competence(nom="Tsunami", puissance=100, defense=30, cout_chakra=40, image_path="image_tech/Suiton-Tsunami.png",affinite="Eau"),
    Competence(nom="Torrent", puissance=70, defense=20, cout_chakra=15, image_path="image_tech/Suiton-Torrent.png",affinite="Eau")
]

competences_foudre = [
    Competence(nom="Éclair", puissance=85, defense=15, cout_chakra=20, image_path="image_tech/Foudre-Eclair.png", affinite="Foudre"),
    Competence(nom="Tempête", puissance=95, defense=25, cout_chakra=30, image_path="image_tech/Foudre-Tempete.png", affinite="Foudre"),
    Competence(nom="orbe_raiton", puissance=85, defense=15, cout_chakra=20, image_path="image_tech/orbe_raiton.png", affinite="Foudre"),
    Competence(nom="raiton_sasuke", puissance=95, defense=25, cout_chakra=30, image_path="image_tech/raiton_sasuke.png", affinite="Foudre")
]

# Characters
personnage_feu = Personnage("Feu", 340, 200, competences_feu, "Feu","sprites/feu.webp")
personnage_eau = Personnage("Eau", 120, 180, competences_eau, "Eau","sprites/eau.webp")
personnage_foudre = Personnage("Foudre", 110, 190, competences_foudre, "Foudre","sprites/foudre.webp")
class Game:
    """
    Classe pour représenter le jeu.

    Attributs
    ---------
    screen: pygame.Surface
        La surface de la fenêtre du jeu.
    player_units : list[Unit]
        La liste des unités du joueur.
    trainer : Trainer
        Le contrôleur des unités ennemies.
    """

    def __init__(self, screen, joueur):
        """
        Construit le jeu avec la surface de la fenêtre.

        Paramètres
        ----------
        screen : pygame.Surface
            La surface de la fenêtre du jeu.
        """
        self.screen = screen
        self.player_units = [
            Unit(0, 6, joueur.health, None, "player", joueur.competences, joueur.chakra, joueur.affinite, joueur.sprite_path),
            Unit(1, 6, joueur.health, None, "player", joueur.competences, joueur.chakra, joueur.affinite, joueur.sprite_path),
        ]
        self.enemy_units = []  # Liste des unités ennemies (remplie par Trainer)

    def assign_ia_character(self, joueur_affinite):
        """
        Assigne un personnage et des compétences optimales à l'IA pour contrer l'affinité du joueur.

        Paramètres
        ----------
        joueur_affinite : str
            L'affinité du joueur (Feu, Eau, Foudre, etc.).
        """
        ia_affinite_map = {
            "Feu": "Eau",       # Eau contre Feu
            "Eau": "Foudre",    # Foudre contre Eau
            "Foudre": "Feu"     # Feu contre Foudre
        }

        # Trouve l'affinité optimale pour l'IA
        ia_affinite = ia_affinite_map.get(joueur_affinite, "Feu")  # Par défaut "Feu"

        # Sélectionne les compétences et sprites correspondants
        if ia_affinite == "Feu":
            ia_competences = competences_feu
            ia_sprite = "sprites/feu.webp"
        elif ia_affinite == "Eau":
            ia_competences = competences_eau
            ia_sprite = "sprites/eau.webp"
        elif ia_affinite == "Foudre":
            ia_competences = competences_foudre
            ia_sprite = "sprites/foudre.webp"
        else:
            print(f"Affinité inconnue : {joueur_affinite}")
            ia_competences = competences_feu
            ia_affinite = "Feu"
            ia_sprite = "sprites/feu.webp"

        # Initialise le Trainer (IA)
        self.trainer = Trainer(0, 0, 200, None, "enemy", ia_competences, 300, ia_affinite, ia_sprite)

        # Ajoute les unités contrôlées par l'IA
        self.trainer.add_unit(Unit(6, 6, 120, None, "enemy", ia_competences, 300, ia_affinite, ia_sprite))
        self.trainer.add_unit(Unit(7, 6, 120, None, "enemy", ia_competences, 300, ia_affinite, ia_sprite))
        print(f"L'IA a choisi le personnage de type {ia_affinite} pour contrer {joueur_affinite}.")
    def handle_enemy_turn(self):
        """Gère le tour de l'IA."""
        if not self.player_units:
            print("All player units have been defeated!")
            return

        self.trainer.handle_turn(self.player_units, self.screen)    
    def handle_player_turn(self):
        """Gère le tour des joueurs."""
        for selected_unit in self.player_units:
            has_acted = False
            selected_unit.is_selected = True
            pv_attack = None
            self.flip_display()

            while not has_acted:
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

                        if event.key == pygame.K_a:  # Sélection d'une attaque
                            pv_attack = selected_unit.show_attack(self.screen)

                        if event.key == pygame.K_SPACE:
                            for enemy in self.trainer.controlled_units:
                                if abs(selected_unit.x - enemy.x) <= 1 and abs(selected_unit.y - enemy.y) <= 1:
                                    if pv_attack is not None:
                                        selected_unit.attack(enemy, pv_attack)
                                    if enemy.health <= 0:
                                        print(f"Enemy unit at ({enemy.x}, {enemy.y}) defeated.")
                                        self.trainer.controlled_units.remove(enemy)
                                    self.handle_enemy_turn()
                                    break  # Stop attacking if the enemy is removed

                            has_acted = True
                            selected_unit.is_selected = False

    

       
    def flip_display(self):
        """Affiche le jeu."""
        WHITE = (255, 255, 255)
        BLACK = (0, 0, 0)

        # Affiche la grille
        self.screen.fill(BLACK)
        level_map(self.screen, HEIGHT, LARGEUR_GRILLE)
        Unit.affiche_stat(self.screen, self.player_units + self.trainer.controlled_units)

        
        for x in range(0, LARGEUR_GRILLE, CELL_SIZE):
            for y in range(0, HEIGHT, CELL_SIZE):
                rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
               # pygame.draw.rect(self.screen, WHITE, rect, 1)


        # Affiche les unités
        for unit in self.player_units + self.trainer.controlled_units:
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
    game.assign_ia_character(joueur.affinite)


    # Boucle principale du jeu
    while True:
        game.handle_player_turn()
        game.handle_enemy_turn()
        
        
if __name__ == "__main__":
    main()