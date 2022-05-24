import sys

import pygame

from states.state import State
from states.single_player import SinglePlayer
from states.option import Option

class MainMenu(State):
	def __init__(self, game):
		super().__init__(game)
		self.click = False
		self.button1 = pygame.Rect(self.game.WINDOW_SIZE[0]/2 - 100, 200, 200, 50)
		self.button2 = pygame.Rect(self.game.WINDOW_SIZE[0]/2 - 100, 300, 200, 50)
		self.button3 = pygame.Rect(self.game.WINDOW_SIZE[0]/2 - 100, 400, 200, 50)

	def update(self, actions):
		mouse_pos = pygame.mouse.get_pos()
		if self.button1.collidepoint(mouse_pos):
			if actions['click']:
				new_state = SinglePlayer(self.game)
				new_state.enter_state()

		elif self.button2.collidepoint(mouse_pos):
			if actions['click']:
				new_state = Option(self.game)
				new_state.enter_state()

		elif self.button3.collidepoint(mouse_pos):
			if actions['click']:
				pygame.quit()
				sys.exit()

		actions['click'] = False

	def render(self, screen):
		screen.fill((0, 0, 0))
		pygame.draw.rect(screen, (255, 255, 255), self.button1)
		pygame.draw.rect(screen, (255, 255, 255), self.button2)
		pygame.draw.rect(screen, (255, 255, 255), self.button3)