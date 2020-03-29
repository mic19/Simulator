import matplotlib.pyplot as plt
from typing import List
from person import Person
from abc import ABC
from graph import Graph


# Strategy Design Patter
class ViewStrategy(ABC):
	def __init__(self, x_dim: float, y_dim: float):
		self.x_dim = x_dim
		self.y_dim = y_dim
		self.time = 0

		self.healthy = []
		self.infected = []
		self.ill = []
		self.convalescent = []
		self.dead = []

		self.healthy_accumulation = []
		self.infected_accumulation = []
		self.ill_accumulation = []
		self.convalescent_accumulation = []
		self.dead_accumulation = []

	def update(self, people: List[Person]):
		# TODO
		self.healthy = []
		self.infected = []
		self.ill = []
		self.convalescent = []
		self.dead = []

		for person in people:
			if person.state is Person.State.Healthy:
				self.healthy.append(person)
			elif person.state is Person.State.Infected:
				self.infected.append(person)
			elif person.state is Person.State.Ill:
				self.ill.append(person)
			elif person.state is Person.State.Convalescent:
				self.convalescent.append(person)
			elif person.state is Person.State.Dead:
				self.dead.append(person)

		self.healthy_accumulation.append(len(self.healthy))
		self.infected_accumulation.append(len(self.infected))
		self.ill_accumulation.append(len(self.ill))
		self.convalescent_accumulation.append(len(self.convalescent))
		self.dead_accumulation.append(len(self.dead))

	def start(self):
		pass

	def show(self):
		pass

	def finish(self):
		pass


# No view during simulation, summary graph at the end
class NoViewStrategy(ViewStrategy):
	def __init__(self, x_dim: float, y_dim: float):
		super().__init__(x_dim, y_dim)
		self.graph = Graph(x_dim, y_dim)
		self.people = None

	def update(self, people: List[Person]):
		self.people = people
		super().update(people)

	def finish(self):
		self.graph.update_distribution(self.people)
		self.graph.update_share(
			self.healthy_accumulation,
			self.infected_accumulation,
			self.ill_accumulation,
			self.convalescent_accumulation,
			self.dead_accumulation
		)

		self.graph.show()


# View updating during simulation
class GraphStrategy(ViewStrategy):
	def __init__(self, x_dim: float, y_dim: float):
		super().__init__(x_dim, y_dim)
		self.graph = Graph(x_dim, y_dim)

	def update(self, people: List[Person]):
		super().update(people)

		self.graph.update_distribution(people)
		self.graph.update_share(
			self.healthy_accumulation,
			self.infected_accumulation,
			self.ill_accumulation,
			self.convalescent_accumulation,
			self.dead_accumulation
		)

		plt.pause(0.05)

	def finish(self):
		self.graph.show()

