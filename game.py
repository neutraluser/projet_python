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
from unit import manhattan_distance

BLACK=(0,0,0)
WHITE=(255,255,255)

personnage_feu=Personnage("Edan",150,200,"Feu","personnage/feu.png")
personnage_eau=Personnage("Oceane",120,180,"Eau","personnage/eau.png")
personnage_foudre=Personnage("Zeus",110,190,"Foudre","personnage/foudre.png")

class Game:
    def __init__(self,screen,map_instance,joueur1,joueur2):
        self.screen=screen
        self.player_units=[
            Unit(0,6,joueur1.health,1,"player",joueur1.competences,joueur1.chakra,joueur1.affinite,joueur1.image,joueur1.competences.vitesse),
            Unit(1,6,joueur2.health,1,"player",joueur2.competences,joueur2.chakra,joueur2.affinite,joueur2.image,joueur2.competences.vitesse)
        ]

        self.enemy_units=[]
        images=charger_images()
        self.cases=generer_cases(images,map_instance)
        self.trainer=Trainer(self.enemy_units)

    def assign_ia_character(self,joueur_affinite):
        possible_affinites=["Feu","Eau","Foudre"]
        modifiers={
            "Feu":{"Feu":1.0,"Eau":0.8,"Foudre":1.2},
            "Eau":{"Feu":2.0,"Eau":1.0,"Foudre":0.8},
            "Foudre":{"Feu":0.9,"Eau":1.1,"Foudre":1.0}
        }

        best_affinite=None
        best_multiplier=-1
        for aff in possible_affinites:
            mult=modifiers[aff].get(joueur_affinite,1.0)
            if mult>best_multiplier:
                best_multiplier=mult
                best_affinite=aff

        self.trainer.setup_ia_character(best_affinite)
        self.trainer.x=6
        self.trainer.y=6
        self.trainer.add_unit(self.trainer)
        ia_image="personnage/feu.png"
        if self.trainer.affinite=="Feu":
            ia_image="personnage/feu.png"
        elif self.trainer.affinite=="Eau":
            ia_image="personnage/eau.png"
        elif self.trainer.affinite=="Foudre":
            ia_image="personnage/foudre.png"
        u2=Unit(7,6,self.trainer.health,None,"enemy",self.trainer.type_attaque,
                self.trainer.chakra,self.trainer.affinite,ia_image,self.trainer.vitesse)
        self.trainer.add_unit(u2)

    def handle_player_turn(self,map_instance):
        for selected_unit in list(self.player_units):
            def selected_unit_still_valid():
                return selected_unit in self.player_units and selected_unit.health>0

            if not self.player_units:
                # Plus de joueurs, afficher GAME OVER
                self.game_over()
                return

            if not selected_unit_still_valid():
                continue

            has_acted=False
            selected_unit.is_selected=True
            self.flip_display()

            while not has_acted:
                if not self.player_units:
                    # Plus de joueurs, GAME OVER
                    self.game_over()
                    return

                if not selected_unit_still_valid():
                    break

                for event in pygame.event.get():
                    if event.type==pygame.QUIT:
                        pygame.quit()
                        exit()

                    if not selected_unit_still_valid():
                        break

                    if event.type==pygame.KEYDOWN:
                        dx,dy=0,0
                        if event.key==pygame.K_LEFT:
                            dx,dy=-1,0
                        elif event.key==pygame.K_RIGHT:
                            dx,dy=1,0
                        elif event.key==pygame.K_UP:
                            dy=-1
                        elif event.key==pygame.K_DOWN:
                            dy=1

                        if dx!=0 or dy!=0:
                            if not selected_unit_still_valid():
                                break
                            selected_unit.move(dx,dy,map_instance,self.screen)
                            for case in self.cases:
                                if isinstance(case,Soins) and case.case_soin(selected_unit):
                                    self.cases.remove(case)
                                    break
                            has_acted=True
                            selected_unit.is_selected=False
                            self.flip_display()
                            if not selected_unit_still_valid():
                                break

                        elif event.key==pygame.K_a:
                            if not selected_unit_still_valid():
                                break

                            selected_unit.show_attack(self.screen)
                            attack_selected=False
                            attack_id=None
                            while not attack_selected:
                                if not self.player_units:
                                    self.game_over()
                                    return
                                if not selected_unit_still_valid():
                                    break
                                for attack_event in pygame.event.get():
                                    if attack_event.type==pygame.KEYDOWN:
                                        if attack_event.key==pygame.K_1:
                                            attack_id=0
                                            attack_selected=True
                                        elif attack_event.key==pygame.K_2:
                                            attack_id=1
                                            attack_selected=True
                                        elif attack_event.key==pygame.K_3:
                                            # Soin
                                            if selected_unit.chakra>=selected_unit.competences.cout_chakra_sort_soin:
                                                selected_unit.chakra-=selected_unit.competences.cout_chakra_sort_soin
                                                selected_unit.health+=20
                                                print("Le joueur se soigne de 20 PV!")
                                                has_acted=True
                                                selected_unit.is_selected=False
                                                attack_selected=True
                                            else:
                                                print("Pas assez de chakra pour le soin!")
                                        elif attack_event.key==pygame.K_ESCAPE:
                                            attack_selected=True

                            if attack_id is not None and not has_acted and selected_unit_still_valid():
                                # Code d'attaque (portee, aoe)
                                if attack_id==0:
                                    portee = selected_unit.competences.zone_attaque1
                                    aoe = selected_unit.competences.aoe_attaque1
                                    image_path=selected_unit.competences.image_path_attaque1
                                    if selected_unit.chakra<selected_unit.competences.cout_chakra_attaque1:
                                        print("Pas assez de chakra!")
                                        continue
                                else:
                                    portee = selected_unit.competences.zone_attaque2
                                    aoe = selected_unit.competences.aoe_attaque2
                                    image_path=selected_unit.competences.image_path_attaque2
                                    if selected_unit.chakra<selected_unit.competences.cout_chakra_attaque2:
                                        print("Pas assez de chakra!")
                                        continue

                                if not self.player_units:
                                    self.game_over()
                                    return

                                target_x,target_y=selected_unit.x,selected_unit.y
                                selecting_target=True

                                while selecting_target:
                                    if not self.player_units:
                                        self.game_over()
                                        return
                                    if not selected_unit_still_valid():
                                        break
                                    self.flip_display()
                                    if not self.player_units:
                                        self.game_over()
                                        return
                                    if not selected_unit_still_valid():
                                        break
                                    # Affiche la portée possible
                                    for dx2 in range(-portee,portee+1):
                                        for dy2 in range(-portee,portee+1):
                                            if abs(dx2)+abs(dy2)<=portee:
                                                ax=selected_unit.x+dx2
                                                ay=selected_unit.y+dy2
                                                if 0<=ax<GRID_SIZE and 0<=ay<42:
                                                    pygame.draw.rect(self.screen,(200,200,0),(ax*CELL_SIZE,ay*CELL_SIZE,CELL_SIZE,CELL_SIZE),1)
                                    pygame.draw.rect(self.screen,(0,255,0),(target_x*CELL_SIZE,target_y*CELL_SIZE,CELL_SIZE,CELL_SIZE),2)
                                    pygame.display.flip()

                                    for target_event in pygame.event.get():
                                        if not self.player_units:
                                            self.game_over()
                                            return
                                        if not selected_unit_still_valid():
                                            break
                                        if target_event.type==pygame.KEYDOWN:
                                            if target_event.key==pygame.K_LEFT:
                                                target_x=max(0,target_x-1)
                                            elif target_event.key==pygame.K_RIGHT:
                                                target_x=min(GRID_SIZE-1,target_x+1)
                                            elif target_event.key==pygame.K_UP:
                                                target_y=max(0,target_y-1)
                                            elif target_event.key==pygame.K_DOWN:
                                                target_y=min(41,target_y+1)
                                            elif target_event.key==pygame.K_RETURN:
                                                if not self.player_units:
                                                    self.game_over()
                                                    return
                                                if not selected_unit_still_valid():
                                                    break
                                                # Vérifier la portée
                                                if manhattan_distance(selected_unit.x,selected_unit.y,target_x,target_y)>portee:
                                                    print("Cible hors de portée!")
                                                    continue
                                                # Animation du projectile
                                                start=(selected_unit.x,selected_unit.y)
                                                end=(target_x,target_y)
                                                attack_image=pygame.image.load(image_path)
                                                attack_image=pygame.transform.scale(attack_image,(CELL_SIZE,CELL_SIZE))
                                                trajectory=calculate_trajectory(start,end)
                                                fireball_animation(self.screen,attack_image,trajectory,CELL_SIZE)

                                                # AoE autour de (target_x,target_y) avec rayon = aoe
                                                enemies_in_zone=[]
                                                for enemy in self.trainer.enemy_units:
                                                    if manhattan_distance(enemy.x,enemy.y,target_x,target_y)<=aoe:
                                                        enemies_in_zone.append(enemy)

                                                for enemy in enemies_in_zone[:]:
                                                    if not enemy.can_evade(self.trainer.enemy_units,(target_x,target_y),aoe):
                                                        selected_unit.attack(enemy,attack_id)
                                                        if enemy.health<=0:
                                                            self.trainer.enemy_units.remove(enemy)
                                                selecting_target=False
                                                has_acted=True
                                                selected_unit.is_selected=False
                                            elif target_event.key==pygame.K_ESCAPE:
                                                selecting_target=False
                                                break

    def handle_enemy_turn(self):
        if not self.player_units:
            # Si plus de joueurs avant le tour de l'IA
            self.game_over()
            return
        self.trainer.handle_turn(self.player_units,self.screen)
        if not self.player_units:
            # Si plus de joueurs après le tour de l'IA
            self.game_over()
            return

    def flip_display(self):
        BLACK=(0,0,0)
        self.screen.fill(BLACK)
        map_instance=Map("Map1",WIDTH,HEIGHT,self.screen)
        Unit.affiche_stat(self.screen,self.player_units,self.trainer.enemy_units)

        dead_units=[]
        for unit in self.player_units:
            if unit.health<=0:
                dead_units.append(unit)
            else:
                unit.draw(self.screen)

        for unit in self.trainer.enemy_units:
            if unit.health<=0:
                dead_units.append(unit)
            else:
                unit.draw(self.screen)

        for case in self.cases:
            case.afficher_case(self.screen)

        if dead_units:
            skull_image=pygame.image.load("icone/crane.png")
            skull_rect=skull_image.get_rect()
            screen_width,screen_height=WIDTH,HEIGHT
            skull_rect.center=(screen_width//2,screen_height//2)
            self.screen.blit(skull_image,skull_rect)

        pygame.display.flip()

        # Retirer les unités mortes
        for du in dead_units:
            if du in self.player_units:
                self.player_units.remove(du)
            elif du in self.trainer.enemy_units:
                self.trainer.enemy_units.remove(du)

        # Vérifier s'il reste des joueurs
        if not self.player_units:
            self.game_over()

    def game_over(self):
        font = pygame.font.Font(None, 100)
        text_surface = font.render("GAME OVER", True, (255,0,0))
        text_rect = text_surface.get_rect(center=(WIDTH//2, HEIGHT//2))
        self.screen.blit(text_surface, text_rect)
        pygame.display.flip()
        pygame.time.wait(2000)  # Attendre 2 secondes
        pygame.quit()
        exit()

def main():
    global map_instance
    pygame.init()
    screen=pygame.display.set_mode((WIDTH,HEIGHT))
    pygame.display.set_caption("Mon jeu de stratégie")
    map_instance=Map("Map1",WIDTH,HEIGHT,screen)

    ecran_accueil=EcranAccueil(screen)
    ecran_regles=EcranRegles(screen)

    while True:
        result=ecran_accueil.boucle_principale()
        if result=="play":
            break
        elif result=="regles":
            retour=ecran_regles.boucle_principale()
            if retour=="retour":
                continue

    personnage_choisi=selectionner_personnage("joueur 1")
    personnages_mapping={
        "Feu":personnage_feu,
        "Eau":personnage_eau,
        "Foudre":personnage_foudre,
    }
    joueur1=personnages_mapping[personnage_choisi]

    personnage_choisi=selectionner_personnage("joueur 2")
    joueur2=personnages_mapping[personnage_choisi]

    game=Game(screen,map_instance,joueur1,joueur2)
    game.assign_ia_character(joueur1.affinite)

    while True:
        # On vérifie ici aussi, juste au cas où
        if not game.player_units:
            game.game_over()
        game.handle_player_turn(map_instance)
        if not game.player_units:
            game.game_over()
        game.handle_enemy_turn()
        if not game.player_units:
            game.game_over()

if __name__=="__main__":
    main()
