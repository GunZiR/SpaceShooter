import pygame

from roles.ship import Ship
from roles.laser import Laser

class Player(Ship):
	def __init__(self, game):
		self.ship_img = pygame.image.load('assets/spaceship.png')
		super().__init__(game, game.WINDOW_SIZE[0]/2 - self.ship_img.get_width()/2, 500)
		self.ship_img = pygame.image.load('assets/spaceship.png')
		self.laser_img = pygame.image.load('assets/laser_yellow.png')
		self.lives = 10
		self.mask = pygame.mask.from_surface(self.ship_img)
		self.cool_down = 0
		self.cool_down_time = 0.2

	def move(self, actions):
		if actions['right'] and self.x<(self.game.WINDOW_SIZE[0]-self.get_width()):  # move right
			self.x += 4
		if actions['left'] and self.x>0:  # move left
			self.x -= 4
		if actions['up'] and self.y>0:  # move up
			self.y -= 4
		if actions['down'] and self.y<(self.game.WINDOW_SIZE[1]-self.get_height()):  # move down
			self.y += 4

	def shoot(self, lasers):
		if self.cool_down <= 0:
			self.cool_down = self.game.FPS * self.cool_down_time
			laser = Laser(self.x+self.get_width()/2-self.laser_img.get_width()/2, self.y, self.laser_img, 2)
			lasers['player'].append(laser)

	def cool_down_count(self):
		if self.cool_down > 0:
			self.cool_down -= 1