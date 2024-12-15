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


personnage_feu = Personnage("Edan", 150, 200, "Feu", "personnage/feu.png")
personnage_eau = Personnage("Oceane", 120, 180, "Eau","personnage/eau.png")
personnage_foudre = Personnage("Zeus", 110, 190, "Foudre","personnage/foudre.png")
class Game:
    def __init__(self, screen,map_instance, joueur1,joueur2):




        self.screen = screen #position(x,y)
        self.player_units = [
            Unit(0, 6, joueur1.health, 1, "player", None, joueur1.chakra, joueur1.affinite, joueur1.image, joueur1.competences.vitesse),
            Unit(0, 6, joueur2.health, 1, "player", None, joueur2.chakra, joueur2.affinite, joueur2.image, joueur2.competences.vitesse)
        ]
        # Dictionnaire associant les types aux images
        association_image = {
            "Feu": "personnage/feu.png",
            "Eau": "personnage/eau.png",
            "Foudre": "personnage/foudre.png"
        }

        types_possibles = ["Feu", "Eau", "Foudre"]
        type_ennemi1 = random.choice(types_possibles)
        type_ennemi2 = random.choice(types_possibles)

        # Utilisation de l'image associée à chaque type d'ennemi
        image_ennemi1 = association_image[type_ennemi1]
        image_ennemi2 = association_image[type_ennemi2]

        self.enemy_units = [
            Unit(3, 7, 120, 20, "enemy", Competence(type_ennemi1), 200, type_ennemi1, image_ennemi1,6),
            Unit(2, 8, 120, 20, "enemy", Competence(type_ennemi2), 200, type_ennemi2, image_ennemi2,6)
        ]
        
        ##### MODIF CLASS SOINS
        # Charger les images des cases de soin
        images = charger_images()
        # Générer les cases de soin
        self.cases = generer_cases(images, map_instance)  # Liste des cases de soin
        #########
        
    def handle_player_turn(self, map_instance):
        """Tour du joueur"""
        for selected_unit in self.player_units:
            has_acted = False  # Le tour du joueur n'est pas encore terminé
            selected_unit.is_selected = True
            self.flip_display()  # Mise à jour de l'affichage initial
    
            while not has_acted:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
    
                    if event.type == pygame.KEYDOWN:
                        # Déplacement du personnage ou choix d'action
                        dx, dy = 0, 0
                        if event.key == pygame.K_LEFT:
                            dx, dy = -1, 0
                        elif event.key == pygame.K_RIGHT:
                            dx, dy = 1, 0
                        elif event.key == pygame.K_UP:
                            dx, dy = 0, -1
                        elif event.key == pygame.K_DOWN:
                            dx, dy = 0, 1
    
                        # Si un mouvement est effectué
                        if dx != 0 or dy != 0:
                            selected_unit.move(dx, dy, map_instance, self.screen)
    
                            # Vérifier si le personnage est sur une case de soin
                            for case in self.cases:
                                if isinstance(case, Soins) and case.case_soin(selected_unit):
                                    #print(f"{selected_unit.nom} a récupéré des PV grâce à une case de soin !")
                                    self.cases.remove(case)  # Retirer la case de soin après utilisation
                                    break  # Une seule case de soin par déplacement
    
                            has_acted = True
                            selected_unit.is_selected = False
                            self.flip_display()  # Mise à jour de l'affichage après déplacement
    
                        # Si l'on appuie sur la touche 'A', on passe à la sélection de l'attaque
                        elif event.key == pygame.K_a:
                            selected_unit.show_attack(self.screen)
    
                            # Affichage des compétences et choix de l'attaque
                            #print(f"Compétences disponibles pour {selected_unit.nom}:")
                            #print(f"1: {selected_unit.competences.nom_attaque1} (Puissance: {selected_unit.competences.puissance_attaque1}, Coût: {selected_unit.competences.cout_chakra_attaque1})")
                            #print(f"2: {selected_unit.competences.nom_attaque2} (Puissance: {selected_unit.competences.puissance_attaque2}, Coût: {selected_unit.competences.cout_chakra_attaque2})")
    
                            # Attente du choix de l'attaque par le joueur
                            attack_selected = False
                            while not attack_selected:
                                for attack_event in pygame.event.get():
                                    if attack_event.type == pygame.KEYDOWN:
                                        if attack_event.key == pygame.K_1:
                                            attack_range = selected_unit.competences.zone_attaque1
                                            attack_power = selected_unit.competences.puissance_attaque1
                                            chakra_cost = selected_unit.competences.cout_chakra_attaque1
                                            attack_selected = True
                                        elif attack_event.key == pygame.K_2:
                                            attack_range = selected_unit.competences.zone_attaque2
                                            attack_power = selected_unit.competences.puissance_attaque2
                                            chakra_cost = selected_unit.competences.cout_chakra_attaque2
                                            attack_selected = True
                                        elif attack_event.key == pygame.K_ESCAPE:
                                            attack_selected = True  # Annuler si ESC est pressé
    
                            if selected_unit.chakra < chakra_cost:
                                print("Pas assez de chakra !")
                                continue
    
                            selected_unit.chakra -= chakra_cost
                            target_x, target_y = selected_unit.x, selected_unit.y
                            selecting_target = True
    
                            while selecting_target:
                                # Effacer l'écran et redessiner la zone d'attaque
                                self.flip_display()
    
                                # Dessiner la zone d'attaque
                                for dx in range(-attack_range, attack_range + 1):
                                    for dy in range(-attack_range, attack_range + 1):
                                        if abs(dx) + abs(dy) <= attack_range:
                                            attack_x = selected_unit.x + dx
                                            attack_y = selected_unit.y + dy
                                            if 0 <= attack_x < GRID_SIZE and 0 <= attack_y < 42:
                                                pygame.draw.rect(
                                                    self.screen,
                                                    (255, 0, 0),  # Couleur rouge
                                                    (attack_x * CELL_SIZE, attack_y * CELL_SIZE, CELL_SIZE, CELL_SIZE),
                                                    2
                                                )
    
                                # Dessiner la cible actuelle
                                pygame.draw.rect(
                                    self.screen,
                                    (0, 255, 0),  # Couleur verte
                                    (target_x * CELL_SIZE, target_y * CELL_SIZE, CELL_SIZE, CELL_SIZE),
                                    2
                                )
                                pygame.display.flip()
    
                                for target_event in pygame.event.get():
                                    if target_event.type == pygame.KEYDOWN:
                                        if target_event.key == pygame.K_LEFT:
                                            target_x = max(0, target_x - 1)
                                        elif target_event.key == pygame.K_RIGHT:
                                            target_x = min(GRID_SIZE - 1, target_x + 1)
                                        elif target_event.key == pygame.K_UP:
                                            target_y = max(0, target_y - 1)
                                        elif target_event.key == pygame.K_DOWN:
                                            target_y = min(41, target_y + 1)
                                        elif target_event.key == pygame.K_RETURN:
                                            # Lancer l'attaque sur la cible sélectionnée
                                            if abs(target_x - selected_unit.x) + abs(target_y - selected_unit.y) <= attack_range:
                                                for enemy in self.enemy_units:
                                                    if enemy.x == target_x and enemy.y == target_y:
                                                        enemy.health -= attack_power
                                                        print(f"Attaque réussie ! PV restants : {enemy.health}")
                                                        if enemy.health <= 0:
                                                            print("Ennemi vaincu !")
                                                            self.enemy_units.remove(enemy)
                                                selecting_target = False
                                                has_acted = True
                                                selected_unit.is_selected = False
                                            else:
                                                print("Cible hors de portée !")
                                        elif target_event.key == pygame.K_ESCAPE:
                                            selecting_target = False
                                            break



    def handle_enemy_turn(self,map_instance):
        """IA très simple pour les ennemis."""
        for enemy in self.enemy_units:

            # Déplacement aléatoire
            target = random.choice(self.player_units)
            dx = 1 if enemy.x < target.x else -1 if enemy.x > target.x else 0
            dy = 1 if enemy.y < target.y else -1 if enemy.y > target.y else 0
            enemy.move(dx, dy,map_instance,self.screen)

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
        map_instance = Map("Map1", WIDTH, HEIGHT, self.screen)
       # level_map(self.screen, HEIGHT, LARGEUR_GRILLE)
        Unit.affiche_stat(self, self.screen)

        for x in range(0, LARGEUR_GRILLE, CELL_SIZE):
            for y in range(0, HEIGHT, CELL_SIZE):
                rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
                #pygame.draw.rect(self.screen, WHITE, rect, 1)


        # Affiche les unités
        for unit in self.player_units + self.enemy_units:
            if(unit.health==0):
                skull_image = pygame.image.load(
                    "icone/crane.png")  # Assurez-vous que le fichier skull.png est dans le bon répertoire
                skull_rect = skull_image.get_rect()

                # Centrer l'image sur l'écran
                screen_width, screen_height = WIDTH, HEIGHT
                skull_rect.center = (screen_width // 2, screen_height // 2)

                # Afficher l'image du crâne
                self.screen.blit(skull_image, skull_rect)
                pygame.display.flip()
                self.player_units.remove(unit)
            else:
                cache=False
                L_cache=map_instance.Liste_cache
                for i in range(len(L_cache)):
                    if (unit.x==L_cache[i][0] and unit.y==L_cache[i][1]):
                        cache=True
                if(cache):
                    pass
                else:
                    unit.draw(self.screen)

        ##### MODIF CLASS SOINS
        # Affiche les cases de soin
        for case in self.cases:  
            case.afficher_case(self.screen)
        ##### MODIF CLASS SOINS
        
        for unit in self.player_units:
            if unit.is_selected:
                # Zoom sur l'unité
                zoom_size = 0 # Taille de la zone zoomée (5x5 cellules)
                if(zoom_size):
                    half_zoom = zoom_size // 2

                    # Calculer la zone à zoomer
                    x_start = max(0, unit.x - half_zoom) * CELL_SIZE
                    y_start = max(0, unit.y - half_zoom) * CELL_SIZE
                    zoom_width = zoom_size * CELL_SIZE
                    zoom_height = zoom_size * CELL_SIZE

                    # Découper la zone zooméettttr4
                    zoom_rect = pygame.Rect(x_start, y_start, zoom_width, zoom_height)
                    zoom_surface = self.screen.subsurface(zoom_rect)

                    # Redimensionner pour occuper tout l'écran
                    zoom_surface_resized = pygame.transform.scale(
                        zoom_surface, (WIDTH, HEIGHT)
                    )
                    self.screen.blit(zoom_surface_resized, (0, 0))


        pygame.display.flip()


def main():
    global map_instance

    # Initialisation de Pygame
    pygame.init()
    # Instanciation de la fenêtre
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Mon jeu de stratégie")
    map_instance = Map("Map1", WIDTH, HEIGHT, screen)

    # Instanciation des écrans (association simple)
    ecran_accueil = EcranAccueil(screen)
    ecran_regles = EcranRegles(screen)

    # Boucle principale pour gérer la navigation entre les écrans
    while True:
        result = ecran_accueil.boucle_principale()

        if result == "play":
            # Si le bouton PLAY est cliqué, lancer le jeu
            print("Lancement du jeu...")
            break
        elif result == "regles":
            # Si le bouton RÈGLES est cliqué, afficher l'écran des règles
            retour = ecran_regles.boucle_principale()
            if retour == "retour":
                # Retourne à l'écran d'accueil
                continue

    # Lancement du jeu après l'écran d'accueil
    from game import Game  # Importer Game ici pour éviter les imports circulaires

    # Sélection des personnages
    personnage_choisi = selectionner_personnage("joueur 1")
    personnages_mapping = {
        "Feu": personnage_feu,
        "Eau": personnage_eau,
        "Foudre": personnage_foudre,
    }
    joueur1 = personnages_mapping[personnage_choisi]

    personnage_choisi = selectionner_personnage("joueur 2")
    joueur2 = personnages_mapping[personnage_choisi]

    # Instanciation du jeu
    game = Game(screen, map_instance, joueur1, joueur2)

    # Boucle principale du jeu
    while True:
        game.handle_player_turn(map_instance)
        game.handle_enemy_turn(map_instance)

if __name__ == "__main__":
    main()

