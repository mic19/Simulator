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
		Quarantined = 2

	mobile_people = []
	idle_people = []
	quarantined_people = []

	healthy_people = []
	infected_people = []
	ill_people = []
	convalescent_people = []
	dead_people = []

	def __init__(self, x_pos: float, y_pos: float, state=State.Healthy):
		self.x = x_pos
		self.y = y_pos
		self.state = state
		self.expose_time = 0
		self.incubation_time = 0
		self.reconvalescence_time = 0
		self.incubation_needed = None  # time needed to get sick after infection
		self.recovery_needed = None

		self.movement_state = Person.MovementState.Idle
		self.destination = None
		self.x_step_share = 0
		self.y_step_share = 0

		self.healthy_people.append(self)
		self.idle_people.append(self)

	def move(self, dx: float, dy: float):
		self.x += dx
		self.y += dy

	def move_to_destination(self, dx: float, dy: float):
		if self.movement_state is Person.MovementState.GoingTo:
			if is_close(self.x, self.destination[0], dx) and is_close(self.y, self.destination[1], dy):
				self.movement_state = Person.MovementState.Idle
				Person.mobile_people.remove(self)
				Person.idle_people.append(self)
			else:
				self.move(self.x_step_share * (dx + dy), self.y_step_share * (dx + dy))

	def set_destination(self, x: float, y: float):
		if self.movement_state is Person.MovementState.Idle:
			self.movement_state = Person.MovementState.GoingTo
			self.destination = (x, y)
			Person.mobile_people.append(self)
			Person.idle_people.remove(self)

			a = self.destination[0] - self.x
			b = self.destination[1] - self.y
			r = sqrt(a ** 2 + b ** 2)

			self.x_step_share = a / r
			self.y_step_share = b / r

	def expose(self, dt: float):
		self.expose_time += dt

	def reconvalesce(self, dt: float):
		self.reconvalescence_time += dt

	def increase_incubation(self, dt: float):
		self.incubation_time += dt
		if self.incubation_time >= self.incubation_needed:
			self.ill()

	def quarantine(self):
		if self.state is Person.State.Infected or self.state is Person.State.Ill:
			self.movement_state = Person.MovementState.Quarantined
			Person.quarantined_people.append(self)

	def unquarantine(self):
		self.movement_state = Person.MovementState.Idle
		if self in Person.quarantined_people:
			Person.quarantined_people.remove(self)

	def run_away(self, dx: float, dy: float, other: 'Person'):
		if self.x >= other.x:
			self.x += dx
		else:
			self.x -= dx

		if self.y >= other.y:
			self.y += dy
		else:
			self.y -= dy

	def infect(self, incubation_needed: float, recovery_needed: float):
		self.incubation_needed = incubation_needed
		self.recovery_needed = recovery_needed
		if self.state is Person.State.Healthy:
			self.state = Person.State.Infected
			Person.healthy_people.remove(self)
			Person.infected_people.append(self)

	def ill(self):
		if self.state is Person.State.Infected:
			self.state = Person.State.Ill
			Person.infected_people.remove(self)
			Person.ill_people.append(self)
			self.unquarantine()

	def cure(self):
		if self.state is Person.State.Ill:
			self.state = Person.State.Convalescent
			Person.ill_people.remove(self)
			Person.convalescent_people.append(self)
			self.unquarantine()

	def kill(self):
		if self.state is Person.State.Ill:
			self.state = Person.State.Dead
			Person.ill_people.remove(self)
			Person.dead_people.append(self)
			self.unquarantine()

	def get_expose_time(self):
		return self.expose_time

	def get_incubation_time(self) -> float:
		return self.incubation_time

	def get_recon_time(self) -> float:
		return self.reconvalescence_time

	def get_recovery_needed(self) -> float:
		return self.recovery_needed

	def get_distance_from(self, other: 'Person') -> float:
		return sqrt((self.x - other.x)**2 + (self.y - other.y)**2)

	def get_destination(self) -> [float, float]:
		return self.x, self.y
