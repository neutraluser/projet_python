import pygame
import random
from competences import *

pygame.init()

screen_info = pygame.display.Info()
screen_width = screen_info.current_w
screen_height = screen_info.current_h

CELL_SIZE = min(screen_height // 42, screen_width // 72)
GRID_SIZE = 72
LARGEUR_GRILLE = GRID_SIZE * CELL_SIZE
HEIGHT = 42 * CELL_SIZE
WIDTH = LARGEUR_GRILLE
FPS = 30
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

def manhattan_distance(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)

class Unit:
    def __init__(self, x, y, health, attack_power, team, competences, chakra, affinite, image, vitesse):
        self.x = x
        self.y = y
        self.health = health
        if affinite == "Feu":
            self.defense = 50
        elif affinite == "Eau":
            self.defense = 60
        elif affinite == "Foudre":
            self.defense = 70
        else:
            self.defense = 50
        self.attack_power = attack_power
        self.team = team
        self.is_selected = False
        self.competences = competences
        self.chakra = chakra
        self.affinite = affinite
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, (CELL_SIZE, CELL_SIZE))
        self.vitesse = vitesse

    @staticmethod
    def ajuster_degats(base_puissance, affinite_attaque, affinite_cible):
        modifiers = {
            "Feu": {"Feu":1.0,"Eau":0.8,"Foudre":1.2},
            "Eau": {"Feu":2.0,"Eau":1.0,"Foudre":0.8},
            "Foudre": {"Feu":0.9,"Eau":1.1,"Foudre":1.0}
        }
        aff_attack = affinite_attaque if affinite_attaque in modifiers else "Feu"
        aff_target = affinite_cible if affinite_cible in modifiers[aff_attack] else "Feu"
        mult = modifiers[aff_attack].get(aff_target, 1.0)
        return base_puissance * mult

    def can_evade(self, enemies, attack_center, attack_range):
        if self.team == "enemy":
            dist = manhattan_distance(self.x, self.y, attack_center[0], attack_center[1])
            if dist <= attack_range:
                r = random.random()
                print(f"DEBUG: Chance d'esquive = {r}, si <0.5 alors esquive garantie.")
                if r < 0.5:
                    # Esquive garantie
                    directions = [(-1,0),(1,0),(0,-1),(0,1)]
                    random.shuffle(directions)
                    found_spot = False
                    for dx, dy in directions:
                        new_x = self.x+dx
                        new_y = self.y+dy
                        # Trouver une case hors de la zone
                        if manhattan_distance(new_x,new_y,attack_center[0],attack_center[1]) > attack_range:
                            self.x = new_x
                            self.y = new_y
                            print(f"{self.team} esquive et se déplace vers ({self.x}, {self.y}). Esquive garantie.")
                            found_spot = True
                            break
                    if not found_spot:
                        # Pas de case sûre trouvée, mais esquive garantie
                        # On reste sur place, pas de dégâts
                        print(f"{self.team} esquive quand même (pas de dégâts) sans se déplacer, esquive garantie.")
                    return True
                else:
                    print(f"{self.team} n'essaie pas d'esquiver (r>=0.5), subit les dégâts.")
                    return False
            else:
                return False
        else:
            return False

    def move(self, dx, dy, map_instance=None, screen=None):
        if map_instance is None or screen is None:
            new_x = self.x+dx
            new_y = self.y+dy
            if 0<=new_x<(LARGEUR_GRILLE / CELL_SIZE) and 0<=new_y<(HEIGHT / CELL_SIZE):
                self.x=new_x
                self.y=new_y
            return

        L=map_instance.Liste_obstacles
        L_eau=map_instance.Liste_vide
        life=True
        mouvan = False
        for i in range(len(map_instance.liste_coin_mouvan)):
            if [self.x, self.y] in map_instance.liste_coin_mouvan:
                mouvan = True

        if (mouvan):
            max_moves = int(self.vitesse / 2)
        else:
            max_moves = self.vitesse
        possible_moves = []
        for ddx in range(-max_moves,max_moves+1):
            for ddy in range(-max_moves,max_moves+1):
                if abs(ddx)+abs(ddy)<=max_moves:
                    new_x=self.x+ddx
                    new_y=self.y+ddy
                    if 0<=new_x<(LARGEUR_GRILLE/CELL_SIZE) and 0<=new_y<(HEIGHT/CELL_SIZE):
                        if [new_x,new_y] not in L:
                            possible_moves.append((new_x,new_y))

        selector_x,selector_y=self.x,self.y
        running=True
        while running:
            screen.fill(BLACK)
            map_image=pygame.image.load(map_instance.fond)
            map_image=pygame.transform.scale(map_image,(WIDTH,HEIGHT))
            screen.blit(map_image,(0,0))

            for move_x,move_y in possible_moves:
                rect=pygame.Rect(move_x*CELL_SIZE,move_y*CELL_SIZE,CELL_SIZE,CELL_SIZE)
                pygame.draw.rect(screen,(200,255,0),rect,1)

            selector_rect=pygame.Rect(selector_x*CELL_SIZE,selector_y*CELL_SIZE,CELL_SIZE,CELL_SIZE)
            pygame.draw.rect(screen,(0,0,255),selector_rect,2)
            screen.blit(self.image,(self.x*CELL_SIZE,self.y*CELL_SIZE))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_LEFT:
                        selector_x=max(0,selector_x-1)
                    elif event.key==pygame.K_RIGHT:
                        selector_x=min(LARGEUR_GRILLE//CELL_SIZE -1,selector_x+1)
                    elif event.key==pygame.K_UP:
                        selector_y=max(0,selector_y-1)
                    elif event.key==pygame.K_DOWN:
                        selector_y=min(HEIGHT//CELL_SIZE -1,selector_y+1)
                    elif event.key==pygame.K_RETURN:
                        if (selector_x,selector_y) in possible_moves:
                            self.x=selector_x
                            self.y=selector_y
                            for i in range(len(L_eau)):
                                if (self.x==L_eau[i][0] and self.y==L_eau[i][1]):
                                    life=False
                            if not life:
                                self.health=0
                            running=False
                    elif event.key==pygame.K_ESCAPE:
                        running=False

    def show_attack(self,screen):
        font_title=pygame.font.Font(None,36)
        font_subtitle=pygame.font.Font(None,15)
        text_color=(196,15,0)

        image_paths=[self.competences.image_path_attaque1,self.competences.image_path_attaque2,self.competences.image_path_sort_soin]
        images=[]
        for path in image_paths:
            img=pygame.image.load(path)
            img=pygame.transform.scale(img,(100,100))
            images.append(img)

        image_titles=[self.competences.nom_attaque1,self.competences.nom_attaque2,self.competences.nom_sort_soin]

        dx=self.x*CELL_SIZE
        dy=self.y*CELL_SIZE

        image_spacing=20
        start_x=dx+20
        start_y=dy+50

        button_rects=[]
        for i in range(len(images)):
            button_rect=pygame.Rect(start_x+i*(100+image_spacing),start_y,100,100)
            button_rects.append(button_rect)

        frame_rect=pygame.Rect(dx,dy,700,200)
        frame_color=(133,133,133)
        frame_width=2

        transparent_surface=pygame.Surface((frame_rect.width,frame_rect.height),pygame.SRCALPHA)
        frame_color_with_alpha=(frame_color[0],frame_color[1],frame_color[2],128)
        transparent_surface.fill(frame_color_with_alpha)
        screen.blit(transparent_surface,(frame_rect.x,frame_rect.y))
        pygame.draw.rect(screen,frame_color,frame_rect,width=frame_width)

        title_surface=font_title.render(f"Techniques (1,2) + Soin(3): {self.affinite}",True,text_color)
        title_x=frame_rect.x+(frame_rect.width - title_surface.get_width())//2
        title_y=frame_rect.y+10
        screen.blit(title_surface,(title_x,title_y))

        for i,(img,rect) in enumerate(zip(images,button_rects)):
            screen.blit(img,rect.topleft)
            subtitle_surface=font_subtitle.render(image_titles[i],True,text_color)
            subtitle_x=rect.x+(rect.width -subtitle_surface.get_width())//2
            subtitle_y=rect.y+rect.height+10
            screen.blit(subtitle_surface,(subtitle_x,subtitle_y))

        pygame.display.flip()

    def attack(self,target,attack_id=None):
        if attack_id is None:
            base_puissance=1
        else:
            if attack_id==0:
                if self.chakra<self.competences.cout_chakra_attaque1:
                    print("Pas assez de chakra pour l'attaque 1!")
                    return
                self.chakra-=self.competences.cout_chakra_attaque1
                base_puissance=self.competences.puissance_attaque1
            elif attack_id==1:
                if self.chakra<self.competences.cout_chakra_attaque2:
                    print("Pas assez de chakra pour l'attaque 2!")
                    return
                self.chakra-=self.competences.cout_chakra_attaque2
                base_puissance=self.competences.puissance_attaque2

        dmg=Unit.ajuster_degats(base_puissance,self.affinite,target.affinite)
        print(f"DEBUG: Attaquant={self.affinite}, Cible={target.affinite}, Base={base_puissance}, Dmg={dmg}")

        if target.defense>0:
            if target.defense>=dmg:
                target.defense-=dmg
                dmg=0
            else:
                dmg-=target.defense
                target.defense=0
        if dmg>0:
            target.health-=dmg
            if target.health<0:
                target.health=0
        print(f"{self.team} attaque {target.team} ! Santé: {target.health}, Défense: {target.defense}")

    def draw(self,screen):
        if self.health==0:
            skull_image=pygame.image.load("icone/crane.png")
            skull_rect=skull_image.get_rect()
            screen_width,screen_height=WIDTH,HEIGHT
            skull_rect.center=(screen_width//2,screen_height//2)
            screen.blit(skull_image,skull_rect)
        else:
            screen.blit(self.image,(self.x*CELL_SIZE,self.y*CELL_SIZE))

    @staticmethod
    def affiche_stat(screen,player_units,enemy_units):
        font=pygame.font.Font(None,22)
        for unit in player_units:
            texte_defense=f"DEF:{int(unit.defense)}"
            text_surface_def=font.render(texte_defense,True,(255,255,0))
            screen.blit(text_surface_def,(unit.x * CELL_SIZE + CELL_SIZE, unit.y * CELL_SIZE - CELL_SIZE - 20))

            texte_health=f"{unit.health}"
            text_surface_health=font.render(texte_health,True,(255,255,255))
            screen.blit(text_surface_health,(unit.x * CELL_SIZE + CELL_SIZE, unit.y * CELL_SIZE - CELL_SIZE))

            texte_chakra=f"{unit.chakra}"
            text_surface_chakra=font.render(texte_chakra,True,(255,255,255))
            screen.blit(text_surface_chakra,(unit.x * CELL_SIZE + CELL_SIZE, unit.y * CELL_SIZE))

        for unit in enemy_units:
            texte_defense=f"DEF:{int(unit.defense)}"
            text_surface_def=font.render(texte_defense,True,(255,255,0))
            screen.blit(text_surface_def,(unit.x * CELL_SIZE + CELL_SIZE, unit.y * CELL_SIZE - CELL_SIZE - 20))

            texte_health=f"{unit.health}"
            text_surface_health=font.render(texte_health,True,(255,255,255))
            screen.blit(text_surface_health,(unit.x * CELL_SIZE + CELL_SIZE, unit.y * CELL_SIZE - CELL_SIZE))

            texte_chakra=f"{unit.chakra}"
            text_surface_chakra=font.render(texte_chakra,True,(255,255,255))
            screen.blit(text_surface_chakra,(unit.x * CELL_SIZE + CELL_SIZE, unit.y * CELL_SIZE))
