import pygame

from act import collide

alien_green_img = pygame.image.load('assets/alien_green.png')
alien_red_img = pygame.image.load('assets/alien_red.png')
alien_blue_img = pygame.image.load('assets/alien_blue.png')

laser_yellow_img = pygame.image.load('assets/laser_yellow.png')
laser_green_img = pygame.image.load('assets/laser_green.png')
laser_red_img = pygame.image.load('assets/laser_red.png')
laser_blue_img = pygame.image.load('assets/laser_blue.png')

class Laser:
	def __init__(self, x, y, img, speed):
		self.x = x
		self.y = y
		self.img = img
		self.speed = speed
		self.mask = pygame.mask.from_surface(self.img)

	def draw(self, window):
		window.blit(self.img, (self.x, self.y))

	def move(self):
		self.y -= self.speed

	def get_width(self):
		return self.img.get_width()

	def get_height(self):
		return self.img.get_height()


class Ship:
	lasers = {'player': [], 'enemy': []}

	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.lives = None
		self.ship_img = None
		self.laser_img = None

	def draw(self, window):
		window.blit(self.ship_img, (self.x, self.y))
		for role in self.lasers:
			for laser in self.lasers[role]:
				laser.draw(window)

	def get_width(self):
		return self.ship_img.get_width()

	def get_height(self):
		return self.ship_img.get_height()


class Player(Ship):
	def __init__(self, x, y, player_img):
		super().__init__(x, y)
		self.ship_img = player_img
		self.laser_img = laser_yellow_img
		self.lives = 10
		self.mask = pygame.mask.from_surface(self.ship_img)
		self.cool_down = 0
		self.cool_down_time = 1

	def shoot(self):
		laser = Laser(self.x+self.get_width()/2-self.laser_img.get_width()/2, self.y, self.laser_img, 2)
		super().lasers['player'].append(laser)


class Enemy(Ship):

	COLOR = {'green': (alien_green_img, laser_green_img, 2, 0.5, 7),
	 	'red': (alien_red_img, laser_red_img, 1, 0.6, 10),
	 	'blue': (alien_blue_img, laser_blue_img, 3, 0.3, 12)
	 	}

	def __init__(self, x, y, color):
		super().__init__(x, y)
		self.ship_img, self.laser_img, self.lives, self.vel, self.cool_down_count = self.COLOR[color]
		self.mask = pygame.mask.from_surface(self.ship_img)
		self.cool_down = 0 

	def move(self):
		self.y += self.vel

	def shoot(self):
		if self.cool_down == 0:
			laser = Laser(self.x+self.get_width()/2-self.laser_img.get_width()/2, self.y+self.laser_img.get_height(), self.laser_img, -1.3)
			super().lasers['enemy'].append(laser)
			self.cool_down = 60 * self.cool_down_count
		else:
			self.cool_down -= 1