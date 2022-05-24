class State:
	def __init__(self, game):
		self.game = game
		self.prev_state = None

	def update(self, actions):
		pass
		
	def render(self, screen):
		pass

	def enter_state(self):
		if len(self.game.states) > 1:
			self.prev_state = self.game.states[-1]
		self.game.states.append(self)

	def exit_state(self):
		self.game.states.pop()