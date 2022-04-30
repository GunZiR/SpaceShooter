import pygame

from collision import collide

alien_green_img = pygame.image.load('assets/alien1.png')
alien_red_img = pygame.image.load('assets/alien2.png')
alien_blue_img = pygame.image.load('assets/alien3.png')

laser_img = pygame.image.load('assets/laser.png')

class Laser:
	def __init__(self, x, y, img):
		self.x = x
		self.y = y
		self.img = img
		self.mask = pygame.mask.from_surface(self.img)

	def draw(self, window):
		window.blit(self.img, (self.x, self.y))

	def move(self, vel):
		self.y -= vel


class Ship:
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.lives = None
		self.ship_img = None
		self.laser_img = None
		#self.laser_speed = None
		self.lasers = []

	def draw(self, window):
		window.blit(self.ship_img, (self.x, self.y))
		for laser in self.lasers:
			laser.draw(window)

	def shoot(self):
		laser = Laser(self.x, self.y, self.laser_img)
		self.lasers.append(laser)

	def get_width(self):
		return self.ship_img.get_width()

	def get_height(self):
		return self.ship_img.get_height()


class Player(Ship):
	def __init__(self, x, y, player_img):
		super().__init__(x, y)
		self.ship_img = player_img
		self.laser_img = laser_img
		self.lives = 10
		self.mask = pygame.mask.from_surface(self.ship_img)
		self.laser_speed = 2

	def move_lasers(self, objs):
		for laser in self.lasers:
			laser.move(self.laser_speed)
			if laser.y <= 0:
				self.lasers.remove(laser)
			else:
				for obj in objs:
					if collide(laser, obj):
						self.lasers.remove(laser)
						obj.lives -= 1
						if obj.lives == 0:
							objs.remove(obj)


class Enemy(Ship):

	COLOR = {'green': (alien_green_img, 2, 0.5), 'red': (alien_red_img, 1, 0.6), 'blue': (alien_blue_img, 3, 0.3)}

	def __init__(self, x, y, color):
		super().__init__(x, y)
		self.ship_img, self.lives, self.vel = self.COLOR[color]
		self.mask = pygame.mask.from_surface(self.ship_img)

	def move(self):
		self.y += self.vel
