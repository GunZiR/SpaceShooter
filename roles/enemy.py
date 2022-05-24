import pygame

from roles.ship import Ship
from roles.laser import Laser

class Enemy(Ship):

	COLOR = {'green': (pygame.image.load('assets/alien_green.png'), pygame.image.load('assets/laser_green.png'), 2, 0.5, 7),
	 	'red': (pygame.image.load('assets/alien_red.png'), pygame.image.load('assets/laser_red.png'), 1, 0.6, 10),
	 	'blue': (pygame.image.load('assets/alien_blue.png'),  pygame.image.load('assets/laser_blue.png'), 3, 0.3, 12)
	 	}

	def __init__(self, game, x, y, color):
		super().__init__(game, x, y)
		self.ship_img, self.laser_img, self.lives, self.speed, self.cool_down_time = self.COLOR[color]
		self.mask = pygame.mask.from_surface(self.ship_img)
		self.cool_down = 0

	def move(self):
		self.y += self.speed

	def shoot(self, lasers):
		if self.cool_down <= 0:
			laser = Laser(self.x+self.get_width()/2-self.laser_img.get_width()/2, self.y+self.laser_img.get_height(), self.laser_img, -1.3)
			lasers['enemy'].append(laser)
			self.cool_down = self.game.FPS * self.cool_down_time
		else:
			self.cool_down -= 1