import socket
import _pickle as pickle

import pygame

from states.state import State
from states.count_down import CountDown
from roles.player import Player
from roles.enemy import Enemy
from roles.laser import Laser
from utils.collide import collide

class Lobby(State):
	def __init__(self, game):
		super().__init__(game)
		# ------------------------------------------INIT SOCKET--------------------------------------------#
		self.ready = False
		self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.client.connect(("26.21.99.133", 5050))
		self.client.send(str.encode('Hi'))
		
		self.p = self.client.recv(1).decode("utf-8")
		raw_data = self.client.recv(2048)

		data = pickle.loads(raw_data)
		if self.p == '1':
			self.enemy = Player(data['2']['x'], data['2']['y'], data['2']['lives'])
			self.player = Player(data['1']['x'], data['1']['y'], data['1']['lives'])
		elif self.p == '2':
			self.enemy = Player(data['1']['x'], data['1']['y'], data['1']['lives'])
			self.player = Player(data['2']['x'], data['2']['y'], data['2']['lives'])
		print(f'Player {self.p} with ({self.player.x}, {self.player.y}) coordinate')
		# ------------------------------------------INIT IN-GAME STUFF------------------------------------#
		self.lost = False
		self.win = False
		self.start = False
		self.countdown_start = self.game.FPS * 5
		self.lasers = {'player': [], 'enemy': []}
		self.lasers_loc = []
		self.small_font = pygame.font.SysFont('comicsans', 25)
		self.medium_font = pygame.font.SysFont('comicsans', 30)
		self.big_font = pygame.font.SysFont('comicsans', 40)

	def update(self, actions):
		if self.start and self.countdown_start>0:
			new_state = CountDown(self.game, self.countdown_start)
			new_state.enter_state()
		
		if not self.ready:
			if actions['space']:
				self.ready = True
				print(f'Player {self.p} ready!!')
				
		if actions['esc']:
			self.exit_state()
		
		if self.player.lives <= 0:
			self.lost = True
			print(f'You player {self.p} lost!!!')
			new_state = CountDown(self.game, self.game.FPS * 3, to='start')
			new_state.enter_state()

		if self.enemy.lives <= 0:
			self.win = True
			print(f'You player {self.p} Won!!!')
			new_state = CountDown(self.game, self.game.FPS * 3, to='start')
			new_state.enter_state()
		
		if self.start:
			self.player.move(actions)
			self.player.cool_down_count()
			if actions['space'] and self.countdown_start<=0:
				if self.p == '1':
					self.player.shoot(self.lasers, 2)
				else:
					self.player.shoot(self.lasers, -2)

		for role in self.lasers:
			for laser in self.lasers[role]:
				laser.move()
				if (laser.y <= 0) or (laser.y >= self.game.WINDOW_SIZE[1]-laser.get_height()):
					self.lasers[role].remove(laser)
				else:	
					if role == 'player':
						if collide(laser, self.enemy):
							self.lasers['player'].remove(laser)
							self.enemy.lives -= 1
								
					if role == 'enemy':
						if collide(laser, self.player):
							self.lasers['enemy'].remove(laser)
							self.player.lives -= 1
		
	def render(self, screen):
		# ------------------------------------------UPDATE UI----------------------------------------------#
		screen.fill((0, 0, 0))
		self.player_lives_label = self.small_font.render(f'Lives: {self.player.lives}', 1, (255, 255, 255))
		self.enemy_lives_label = self.small_font.render(f'Lives: {self.enemy.lives}', 1, (255, 255, 255))
		# ------------------------------------------SEND DATA----------------------------------------------#
		send_data = {'player':{'x':self.player.x, 'y':self.player.y, 'lives':self.player.lives, 'ready':self.ready},
					 'laser': self.lasers_loc}
		send_data = pickle.dumps(send_data)
		self.client.send(send_data)
		# ------------------------------------------RECIEVE DATA------------------------------------------#
		raw_data = self.client.recv(2048*2)
		data = pickle.loads(raw_data)
		player_data = data['player']
		laser_data = data['laser']
		# ------------------------------------------RENDER GAME-------------------------------------------#
		if self.start:
			screen.blit(self.player_lives_label, (self.game.WINDOW_SIZE[0]/2-self.player_lives_label.get_width()/2, 0))
			screen.blit(self.enemy_lives_label, (self.game.WINDOW_SIZE[0]/2-self.enemy_lives_label.get_width()/2, self.game.WINDOW_SIZE[1]-self.enemy_lives_label.get_height()))
			# ------------------------------------------HANDLE LASERS--------------------------------------#
			self.lasers_loc.clear()
			for laser in self.lasers['player']:
				self.lasers_loc.append({'x': laser.x, 'y': laser.y, 'built':laser.built})

			if self.p == '1':
				for loc in laser_data['2']:
					if not loc['built']:
						laser = Laser(loc['x'], loc['y'], self.enemy.laser_img, -2)
						laser.built = True
						self.lasers['enemy'].append(laser)
			elif self.p == '2':
				for loc in laser_data['1']:
					if not loc['built']:
						laser = Laser(loc['x'], loc['y'], self.enemy.laser_img, 2)
						laser.built = True
						self.lasers['enemy'].append(laser)

			for role in self.lasers:
				for laser in self.lasers[role]:
					laser.render(screen)

		if self.start and self.countdown_start>0:
			self.countdown_label = self.big_font.render(f'{int(self.countdown_start/self.game.FPS)}', 1, (255, 255, 255))
			screen.blit(self.countdown_label, (self.game.WINDOW_SIZE[0]/2 - self.countdown_label.get_width()/2, self.game.WINDOW_SIZE[1]/2))
			self.countdown_start -= 1

		if self.lost:
			self.lost_label = self.medium_font.render('You lost!!!', 1, (255, 255, 255))
			screen.blit(self.lost_label, (self.game.WINDOW_SIZE[0]/2 - self.lost_label.get_width()/2, self.game.WINDOW_SIZE[1]/2))

		if self.win:
			self.win_label = self.medium_font.render('You won!!!', 1, (255, 255, 255))
			screen.blit(self.win_label, (self.game.WINDOW_SIZE[0]/2 - self.win_label.get_width()/2, self.game.WINDOW_SIZE[1]/2))

		if self.p == '1':
			self.enemy.x = player_data['2']['x']
			self.enemy.y = player_data['2']['y']
			self.enemy.lives = player_data['2']['lives']
			enemy_conn = player_data['2']['ready']
		elif self.p == '2':
			self.enemy.x = player_data['1']['x']
			self.enemy.y = player_data['1']['y']
			self.enemy.lives = player_data['1']['lives']
			enemy_conn = player_data['1']['ready']
		
		self.player.render(screen)

		if enemy_conn and self.ready:
			self.start = True

		if enemy_conn:
			self.enemy.render(screen)