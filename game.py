import pygame
import random

from unit import *
from level import *
from animation import *
from EcranAccueil import *
from Soins import *
from Select_perso import selectionner_personnage
from Personnage import *
from EcranRegles import *
from trainer import Trainer

personnage_feu = Personnage("Edan", 150, 200, "Feu", "personnage/feu.png")
personnage_eau = Personnage("Oceane", 120, 180, "Eau","personnage/eau.png")
personnage_foudre = Personnage("Zeus", 110, 190, "Foudre","personnage/foudre.png")

class Game:
    def __init__(self, screen, map_instance, joueur1, joueur2):
        self.screen = screen
        self.player_units = [
            Unit(0, 6, joueur1.health, 1, "player", joueur1.competences, joueur1.chakra, joueur1.affinite, joueur1.image, joueur1.competences.vitesse),
            Unit(1, 6, joueur2.health, 1, "player", joueur2.competences, joueur2.chakra, joueur2.affinite, joueur2.image, joueur2.competences.vitesse)
        ]
        self.enemy_units = []
        images = charger_images()
        self.cases = generer_cases(images, map_instance)

        self.trainer = Trainer(self.enemy_units)

    def assign_ia_character(self, joueur_affinite):
        """
        Choisit l'affinité de l'IA en fonction de l'affinité du joueur pour maximiser les dégâts.
        """
        possible_affinites = ["Feu", "Eau", "Foudre"]
        modifiers = {
            "Feu": {"Eau": 0.8, "Foudre": 1.2, "Feu": 1.0},
            "Eau": {"Feu": 1.5, "Foudre": 0.8, "Eau": 1.0},
            "Foudre": {"Eau": 1.1, "Feu": 0.9, "Foudre": 1.0}
        }

        best_affinite = None
        best_multiplier = -1

        for aff in possible_affinites:
            mult = modifiers.get(aff, {}).get(joueur_affinite, 1.0)
            if mult > best_multiplier:
                best_multiplier = mult
                best_affinite = aff

        # Choix de l'image en fonction de l'affinité IA choisie
        if best_affinite == "Feu":
            ia_image = "personnage/feu.png"
        elif best_affinite == "Eau":
            ia_image = "personnage/eau.png"
        else:
            ia_image = "personnage/foudre.png"

        # Configuration de l'IA
        self.trainer.setup_ia_character(best_affinite)
        self.trainer.add_unit(Unit(6, 6, self.trainer.health, None, "enemy", self.trainer.type_attaque,
                                   self.trainer.chakra, self.trainer.affinite, ia_image, self.trainer.type_attaque.vitesse))
        self.trainer.add_unit(Unit(7, 6, self.trainer.health, None, "enemy", self.trainer.type_attaque,
                                   self.trainer.chakra, self.trainer.affinite, ia_image, self.trainer.type_attaque.vitesse))

    def handle_player_turn(self, map_instance):
        for selected_unit in self.player_units:
            has_acted = False
            selected_unit.is_selected = True
            self.flip_display()

            while not has_acted:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()

                    if event.type == pygame.KEYDOWN:
                        dx, dy = 0, 0
                        if event.key == pygame.K_LEFT:
                            dx, dy = -1, 0
                        elif event.key == pygame.K_RIGHT:
                            dx, dy = 1, 0
                        elif event.key == pygame.K_UP:
                            dy = -1
                        elif event.key == pygame.K_DOWN:
                            dy = 1

                        if dx != 0 or dy != 0:
                            selected_unit.move(dx, dy, map_instance, self.screen)
                            for case in self.cases:
                                if isinstance(case, Soins) and case.case_soin(selected_unit):
                                    self.cases.remove(case)
                                    break
                            has_acted = True
                            selected_unit.is_selected = False
                            self.flip_display()

                        elif event.key == pygame.K_a:
                            selected_unit.show_attack(self.screen)
                            attack_selected = False
                            attack_id = None
                            while not attack_selected:
                                for attack_event in pygame.event.get():
                                    if attack_event.type == pygame.KEYDOWN:
                                        if attack_event.key == pygame.K_1:
                                            attack_id = 0
                                            attack_selected = True
                                        elif attack_event.key == pygame.K_2:
                                            attack_id = 1
                                            attack_selected = True
                                        elif attack_event.key == pygame.K_ESCAPE:
                                            attack_selected = True

                            if attack_id is not None:
                                if attack_id == 0 and selected_unit.chakra < selected_unit.competences.cout_chakra_attaque1:
                                    print("Pas assez de chakra!")
                                    continue
                                if attack_id == 1 and selected_unit.chakra < selected_unit.competences.cout_chakra_attaque2:
                                    print("Pas assez de chakra!")
                                    continue

                                target_x, target_y = selected_unit.x, selected_unit.y
                                selecting_target = True
                                attack_range = selected_unit.competences.zone_attaque1 if attack_id==0 else selected_unit.competences.zone_attaque2

                                while selecting_target:
                                    self.flip_display()
                                    for dx2 in range(-attack_range, attack_range + 1):
                                        for dy2 in range(-attack_range, attack_range + 1):
                                            if abs(dx2) + abs(dy2) <= attack_range:
                                                ax = selected_unit.x + dx2
                                                ay = selected_unit.y + dy2
                                                if 0 <= ax < GRID_SIZE and 0 <= ay < 42:
                                                    pygame.draw.rect(self.screen,(255, 0, 0),(ax*CELL_SIZE, ay*CELL_SIZE, CELL_SIZE, CELL_SIZE),2)
                                    pygame.draw.rect(self.screen,(0, 255, 0),(target_x*CELL_SIZE, target_y*CELL_SIZE, CELL_SIZE, CELL_SIZE),2)
                                    pygame.display.flip()

                                    for target_event in pygame.event.get():
                                        if target_event.type == pygame.KEYDOWN:
                                            if target_event.key == pygame.K_LEFT:
                                                target_x = max(0, target_x - 1)
                                            elif target_event.key == pygame.K_RIGHT:
                                                target_x = min(GRID_SIZE-1, target_x + 1)
                                            elif target_event.key == pygame.K_UP:
                                                target_y = max(0, target_y - 1)
                                            elif target_event.key == pygame.K_DOWN:
                                                target_y = min(41, target_y + 1)
                                            elif target_event.key == pygame.K_RETURN:
                                                if abs(target_x - selected_unit.x)+ abs(target_y - selected_unit.y)<=attack_range:
                                                    for enemy in self.trainer.enemy_units:
                                                        if enemy.x == target_x and enemy.y == target_y:
                                                            selected_unit.attack(enemy, attack_id)
                                                            if enemy.health <= 0:
                                                                self.trainer.enemy_units.remove(enemy)
                                                            self.handle_enemy_turn()
                                                    selecting_target = False
                                                    has_acted = True
                                                    selected_unit.is_selected = False
                                                else:
                                                    print("Cible hors de portée!")
                                            elif target_event.key == pygame.K_ESCAPE:
                                                selecting_target = False
                                                break

    def handle_enemy_turn(self):
        self.trainer.handle_turn(self.player_units, self.screen)

    def flip_display(self):
        BLACK = (0, 0, 0)
        self.screen.fill(BLACK)
        map_instance = Map("Map1", WIDTH, HEIGHT, self.screen)
        Unit.affiche_stat(self.screen, self.player_units, self.trainer.enemy_units)

        for unit in self.player_units + self.trainer.enemy_units:
            if unit.health == 0:
                skull_image = pygame.image.load("icone/crane.png")
                skull_rect = skull_image.get_rect()
                screen_width, screen_height = WIDTH, HEIGHT
                skull_rect.center = (screen_width // 2, screen_height // 2)
                self.screen.blit(skull_image, skull_rect)
                pygame.display.flip()
                if unit in self.player_units:
                    self.player_units.remove(unit)
                else:
                    self.trainer.enemy_units.remove(unit)
            else:
                unit.draw(self.screen)

        for case in self.cases:
            case.afficher_case(self.screen)
        pygame.display.flip()


def main():
    global map_instance
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Mon jeu de stratégie")
    map_instance = Map("Map1", WIDTH, HEIGHT, screen)

    ecran_accueil = EcranAccueil(screen)
    ecran_regles = EcranRegles(screen)

    while True:
        result = ecran_accueil.boucle_principale()
        if result == "play":
            break
        elif result == "regles":
            retour = ecran_regles.boucle_principale()
            if retour == "retour":
                continue

    personnage_choisi = selectionner_personnage("joueur 1")
    personnages_mapping = {
        "Feu": personnage_feu,
        "Eau": personnage_eau,
        "Foudre": personnage_foudre,
    }
    joueur1 = personnages_mapping[personnage_choisi]

    personnage_choisi = selectionner_personnage("joueur 2")
    joueur2 = personnages_mapping[personnage_choisi]

    game = Game(screen, map_instance, joueur1, joueur2)
    game.assign_ia_character(joueur1.affinite)

    while True:
        game.handle_player_turn(map_instance)
        game.handle_enemy_turn()

if __name__ == "__main__":
    main()
