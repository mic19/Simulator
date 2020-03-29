from enum import Enum
from math import sqrt


def is_close(a: float, b: float, diff=0.05) -> bool:
	if abs(a - b) < diff:
		return True
	return False


class Person:
	class State(Enum):
		Healthy = 0
		Infected = 1
		Ill = 2
		Convalescent = 3
		Dead = 4

	class MovementState(Enum):
		Idle = 0
		GoingTo = 1

	mobile_people = []

	def __init__(self, x_pos: float, y_pos: float, state=State.Healthy):
		self.x = x_pos
		self.y = y_pos
		self.state = state
		self.expose_time = 0
		self.incubation_time = 0
		self.reconvalescence_time = 0

		self.movement_state = Person.MovementState.Idle
		self.destination = None
		self.x_step_share = 0
		self.y_step_share = 0

	def move(self, dx: float, dy: float):
		self.x += dx
		self.y += dy

	def move_to_destination(self, dx: float, dy: float):
		if self.movement_state is Person.MovementState.GoingTo:
			if is_close(self.x, self.destination[0], dx) and is_close(self.y, self.destination[1], dy):
				self.movement_state = Person.MovementState.Idle
				Person.mobile_people.remove(self)
			else:
				self.move(self.x_step_share * (dx + dy), self.y_step_share * (dx + dy))

	def set_destination(self, x: float, y: float):
		if self.movement_state is Person.MovementState.Idle:
			self.movement_state = Person.MovementState.GoingTo
			self.destination = (x, y)
			self.mobile_people.append(self)

			a = self.destination[0] - self.x
			b = self.destination[1] - self.y
			r = sqrt(a ** 2 + b ** 2)

			self.x_step_share = a / r
			self.y_step_share = b / r

	def expose(self, dt: float):
		self.expose_time += dt

	def reconvalesce(self, dt: float):
		self.reconvalescence_time += dt

	def increase_incubation(self, dt):
		self.incubation_time += dt

	def infect(self):
		if self.state is Person.State.Healthy:
			self.state = Person.State.Infected

	def ill(self):
		if self.state is Person.State.Infected:
			self.state = Person.State.Ill

	def cure(self):
		if self.state is Person.State.Ill:
			self.state = Person.State.Convalescent

	def kill(self):
		if self.state is Person.State.Ill:
			self.state = Person.State.Dead

	def get_expose_time(self):
		return self.expose_time

	def get_incubation_time(self) -> float:
		return self.incubation_time

	def get_recon_time(self) -> float:
		return self.reconvalescence_time

	def get_distance_from(self, other: 'Person') -> float:
		return sqrt((self.x - other.x)**2 + (self.y - other.y)**2)
