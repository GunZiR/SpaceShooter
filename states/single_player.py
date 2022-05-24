import random

import pygame

from states.state import State
from states.lost import Lost
from roles.player import Player
from roles.enemy import Enemy
from roles.laser import Laser
from acts.collide import collide

class SinglePlayer(State):
	def __init__(self, game):
		super().__init__(game)
		self.player = Player(self.game)
		self.enemies = []
		self.lasers = {'player': [], 'enemy': []}
		self.wave_len = 0
		self.lvl = 0
		self.lost = False
		self.main_font = pygame.font.SysFont('comicsans', 25)
		self.lost_font = pygame.font.SysFont('comicsans', 30)
		self.bg = pygame.image.load('assets/space.png')
		self.lives_label = self.main_font.render(f'Lives: {self.player.lives}', 1, (255, 255, 255))
		self.lvl_label = self.main_font.render(f'Level: {self.lvl}', 1, (255, 255, 255))
		self.lost_label = self.lost_font.render('You lost!!', 1, (255, 255, 255))

	def update(self, actions):
		self.lives_label = self.main_font.render(f'Lives: {self.player.lives}', 1, (255, 255, 255))
		self.lvl_label = self.main_font.render(f'Level: {self.lvl}', 1, (255, 255, 255))
		if self.player.lives <= 0:
			self.lost = True
			new_state = Lost(self.game)
			new_state.enter_state()

		if len(self.enemies) == 0:
			self.lvl += 1
			self.wave_len += 5
			for i in range(self.wave_len):  # spawn enemies
				enemy = Enemy(self.game, random.randrange(50, 300), random.randrange(-400*self.lvl/2, -20), random.choice(['red', 'green', 'blue']))
				self.enemies.append(enemy)

		self.player.move(actions)
		self.player.cool_down_count()
		if actions['space']:
			self.player.shoot(self.lasers)

		for enemy in self.enemies[:]:
			if enemy.lives == 0:
				self.enemies.remove(enemy)
			enemy.move()
			if enemy.y > 10:
				enemy.shoot(self.lasers)
			if enemy.y >= self.game.WINDOW_SIZE[1]-enemy.get_height():
				self.enemies.remove(enemy)
				self.player.lives -= 1
			elif collide(enemy, self.player):
				self.enemies.remove(enemy)
				self.player.lives -= 1

		for role in self.lasers:
			for laser in self.lasers[role]:
				laser.move()
				if (laser.y <= 0) or (laser.y >= self.game.WINDOW_SIZE[1]-laser.get_height()):
					self.lasers[role].remove(laser)
				else:	
					if role == 'player':
						for enemy in self.enemies:
							if collide(laser, enemy):
								self.lasers['player'].remove(laser)
								enemy.lives -= 1
								
					if role == 'enemy':
						if collide(laser, self.player):
							self.lasers['enemy'].remove(laser)
							self.player.lives -= 1

		
		
	def render(self, screen):
		screen.blit(self.bg, (0, 0))
		screen.blit(self.lvl_label, (0, 0))
		screen.blit(self.lives_label, (self.game.WINDOW_SIZE[0]-self.lives_label.get_width(), 0))
		if self.lost:
			screen.blit(self.lost_label, (self.game.WINDOW_SIZE[0]/2 - self.lost_label.get_width()/2, self.game.WINDOW_SIZE[1]/2))

		for enemy in self.enemies:
			enemy.render(screen)

		self.player.render(screen)

		for role in self.lasers:
			for laser in self.lasers[role]:
				laser.render(screen)

