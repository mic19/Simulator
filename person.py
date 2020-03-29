from enum import Enum
from math import sqrt


class Person:
	class State(Enum):
		Healthy = 0
		Infected = 1
		Ill = 2
		Convalescent = 3
		Dead = 4

	def __init__(self, x_pos: float, y_pos: float, state=State.Healthy):
		self.x = x_pos
		self.y = y_pos
		self.state = state
		self.expose_time = 0
		self.incubation_time = 0
		self.reconvalescence_time = 0

	def move(self, dx: float, dy: float):
		self.x += dx
		self.y += dy

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