from states.state import State

class CountDown(State):
	def __init__(self, game, count, to='prev'):
		super().__init__(game)
		self.count_down_time = count
		self.to = to

	def update(self, actions):
		if self.count_down_time * self.game.FPS <= 0:
			if self.to == 'prev':
				self.exit_state()
			elif self.to == 'start':
				while len(self.game.states) > 1:
					self.game.states.pop()
		else:
			self.count_down_time -= 1
		
	def render(self, screen):
		self.prev_state.render(screen)