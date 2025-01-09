import pygame
import pytmx
import pyscroll

from player import Player

class Game:

    def __init__(self):

        # Creer la fenetre du jeu
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Pygamon Game")

        # Initialiser la carte actuelle
        self.map = "world"

        # Charger la carte (tmx)
        tmx_data = pytmx.util_pygame.load_pygame("carte.tmx")
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 2

        # Generer un joueur
        player_position = tmx_data.get_object_by_name("player")
        self.player = Player(player_position.x, player_position.y)

        # Definir une liste qui va stocker les rectangles de collision
        self.walls = []

        for obj in tmx_data.objects:
            if obj.type == "collision":
                self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        # Dessiner le groupe de calques
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=5)
        self.group.add(self.player)

        # Definir le rect de collision pour entrer dans la maison
        enter_house1 = tmx_data.get_object_by_name("enter_house1")
        self.enter_house1_rect = pygame.Rect(enter_house1.x, enter_house1.y, enter_house1.width, enter_house1.height)

    def hundle_input(self):
        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_UP]:
            self.player.move_up()
            self.player.change_animation("up")
        elif pressed[pygame.K_DOWN]:
            self.player.move_down()
            self.player.change_animation("down")
        elif pressed[pygame.K_LEFT]:
            self.player.move_left()
            self.player.change_animation("left")
        elif pressed[pygame.K_RIGHT]:
            self.player.move_right()
            self.player.change_animation("right")

    def switch_house1(self):
         # Charger la carte (tmx)
        tmx_data = pytmx.util_pygame.load_pygame("house1.tmx")
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 2

        # Definir une liste qui va stocker les rectangles de collision
        self.walls = []

        for obj in tmx_data.objects:
            if obj.type == "collision":
                self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        # Dessiner le groupe de calques
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=5)
        self.group.add(self.player)

        # Definir le rect de collision pour entrer dans la maison
        enter_house1 = tmx_data.get_object_by_name("exit_house1")
        self.enter_house1_rect = pygame.Rect(enter_house1.x, enter_house1.y, enter_house1.width, enter_house1.height)

        # Recuperer le point de spawn dans la maison
        spawn_house1_point = tmx_data.get_object_by_name("spawn_house1")
        self.player.position[0] = spawn_house1_point.x
        self.player.position[1] = spawn_house1_point.y - 20

    def switch_world(self):
            # Charger la carte (tmx)
            tmx_data = pytmx.util_pygame.load_pygame("carte.tmx")
            map_data = pyscroll.data.TiledMapData(tmx_data)
            map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
            map_layer.zoom = 2

            # Definir une liste qui va stocker les rectangles de collision
            self.walls = []

            for obj in tmx_data.objects:
                if obj.type == "collision":
                    self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

            # Dessiner le groupe de calques
            self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=5)
            self.group.add(self.player)

            # Definir le rect de collision pour entrer dans la maison
            enter_house1 = tmx_data.get_object_by_name("enter_house1")
            self.enter_house1_rect = pygame.Rect(enter_house1.x, enter_house1.y, enter_house1.width, enter_house1.height)

            # Recuperer le point de spawn devant la maison
            spawn_house1_point = tmx_data.get_object_by_name("enter_house1_exit")
            self.player.position[0] = spawn_house1_point.x
            self.player.position[1] = spawn_house1_point.y + 20

    def update(self):
        self.group.update()

        # verifier l'entree dans la maison
        if self.map == "world" and self.player.feet.colliderect(self.enter_house1_rect):
            self.switch_house1()
            self.map = "house1"

            # verifier la sortie de la maison
        if self.map == "house1" and self.player.feet.colliderect(self.enter_house1_rect):
            self.switch_world()
            self.map = "world"

        # Verification collision
        for sprite in self.group.sprites():
            if sprite.feet.collidelist(self.walls) > -1:
                sprite.move_back()

    def run(self):

        clock = pygame.time.Clock()

        # Boucle du jeu
        running = True

        while running:

            self.player.save_location()
            self.hundle_input()
            self.update()
            self.group.center(self.player.rect.center)
            self.group.draw(self.screen)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            clock.tick(60)

        pygame.quit()