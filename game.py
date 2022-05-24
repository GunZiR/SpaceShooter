import sys

import pygame
from pygame.locals import *

from states.main_menu import MainMenu

class Game:
	def __init__(self):
		pygame.init()
		pygame.display.set_caption('Space Shooter')
		self.WINDOW_SIZE = (400, 600)
		self.screen = pygame.display.set_mode(self.WINDOW_SIZE, 0, 32)
		self.clock = pygame.time.Clock()
		self.FPS = 60
		self.states = []
		self.actions = {'right': False,
						'left': False,
						'up': False,
						'down': False,
						'space': False,
						'click': False}
		
		self.running = True
		self.get_main_menu()

	def run(self):
		while self.running:
			self.get_events()
			self.update()
			self.render()
			self.clock.tick(self.FPS)

	def get_events(self):
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()

			if event.type == KEYDOWN:
				if event.key == K_RIGHT:
					self.actions['right'] = True
				if event.key == K_LEFT:
					self.actions['left'] = True
				if event.key == K_UP:
					self.actions['up'] = True
				if event.key == K_DOWN:
					self.actions['down'] = True
				if event.key == K_SPACE:
					self.actions['space'] = True

			if event.type == KEYUP:
				if event.key == K_RIGHT:
					self.actions['right'] = False
				if event.key == K_LEFT:
					self.actions['left'] = False
				if event.key == K_UP:
					self.actions['up'] = False
				if event.key == K_DOWN:
					self.actions['down'] = False
				if event.key == K_SPACE:
					self.actions['space'] = False

			if event.type == MOUSEBUTTONDOWN:
				if event.button == 1:
					self.actions['click'] = True

	def update(self):
		self.states[-1].update(self.actions)

	def render(self):
		self.states[-1].render(self.screen)
		pygame.display.update()

	def get_main_menu(self):
		first_state = MainMenu(self)
		self.states.append(first_state)

	def reset_keys(self):
		for action in self.actions:
			self.actions[action] = False
