# import pygame
import pygame
import random

from pygame.locals import (
   RLEACCEL,
   K_UP,
   K_DOWN,
   K_LEFT,
   K_RIGHT,
   K_ESCAPE,
   KEYDOWN,
   QUIT,
)

# initialize pygame
pygame.init()

# setup screen
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Draw screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# create a player sprite
class Player(pygame.sprite.Sprite):

   def __init__(self) -> None:
      super(Player, self).__init__()
      self.surf = pygame.image.load("ship.jpg").convert()
      self.surf.set_colorkey((255, 255, 255), RLEACCEL)
      self.rect = self.surf.get_rect()

   def update(self, pressed_keys):
      if pressed_keys[K_UP]:
         self.rect.move_ip(0, -5)
      if pressed_keys[K_DOWN]:
         self.rect.move_ip(0, 5)
      if pressed_keys[K_RIGHT]:
         self.rect.move_ip(5, 0)
      if pressed_keys[K_LEFT]:
         self.rect.move_ip(-5, 0)

      # keep player within play area
      if self.rect.left < 0:
         self.rect.left = 0
      if self.rect.right > SCREEN_WIDTH:
         self.rect.right = SCREEN_WIDTH
      if self.rect.top <= 0:
         self.rect.top = 0
      if self.rect.bottom > SCREEN_HEIGHT:
         self.rect.bottom = SCREEN_HEIGHT

# create an enemy class
class Enemy(pygame.sprite.Sprite):

   def __init__(self) -> None:
      super(Enemy, self).__init__()
      self.surf = pygame.image.load("enemy.jpg").convert()
      self.surf.set_colorkey((255, 255, 255), RLEACCEL)
      self.rect = self.surf.get_rect(
         center = (
            random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
            random.randint(0, SCREEN_HEIGHT)
         )
      )
      self.speed = random.randint(5, 20)

   def update(self):
      self.rect.move_ip(-self.speed, 0)
      if self.rect.left < 0:
         self.kill()

# create a cloud class
class Cloud(pygame.sprite.Sprite):

   def __init__(self) -> None:
      super(Cloud, self).__init__()
      self.surf = pygame.image.load("cloud.jpg").convert()
      self.surf.set_colorkey((255, 255, 255), RLEACCEL)
      self.rect = self.surf.get_rect()

      # The starting position is randomly generated
      self.rect = self.surf.get_rect(
         center=(
            random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
            random.randint(0, SCREEN_HEIGHT),
         )
      )

   # update clouds
   def update(self):
      self.rect.move_ip(-5, 0)
      if self.rect.left < 0:
         self.kill()


# Create a custom event for adding a new enemy
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 250)
# create custom event to add clouds
ADDCLOUD = pygame.USEREVENT + 2
pygame.time.set_timer(ADDCLOUD, 1000)

# create player object 
player = Player()

# Create groups to hold enemy sprites and all sprites
# - enemies is used for collision detection and position updates
# - all_sprites is used for rendering
enemies = pygame.sprite.Group()
clouds = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

# create new surface
scr = pygame.Surface((50, 50))

# color sufrace
scr.fill((0, 0, 0))
rect = scr.get_rect()

# draw surface to screen
surf_center = (
   (SCREEN_WIDTH - scr.get_width()) / 2,
   (SCREEN_HEIGHT - scr.get_height()) / 2

)

# set up game state
running = True

# setup gameloop
while running:

   for event in pygame.event.get():
      if event.type == KEYDOWN:
         if event.key == K_ESCAPE:
            running = False

      elif event.type == QUIT:
         running = False

      # create new enemy
      elif event.type == ADDENEMY:
         new_enemy = Enemy()
         enemies.add(new_enemy)
         all_sprites.add(new_enemy)

      # create clouds
      elif event.type == ADDCLOUD:
         new_cloud = Cloud()
         clouds.add(new_cloud)
         all_sprites.add(new_cloud)

   # get key pressed
   pressed_keys = pygame.key.get_pressed()

   # update player position
   player.update(pressed_keys)

   # update enemies position
   enemies.update()

   # update clouds position
   clouds.update()

   # fill the screen
   screen.fill((135, 206, 250))

   # draw player
   # Draw all sprites
   for entity in all_sprites:
      screen.blit(entity.surf, entity.rect)

   # Check if any enemies have collided with the player
   if pygame.sprite.spritecollideany(player, enemies):
      # If so, then remove the player and stop the loop
      player.kill()
      running = False

   # Setup the clock for a decent framerate
   clock = pygame.time.Clock()

   # Ensure program maintains a rate of 30 frames per second
   clock.tick(35)

   # flip display
   pygame.display.flip()