class Ship:

	def __init__(self, game, x, y):
		self.game = game
		self.x = x
		self.y = y
		self.ship_img = None

	def render(self, screen):
		screen.blit(self.ship_img, (self.x, self.y))

	def get_width(self):
		return self.ship_img.get_width()

	def get_height(self):
		return self.ship_img.get_height()