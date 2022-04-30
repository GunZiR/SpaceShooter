import sys, math, random

import pygame
from pygame.locals import *

from character import Player, Enemy
from collision import collide

pygame.init()

WINDOW_SIZE = (400, 600)

screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)

clock = pygame.time.Clock()

pygame.display.set_caption('Space Shooter')

main_font = pygame.font.SysFont('comicsans', 25)
lost_font = pygame.font.SysFont('comicsans', 30)

player_img = pygame.image.load('assets/spaceship.png')

bg = pygame.image.load('assets/space.png')

player_location = [WINDOW_SIZE[0]/2 - player_img.get_width()/2, 500]

player = Player(player_location[0], player_location[1], player_img)

moving_right = False
moving_left = False
moving_up = False
moving_down = False

enemies = []
wave_len = 0
lvl = 0
lost = False
lost_count = 0
fps = 60

run = True

while run:

	if len(enemies) == 0:
		lvl += 1
		wave_len += 5
		for i in range(wave_len):  # spawn enemies
			enemy = Enemy(random.randrange(50, 300), random.randrange(-400*lvl/2, -20), random.choice(['red', 'green', 'blue']))
			enemies.append(enemy)

	lives_label = main_font.render(f'Lives: {player.lives}', 1, (255, 255, 255))
	lvl_label = main_font.render(f'Level: {lvl}', 1, (255, 255, 255))

	screen.blit(bg, (0, 0))
	screen.blit(lvl_label, (0, 0))
	screen.blit(lives_label, (WINDOW_SIZE[0]-lives_label.get_width(), 0))
	
	if moving_right and player.x<(WINDOW_SIZE[0]-player.get_width()):  # move right
		player.x += 4
	if moving_left and player.x>0:  # move left
		player.x -= 4
	if moving_up and player.y>0:  # move up
		player.y -= 4
	if moving_down and player.y<(WINDOW_SIZE[1]-player.get_height()):  # move down
		player.y += 4

	for event in pygame.event.get():
		if event.type == QUIT:
			#pygame.quit()
			#sys.exit()
			run = False

		if event.type == KEYDOWN:
			if event.key == K_RIGHT:
				moving_right = True
			if event.key == K_LEFT:
				moving_left = True
			if event.key == K_UP:
				moving_up = True
			if event.key == K_DOWN:
				moving_down = True
			if event.key == K_SPACE:
				player.shoot()

		if event.type == KEYUP:
			if event.key == K_RIGHT:
				moving_right = False
			if event.key == K_LEFT:
				moving_left = False
			if event.key == K_UP:
				moving_up = False
			if event.key == K_DOWN:
				moving_down = False

	for enemy in enemies[:]:
		enemy.move()
		if enemy.y >= WINDOW_SIZE[1]-enemy.get_height():
			enemies.remove(enemy)
			player.lives -= 1
		elif collide(enemy, player):
			enemies.remove(enemy)
			player.lives -= 1

	for enemy in enemies:
		enemy.draw(screen)

	player.move_lasers(enemies)

	player.draw(screen)

	if player.lives <= 0:
		lost = True
		lost_count += 1

	if lost:
		lost_label = lost_font.render('You lost!!', 1, (255, 255, 255))
		screen.blit(lost_label, (WINDOW_SIZE[0]/2 - lost_label.get_width()/2, WINDOW_SIZE[1]/2))

	if lost:
		if lost_count > fps * 3:
			run = False
		else:
			continue

			
	pygame.display.update()
	clock.tick(fps)