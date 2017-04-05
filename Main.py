# Frozen Jam by tgfcoder <https://twitter.com/tgfcoder> licensed under CC-BY-3 
# Art from Kenney.nl

import pygame
import random
from os import path

# Image Directory
img_dir = path.join(path.dirname(__file__), "Assets")
snd_dir = path.join(path.dirname(__file__), "Sound")

# Basic variables
WIDTH = 480
HEIGHT = 550
FPS = 60
POWERUP_TIME = 5000

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Initialize Pygame & Create Window
pygame.init()
pygame.mixer.init()  
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shoot Them")
clock = pygame.time.Clock()

# Font
font_name = pygame.font.match_font('arial')

# Initializing Text Function
def draw_text(surf, text, size, x, y):
	font = pygame.font.Font(font_name, size)
	text_surface = font.render(text, True, WHITE)
	text_rect = text_surface.get_rect()
	text_rect.midtop = (x, y)
	surf.blit(text_surface, text_rect)

# Respawn Mob Function
def new_mob():
	m = Mob()
	all_sprites.add(m)
	mob.add(m)

# Creating/Drawing The Shield Bar
def draw_shield_bar(surf, x, y, pct):
	if pct < 0:
		pct = 0
	BAR_LENGTH = 100
	BAR_HEIGHT = 10
	fill = (pct / 100) * BAR_LENGTH
	outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
	fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
	pygame.draw.rect(surf, BLUE, fill_rect)
	pygame.draw.rect(surf, WHITE, outline_rect, 2)

# Creating/Drawing The Lives
def draw_lives(surf, x, y, lives, img):
	for i in range(lives):
		img_rect = img.get_rect()
		img_rect.x = x + 30 * i
		img_rect.y = y
		surf.blit(img, img_rect)

# Creating/Drawing The Game Over Screen 
def show_waiting_screen():
	screen.blit(background, background_rect)
	draw_text(screen, "Shoot Them!", 64, WIDTH/2, HEIGHT/4)
	draw_text(screen, "Left & Right Arrow Keys to move, Space to fire", 22, WIDTH/2, HEIGHT/2)
	draw_text(screen, "Press a key to begin", 18, WIDTH/2, HEIGHT * 3/4)
	pygame.display.flip()
	waiting = True
	while waiting:
		clock.tick(FPS)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
			if event.type == pygame.KEYUP:
				waiting = False

