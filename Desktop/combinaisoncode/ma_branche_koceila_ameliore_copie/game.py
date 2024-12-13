import pygame
import random
from Ecran_acceuil import selectionner_personnage
from unit import *
from level import *
from competences import Competence
from Personnage import *
# List of competences
# Characters
personnage_feu = Personnage("Edan", 150, 200, "Feu", "sprites/feu.webp")
personnage_eau = Personnage("Oceane", 120, 180, "Eau","sprites/eau.webp")
personnage_foudre = Personnage("Zeus", 110, 190, "Foudre","sprites/foudre.webp")
class Game:
    def __init__(self, screen, joueur):
        self.screen = screen #position(x,y)
        self.player_units = [
            Unit(0, 6, joueur.health, 1, "player", joueur.competences, joueur.chakra, joueur.affinite,joueur.image),
            Unit(0, 6, joueur.health, 1, "player", joueur.competences, joueur.chakra, joueur.affinite,joueur.image)
        ]
        self.enemy_units = [
            Unit(6, 6, 120, 80, "enemy", Competence("Feu"), 200, "Feu"),
            Unit(7, 6, 120, 80, "enemy",Competence("Feu"), 200, "Feu")
        ]
        


    def handle_player_turn(self):
        """Handles the player's turn."""
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
                        
                        if event.key == pygame.K_a:  # Touche 'A'
                            #print(selected_unit.type_attaque.image_path_attaque1)

                            pv_attack = selected_unit.show_attack(self.screen)
                            
                            
                        print(f"pv_attack before SPACE key: {pv_attack}")  # Vérifiez avant SPACE

                        if event.key == pygame.K_SPACE:
                            for enemy in self.enemy_units:
                                if abs(selected_unit.x - enemy.x) <= 1 and abs(selected_unit.y - enemy.y) <= 1:
                                    if pv_attack is not None:  # Vérifiez si une compétence est sélectionnée
                                        print(f"Attacking enemy at ({enemy.x}, {enemy.y}) with competence index: {pv_attack}")
                                        selected_unit.attack(enemy, pv_attack)
                                        print(f"pv_attack after attack: {pv_attack}")
                                    else:
                                        print("Aucune compétence sélectionnée. Attaque annulée.")

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
   # print(f"Personnage sélectionné : {personnage_choisi}")
    
    # Map character to actual instance
    personnages_mapping = {
        "Feu": personnage_feu,
        "Eau": personnage_eau,
        "Foudre": personnage_foudre,
    }
    joueur = personnages_mapping[personnage_choisi]

    # Instanciation du jeu
   # print(type(screen))
    game = Game(screen, joueur)
    #initalisation de l'environement et son
    #play_music(screen)

    # Boucle principale du jeu
    while True:
        game.handle_player_turn()
        game.handle_enemy_turn()
if __name__ == "__main__":
    main()