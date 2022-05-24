from states.state import State

class Lost(State):
	def __init__(self, game):
		super().__init__(game)
		self.count_down_time = 0

	def update(self, actions):
		if self.count_down_time > self.game.FPS * 3:
			while len(self.game.states) > 1:
				self.game.states.pop()
		else:
			self.count_down_time += 1
		
	def render(self, screen):
		self.prev_state.render(screen)