# Initializing The Player Sprite
class Player(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = player_img
		self.image.set_colorkey(WHITE)
		self.rect = self.image.get_rect()
		self.radius = int(self.rect.width / 2)
		self.rect.centerx = WIDTH / 2
		self.rect.bottom = HEIGHT - 10
		self.xspeed = 0
		self.shield = 100
		self.shoot_delay = 250
		self.last_shot = pygame.time.get_ticks()
		self.lives = 3
		self.hidden = False
		self.hide_timer = pygame.time.get_ticks()
		self.power = 1
		self.power_time = pygame.time.get_ticks()

	def update(self):
		#Timeout For PowerUps
		if self.power >= 3 and pygame.time.get_ticks() - self.power_time > POWERUP_TIME:
			self.power -= 1
			self.power_time = pygame.time.get_ticks()
		if self.power == 2 and pygame.time.get_ticks() - self.power_time > POWERUP_TIME:
			self.power -= 1
			self.power_time = pygame.time.get_ticks()


		# Unhide If Hidden
		if self.hidden and pygame.time.get_ticks() - self.hide_timer > 1500:
			self.hidden = False
			self.rect.centerx = (WIDTH / 2)
			self.rect.bottom = HEIGHT - 10
		self.xspeed = 0
		key_state = pygame.key.get_pressed()

		# Player Controls
		if key_state[pygame.K_LEFT]:
			self.xspeed = -5
		if key_state[pygame.K_RIGHT]:
			self.xspeed = 5

		if key_state[pygame.K_SPACE]:
			self.shoot()
		# Player Speed
		self.rect.x += self.xspeed

		# Boundaries
		if self.rect.right > WIDTH:
			self.rect.right = WIDTH
		if self.rect.left < 0:
			self.rect.left = 0

	def PowerUp(self):
		self.power += 1
		self.power_time = pygame.time.get_ticks()

	def shoot(self):
		now = pygame.time.get_ticks()
		if now - self.last_shot > self.shoot_delay:
			self.last_shot = now
			if self.power == 1:
				bullet = Bullet(self.rect.centerx, self.rect.top)
				all_sprites.add(bullet)
				bullets.add(bullet)
				shoot_sound.play()
			if self.power == 2:
				bullet1 = Bullet(self.rect.left, self.rect.centery)
				bullet2 = Bullet(self.rect.right, self.rect.centery)
				all_sprites.add(bullet1)
				all_sprites.add(bullet2)
				bullets.add(bullet1)
				bullets.add(bullet2)
				shoot_sound.play()
			if self.power >= 3:
				bullet1 = Bullet(self.rect.left, self.rect.centery)
				bullet2 = Bullet(self.rect.centerx, self.rect.top)
				bullet3 = Bullet(self.rect.right, self.rect.centery)
				all_sprites.add(bullet1)
				all_sprites.add(bullet2)
				all_sprites.add(bullet3)
				bullets.add(bullet1)
				bullets.add(bullet2)
				bullets.add(bullet3)
				shoot_sound.play()

	# Temporarily Hides The Player Sprite
	def hide(self):
		self.hidden = True
		self.hide_timer = pygame.time.get_ticks()
		self.rect.center = (WIDTH / 2, HEIGHT + 200)

# Initializing The Enemy Sprites
class Mob(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image_orig = random.choice(meteor_images)
		self.image_orig.set_colorkey(BLACK)
		self.image = self.image_orig.copy()
		self.rect = self.image.get_rect()
		self.radius = int(self.rect.width * 0.85 / 2)
		self.rect.x = random.randrange(WIDTH - self.rect.width)
		self.rect.y = random.randrange(-100, -40)
		self.speedy = random.randrange(1, 8)
		self.speedx = random.randrange(-3, 3)
		self.rot = 0
		self.rot_speed = random.randrange(-8, 8)
		self.last_update = pygame.time.get_ticks()

	def rotate(self):
		current = pygame.time.get_ticks()
		if current - self.last_update > 50:
			self.last_update = current
			self.rot = (self.rot + self.rot_speed) % 360
			new_image = pygame.transform.rotate(self.image_orig, self.rot)
			old_center = self.rect.center
			self.image = new_image
			self.rect = self.image.get_rect()
			self.rect.center = old_center

	def update(self):
		self.rotate()
		self.rect.y += self.speedy
		self.rect.x += self.speedx

		# Off Screen
		if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
			self.rect.x = random.randrange(WIDTH - self.rect.width)
			self.rect.y = random.randrange(-100, -40)
			self.speedy = random.randrange(1, 8)

# Initializing The Bullet Sprites
class Bullet(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.image = laser_img
		self.image.set_colorkey(BLACK)
		self.rect = self.image.get_rect()
		self.rect.bottom = y
		self.rect.centerx = x
		self.speedy = -10

	def update(self):
		self.rect.y += self.speedy

		# Removes The Sprite Once Off Screen
		if self.rect.bottom < 0:
			self.kill()

# Initializing The PowerUp Sprites
class PowerUp(pygame.sprite.Sprite):
	def __init__(self, center):
		pygame.sprite.Sprite.__init__(self)
		self.type = random.choice(["shield", "gun"])
		self.image = powerup_images[self.type]
		self.image.set_colorkey(BLACK)
		self.rect = self.image.get_rect()
		self.rect.center = center
		self.speedy = 4

	def update(self):
		self.rect.y += self.speedy

		# Removes The Sprite Once Off Screen
		if self.rect.top > HEIGHT:
			self.kill()

# Initializing The Explosion Sprites
class Explosion(pygame.sprite.Sprite):
	def __init__(self, center, size):
		pygame.sprite.Sprite.__init__(self)
		self.size = size
		self.image = explosion_animation[self.size][0]
		self.rect = self.image.get_rect()
		self.rect.center = center
		self.frame = 0
		self.last_update = pygame.time.get_ticks()
		self.frame_rate = 75

	def update(self):
		current = pygame.time.get_ticks()
		if current - self.last_update > self.frame_rate:
			self.last_update = current
			self.frame += 1
			if self.frame == len(explosion_animation[self.size]):
				self.kill()
			else:
				center = self.rect.center
				self.image = explosion_animation[self.size][self.frame]
				self.rect = self.image.get_rect()
				self.rect.center = center

# Initialize Game Graphics
background = pygame.image.load(path.join(img_dir, "background.png")).convert()
background_rect = background.get_rect()

player_img = pygame.image.load(path.join(img_dir, "playerShip1_red.png")).convert()
player_mini_img = pygame.transform.scale(player_img, (25, 19))
player_mini_img.set_colorkey(WHITE)

laser_img = pygame.image.load(path.join(img_dir, "laserRed16.png")).convert()

meteor_images = []
meteor_list = [
	"meteorBrown_big1.png", "meteorBrown_big2.png", "meteorBrown_big3.png", "meteorBrown_big4.png",
	"meteorBrown_med1.png", "meteorBrown_med3.png", "meteorBrown_small1.png", "meteorBrown_small1.png",
	"meteorBrown_tiny1.png", "meteorBrown_tiny2.png"
]
for img in meteor_list:
	meteor_images.append(pygame.image.load(path.join(img_dir, img)).convert())

powerup_images = {}
powerup_images["shield"] = pygame.image.load(path.join(img_dir, "shield_gold.png")).convert()
powerup_images["gun"] = pygame.image.load(path.join(img_dir, "bolt_gold.png")).convert()

# Creating The Explosion Animation	
explosion_animation = {}
explosion_animation["lg"] = []
explosion_animation['sm'] = []
explosion_animation["player"] = []
for i in range(9):
	filename = "regularExplosion0{}.png".format(i)
	img = pygame.image.load(path.join(img_dir, filename)).convert()
	img.set_colorkey(BLACK)
	img_lg = pygame.transform.scale(img, (75, 75))
	explosion_animation["lg"].append(img_lg)
	img_sm = pygame.transform.scale(img, (32, 32))
	explosion_animation["sm"].append(img_sm)

	filename = "sonicExplosion0{}.png".format(i)
	img = pygame.image.load(path.join(img_dir, filename)).convert()
	img.set_colorkey(BLACK)
	explosion_animation["player"].append(img)

# Initialize Game Sound
shoot_sound  = pygame.mixer.Sound(path.join(snd_dir, "Laser.wav"))
shield_sound  = pygame.mixer.Sound(path.join(snd_dir, "shield.wav"))
power_sound  = pygame.mixer.Sound(path.join(snd_dir, "power.wav"))
expl_sounds = []
for snd in ["Explosion1.wav", "Explosion2.wav"]:
	expl_sounds.append(pygame.mixer.Sound(path.join(snd_dir, snd)))
player_die_sound = pygame.mixer.Sound(path.join(snd_dir, "rumble1.ogg"))
pygame.mixer.music.load(path.join(snd_dir, "bgm.ogg"))
pygame.mixer.music.set_volume(0.4)

pygame.mixer.music.play(loops = -1)

# Game Loop
running = True
game_over = True
while running:
	if game_over:
		show_waiting_screen()
		game_over = False

		# Actual Group That Is Used To Show The Images On The Screen
		all_sprites = pygame.sprite.Group()
		mob = pygame.sprite.Group()
		bullets = pygame.sprite.Group()
		powerups = pygame.sprite.Group()
		player = Player()
		all_sprites.add(player)

		for i in range(8):
			new_mob()

		score = 0

	# Keep Loop Running At The Right Speed
	clock.tick(FPS)

	# Process Input (events)
	for event in pygame.event.get():
		# Checks For Closing Window
		if event.type == pygame.QUIT:
			running = False

	# Update
	all_sprites.update()

	# Looks For Collision Between Bullets & Mob
	hits = pygame.sprite.groupcollide(mob, bullets, True, True)
	for hit in hits:
		score += 50 - hit.radius
		random.choice(expl_sounds).play()
		expl = Explosion(hit.rect.center, "lg")
		all_sprites.add(expl)
		if random.random() > 0.9:
			power = PowerUp(hit.rect.center)
			all_sprites.add(power)
			powerups.add(power)
		new_mob()

	# Looks For Collision Between Player & Mob
	hits = pygame.sprite.spritecollide(player, mob, True, pygame.sprite.collide_circle)
	for hit in hits:
		player.shield -= hit.radius * 2
		expl = Explosion(hit.rect.center, "sm")
		all_sprites.add(expl)
		new_mob()
		if player.shield <= 0:
			player_die_sound.play()
			death = Explosion(player.rect.center, "player")
			all_sprites.add(death)
			player.hide()
			player.lives -= 1
			player.Shield = 100

	# Looks For Collision Between Player & PowerUp
	hits = pygame.sprite.spritecollide(player, powerups, True)
	for hit in hits:
		if hit.type == "shield":
			player.shield += random.randrange(10, 50)
			shield_sound.play()
			if player.shield >= 100:
				player.shield = 100
		if hit.type == "gun":
			player.PowerUp()
			power_sound.play()

	# Player Is Dead & Explosion Animaiton Is Done
	if player.lives == 0 and not death.alive():
		game_over = True

	# Draw/Render
	screen.fill(BLACK)
	screen.blit(background, background_rect)
	all_sprites.draw(screen)
	draw_text(screen, str(score), 18, WIDTH/2, 10)
	draw_shield_bar(screen, 5, 5, player.shield)
	draw_lives(screen, WIDTH - 100, 5, player.lives, player_mini_img)
	# Alway Do The Flip Last (after drawing everything)
	pygame.display.flip()

pygame.quit()