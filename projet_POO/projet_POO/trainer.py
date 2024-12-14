from unit import Unit
from game import *

class Trainer(Unit):
    """
    Classe représentant une IA ou un entraîneur qui contrôle des unités.

    Hérite de la classe Unit pour partager des propriétés et des méthodes communes.
    """

    def __init__(self, x, y, health, attack_power, team, type_attaque, chakra, affinite, sprite_path=None):
        """
        Initialise une instance de Trainer.
        """
        super().__init__(x, y, health, attack_power, team, type_attaque, chakra, affinite, sprite_path)
        self.controlled_units = []  # Liste des unités sous son contrôle

    def add_unit(self, unit):
        """
        Ajoute une unité contrôlée par l'IA.
        """
        self.controlled_units.append(unit)

    def setup_ia_character(self, player_affinite):
        """
        Configure les attributs de l'IA en fonction de l'affinité du joueur.

        Parameters:
        ----------
        player_affinite : str
            L'affinité du joueur (Feu, Eau, Foudre, etc.).
        """
        ia_character = self.choose_character(player_affinite)
        self.health = ia_character["health"]
        self.chakra = ia_character["chakra"]
        self.type_attaque = ia_character["competences"]
        self.affinite = ia_character["affinite"]
        self.sprite = pygame.image.load(ia_character["sprite_path"])
        self.sprite = pygame.transform.scale(self.sprite, (CELL_SIZE, CELL_SIZE))

    def choose_character(self, player_affinite):
        """
        Sélectionne un personnage avec une affinité avantageuse contre le joueur.

        Parameters:
        ----------
        player_affinite : str
            L'affinité du joueur (Feu, Eau, Foudre, etc.).

        Returns:
        -------
        dict
            Dictionnaire contenant les détails du personnage choisi.
        """
        # Définir les affinités opposées
        counter_affinities = {
            "Feu": "Eau",  # L'eau est forte contre le feu
            "Eau": "Foudre",  # La foudre est forte contre l'eau
            "Foudre": "Feu"  # Le feu est fort contre la foudre
        }

        # Obtenir l'affinité de l'IA
        ia_affinite = counter_affinities.get(player_affinite, "Feu")  # Par défaut, l'IA choisit le Feu si rien n'est défini

        # Dictionnaire des personnages IA
        character_data = {
            "Feu": {
                "health": 130,
                "chakra": 210,
                "competences": competences_feu,
                "affinite": "Feu",
                "sprite_path": "sprites/feu.webp"
            },
            "Eau": {
                "health": 120,
                "chakra": 200,
                "competences": competences_eau,
                "affinite": "Eau",
                "sprite_path": "sprites/eau.webp"
            },
            "Foudre": {
                "health": 110,
                "chakra": 190,
                "competences": competences_foudre,
                "affinite": "Foudre",
                "sprite_path": "sprites/foudre.webp"
            }
        }

        return character_data[ia_affinite]
    def can_evade(self, player_units):
    
        for player in player_units:
            # Détection d'une attaque imminente
            if abs(self.x - player.x) <= 1 and abs(self.y - player.y) <= 1:
                if random.random() < 0.3:
                    return True
                    
            
                
        return False


    def handle_turn(self, player_units, screen):
        """
        Gère le tour de chaque unité contrôlée par l'IA.

        Parameters:
        ----------
        player_units : list[Unit]
            Liste des unités du joueur.
        screen : pygame.Surface
            Surface du jeu pour dessiner les actions.
        """
        
        for unit in self.controlled_units:
            unit.evaded_this_turn = False

        for unit in self.controlled_units:
            if not player_units:
                print("Tous les joueurs ont été vaincus. Victoire de l'IA !")
                return
            

            if  unit.can_evade(player_units):  # 30% de chance d'esquiver
                print(f"{unit.team} tente d'esquiver une attaque imminente.")
                unit.evade()
                unit.evaded_this_turn = True
                continue  # Passe à l'unité suivante après l'esquive

        # Si l'IA ne tente pas d'esquiver ou ne peut pas esquiver, elle attaque
            target = self.select_target(player_units)
            print(f"L'IA a sélectionné la cible à ({target.x}, {target.y}) avec {target.health} PV.")

            if self.can_attack(unit, target):  # Vérifie si une attaque est possible
                best_attack_index = self.select_best_attack(unit, target)
                if best_attack_index is not None:
                    unit.attack(target, best_attack_index)
                    print(f"{unit.team} attacked {target.team} at ({target.x}, {target.y}) with {unit.type_attaque[best_attack_index].nom}.")
                    if target.health <= 0:
                        print(f"{target.team} unit at ({target.x}, {target.y}) defeated!")
                        player_units.remove(target)
                    continue  # Passe à l'unité suivante après l'attaque
                else:
                    print("L'IA n'a pas trouvé d'attaque valide.")
            else:
                print(f"L'IA ne peut pas attaquer la cible à ({target.x}, {target.y}).")

        # Sinon, se déplacer vers la cible
            self.move_towards(unit, target)
            print(f"{unit.team} moved closer to ({target.x}, {target.y}).")
          

            

    def select_target(self, player_units):
        """
        Sélectionne la cible prioritaire (ennemi le plus faible).

        Returns:
        -------
        Unit
            L'unité cible.
        """
        return min(player_units, key=lambda unit: unit.health)

    def can_attack(self, unit, target):
        """
        Vérifie si l'unité peut attaquer la cible.

        Returns:
        -------
        bool
            True si l'unité peut attaquer, False sinon.
        """
        return abs(unit.x - target.x) <= 1 and abs(unit.y - target.y) <= 1

    def select_best_attack(self, unit, target):
        """
        Sélectionne la meilleure attaque pour une unité.

        Returns:
        -------
        int
            L'indice de la meilleure attaque.
        """
        best_index = None
        max_damage = 0

        for i, competence in enumerate(unit.type_attaque):
            if competence.cout_chakra <= unit.chakra:  # Vérifie si l'unité a assez de chakra
                damage = competence.puissance  # Ajoutez la logique d'affinité ici si nécessaire
                if damage > max_damage:
                    max_damage = damage
                    best_index = i

        if best_index is not None:
            print(f"{unit.team} selected {unit.type_attaque[best_index].nom} for attack.")
        return best_index

    def move_towards(self, unit, target):
        """
        Déplace l'unité vers la cible.

        Parameters:
        ----------
        unit : Unit
            L'unité à déplacer.
        target : Unit
            La cible vers laquelle se déplacer.
        """
        dx = 1 if unit.x < target.x else -1 if unit.x > target.x else 0
        dy = 1 if unit.y < target.y else -1 if unit.y > target.y else 0
        unit.move(dx, dy)
