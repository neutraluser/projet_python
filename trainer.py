import random
import pygame
from animation import fireball_animation, calculate_trajectory
from unit import*

class Trainer:
    def __init__(self, enemy_units, competences_feu=None, competences_eau=None, competences_foudre=None):
        self.enemy_units = enemy_units
        self.competences_feu = competences_feu
        self.competences_eau = competences_eau
        self.competences_foudre = competences_foudre
        self.health = None
        self.chakra = None
        self.type_attaque = None
        self.affinite = None

    def setup_ia_character(self, affinite):
        from competences import Competence
        if affinite == "Feu":
            c = Competence("Feu")
            self.health = 130
            self.chakra = 210
            self.affinite = "Feu"
            self.type_attaque = c
        elif affinite == "Eau":
            c = Competence("Eau")
            self.health = 120
            self.chakra = 200
            self.affinite = "Eau"
            self.type_attaque = c
        elif affinite == "Foudre":
            c = Competence("Foudre")
            self.health = 110
            self.chakra = 190
            self.affinite = "Foudre"
            self.type_attaque = c
        else:
            c = Competence("Feu")
            self.health = 130
            self.chakra = 210
            self.affinite = "Feu"
            self.type_attaque = c

    def add_unit(self, unit):
        self.enemy_units.append(unit)

    def handle_turn(self, player_units, screen):
        if not player_units:
            return

        for enemy in self.enemy_units:
            if not player_units:
                break

            target = self.select_target(player_units)

            if self.can_attack(enemy, target):
                best_attack_id = self.select_best_attack_by_power(enemy)
                if best_attack_id is not None:
                    self.perform_attack(enemy, target, best_attack_id, screen)
                else:
                    self.move_towards(enemy, target)
            else:
                if random.random() < 0.3:
                    best_attack_id = self.select_best_attack_distance(enemy, target)
                    if best_attack_id is not None:
                        self.perform_attack(enemy, target, best_attack_id, screen)
                    else:
                        self.move_towards(enemy, target)
                else:
                    self.move_towards(enemy, target)

    def select_target(self, player_units):
        return min(player_units, key=lambda u: u.health)

    def can_attack(self, unit, target):
        return abs(unit.x - target.x) <= 1 and abs(unit.y - target.y) <= 1

    def select_best_attack_by_power(self, unit):
        viable_attacks = []
        if unit.chakra >= unit.competences.cout_chakra_attaque1:
            viable_attacks.append((0, unit.competences.puissance_attaque1))
        if unit.chakra >= unit.competences.cout_chakra_attaque2:
            viable_attacks.append((1, unit.competences.puissance_attaque2))
        if not viable_attacks:
            return None
        viable_attacks.sort(key=lambda x: x[1], reverse=True)
        return viable_attacks[0][0]

    def select_best_attack_distance(self, unit, target):
        distance = abs(unit.x - target.x) + abs(unit.y - target.y)
        attacks = []
        zone1 = unit.competences.zone_attaque1
        dmg1 = unit.competences.puissance_attaque1
        if zone1 >= distance and unit.chakra >= unit.competences.cout_chakra_attaque1:
            attacks.append((0, zone1, dmg1))

        zone2 = unit.competences.zone_attaque2
        dmg2 = unit.competences.puissance_attaque2
        if zone2 >= distance and unit.chakra >= unit.competences.cout_chakra_attaque2:
            attacks.append((1, zone2, dmg2))

        if not attacks:
            return None
        attacks.sort(key=lambda x: (x[1], x[2]), reverse=True)
        return attacks[0][0]

    def move_towards(self, unit, target):
        dx = 1 if unit.x < target.x else -1 if unit.x > target.x else 0
        dy = 1 if unit.y < target.y else -1 if unit.y > target.y else 0
        unit.move(dx, dy)

    def perform_attack(self, enemy, target, attack_id, screen):
        start = (enemy.x, enemy.y)
        end = (target.x, target.y)
        trajectory = calculate_trajectory(start, end)

        if attack_id == 0:
            attack_image_path = enemy.competences.image_path_attaque1
        else:
            attack_image_path = enemy.competences.image_path_attaque2

        attack_image = pygame.image.load(attack_image_path)
        attack_image = pygame.transform.scale(attack_image, (CELL_SIZE, CELL_SIZE))

        fireball_animation(screen, attack_image, trajectory, CELL_SIZE)
        enemy.attack(target, attack_id)
