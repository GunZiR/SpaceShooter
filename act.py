import pygame

def collide(obj1, obj2):
	offset_x = obj2.x - obj1.x
	offset_y = obj2.y - obj1.y
	return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None


def move_lasers(lasers, player, objs, height):
	for laser in lasers['player'][:]:
		laser.move()
		if laser.y <= 0:
			lasers['player'].remove(laser)
		else:
			for obj in objs:
				if collide(laser, obj):
					lasers['player'].remove(laser)
					obj.lives -= 1
					if obj.lives == 0:
						objs.remove(obj)

	for laser in lasers['enemy'][:]:
		laser.move()
		if laser.y >= height-laser.get_height():
			lasers['enemy'].remove(laser)
		else:
			if collide(laser, player):
				lasers['enemy'].remove(laser)
				player.lives -= 1