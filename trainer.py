import random

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

            if enemy.can_evade(player_units):
                enemy.evade()
                continue

            target = self.select_target(player_units)
            if self.can_attack(enemy, target):
                best_attack_id = self.select_best_attack(enemy)
                if best_attack_id is not None:
                    enemy.attack(target, best_attack_id)
                    if target.health <= 0:
                        player_units.remove(target)
            else:
                self.move_towards(enemy, target)

    def select_target(self, player_units):
        return min(player_units, key=lambda u: u.health)

    def can_attack(self, unit, target):
        return abs(unit.x - target.x) <= 1 and abs(unit.y - target.y) <= 1

    def select_best_attack(self, unit):
        viable_attacks = []
        if unit.chakra >= unit.competences.cout_chakra_attaque1:
            viable_attacks.append((0, unit.competences.puissance_attaque1))
        if unit.chakra >= unit.competences.cout_chakra_attaque2:
            viable_attacks.append((1, unit.competences.puissance_attaque2))
        if not viable_attacks:
            return None
        return max(viable_attacks, key=lambda x: x[1])[0]

    def move_towards(self, unit, target):
        dx = 1 if unit.x < target.x else -1 if unit.x > target.x else 0
        dy = 1 if unit.y < target.y else -1 if unit.y > target.y else 0
        # IA move direct, pas besoin de map_instance ni screen
        unit.move(dx, dy)
