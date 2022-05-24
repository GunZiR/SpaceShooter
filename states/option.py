import pygame

from states.state import State

class Option(State):
	def __init__(self, game):
		super().__init__(game)
		self.button1 = pygame.Rect(self.game.WINDOW_SIZE[0]/2 - 100, 100, 200, 50)
		self.button2 = pygame.Rect(self.game.WINDOW_SIZE[0]/2 - 100, 200, 200, 50)
		self.button3 = pygame.Rect(self.game.WINDOW_SIZE[0]/2 - 100, 300, 200, 50)
		self.button4 = pygame.Rect(self.game.WINDOW_SIZE[0]/2 - 100, 400, 200, 50)

	def update(self, actions):
		mouse_pos = pygame.mouse.get_pos()
		if self.button1.collidepoint(mouse_pos):
			if actions['click']:
				print('option 1')
		if self.button2.collidepoint(mouse_pos):
			if actions['click']:
				print('option 2')
		if self.button3.collidepoint(mouse_pos):
			if actions['click']:
				print('option 3')
		if self.button4.collidepoint(mouse_pos):
			if actions['click']:
				self.exit_state()

		self.game.reset_keys()
		
	def render(self, screen):
		pygame.draw.rect(screen, (0, 255, 0), self.button1)
		pygame.draw.rect(screen, (0, 255, 0), self.button2)
		pygame.draw.rect(screen, (0, 255, 0), self.button3)
		pygame.draw.rect(screen, (0, 255, 0), self.button4)