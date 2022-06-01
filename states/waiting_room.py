import random
import socket
import _pickle as pickle

import pygame

from states.state import State
#from states.multiplayer import MultiPlayer
from roles.player import Player
from roles.enemy import Enemy
from roles.laser import Laser
from acts.collide import collide

class WaitingRoom(State):
	def __init__(self, game):
		#print('Start init')
		super().__init__(game)
		self.ready = False
		self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.client.connect(("26.21.99.133", 5050))
		self.client.send(str.encode('Hi'))
		
		self.p = self.client.recv(1).decode("utf-8")
		raw_data = self.client.recv(2048)

		data = pickle.loads(raw_data)
		if self.p == '1':
			self.player = Player(data['1']['x'], data['1']['y'], data['1']['lives'])
			self.enemy = Player(data['2']['x'], data['2']['y'], data['2']['lives'])
		elif self.p == '2':
			self.player = Player(data['2']['x'], data['2']['y'], data['2']['lives'])
			self.enemy = Player(data['1']['x'], data['1']['y'], data['1']['lives'])
		self.lost = False
		self.start = False
		print(f'Player {self.p} with ({self.player.x}, {self.player.y}) coordinate')
		#print('Finish init')

	def update(self, actions):
		#print('Start update')
		'''
		if not self.ready:
			if actions['space']:
				self.ready = True
				print(f'Player {self.p} ready!!')
		
		if self.player.lives <= 0:
			self.lost = True
			new_state = Lost(self.game)
			new_state.enter_state()
		'''
		#if self.start:
		self.player.move(actions)
		#self.player.cool_down_count()
		# if actions['space']:
			# self.player.shoot(self.lasers)
		
		#print('End update')
		
	def render(self, screen):
		#print('Start sending data')
		send_data = {'x':self.player.x, 'y':self.player.y, 'lives':self.player.lives, 'ready':self.ready}
		send_data = pickle.dumps(send_data)  # {'x':x, 'y':y, 'lives':lives, 'ready':False}
		self.client.send(send_data)
		#print('Sent data')
		#print('Start render')
		#print('Start recieve data')
		raw_data = self.client.recv(2048)
		#print('Recieved data')
		data = pickle.loads(raw_data)
		if self.p == '1':
			self.enemy.x = data['2']['x']
			self.enemy.y = data['2']['y']
			self.enemy.lives = data['2']['lives']
			enemy_conn = data['2']['ready']
		elif self.p == '2':
			self.enemy.x = data['1']['x']
			self.enemy.y = data['1']['y']
			self.enemy.lives = data['1']['lives']
			enemy_conn = data['1']['ready']
		screen.fill((0, 0, 0))
		self.player.render(screen)
		#if enemy_conn:
		self.enemy.render(screen)
		#print('End render')