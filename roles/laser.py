import pygame

from acts.collide import collide

class Laser:
	def __init__(self, x, y, img, speed):
		self.x = x
		self.y = y
		self.img = img
		self.speed = speed
		self.mask = pygame.mask.from_surface(self.img)

	def get_width(self):
		return self.img.get_width()

	def get_height(self):
		return self.img.get_height()

	def render(self, screen):
		screen.blit(self.img, (self.x, self.y))

	def move(self):
		self.y -= self.speed
