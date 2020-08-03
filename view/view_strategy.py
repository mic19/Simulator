import matplotlib.pyplot as plt
from typing import List
from person import Person
from abc import ABC
from view.graph import Graph
from view.summary import SummaryFigure


# Strategy Design Patter
class ViewStrategy(ABC):
	def __init__(self, x_dim: float, y_dim: float):
		self.x_dim = x_dim
		self.y_dim = y_dim
		self.time = 0

		self.healthy_accumulation = []
		self.infected_accumulation = []
		self.ill_accumulation = []
		self.convalescent_accumulation = []
		self.dead_accumulation = []
		self.people = None

	def update(self, people: List[Person]):
		self.people = people
		self.healthy_accumulation.append(len(Person.healthy_people))
		self.infected_accumulation.append(len(Person.infected_people))
		self.ill_accumulation.append(len(Person.ill_people))
		self.convalescent_accumulation.append(len(Person.convalescent_people))
		self.dead_accumulation.append(len(Person.dead_people))

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
		self.graph.update_distribution()
		self.graph.update_share(
			self.healthy_accumulation,
			self.infected_accumulation,
			self.ill_accumulation,
			self.convalescent_accumulation,
			self.dead_accumulation
		)
		plt.show()


# Summary graph and generated gif at the end
class GifStrategy(NoViewStrategy):
	def __init__(self, x_dim: float, y_dim: float):
		super().__init__(x_dim, y_dim)

		self.gif_data = []
		self.counter = 0

	def update(self, people: List[Person]):
		super().update(people)

		self.graph.update_distribution()
		self.graph.update_share(
			self.healthy_accumulation,
			self.infected_accumulation,
			self.ill_accumulation,
			self.convalescent_accumulation,
			self.dead_accumulation
		)

		# TODO:
		name = 'output/test' + str(self.counter) + '.png'
		plt.savefig(name, dpi=80)
		self.counter += 1
		self.gif_data.append(name)

	def finish(self):
		super().finish()

		import imageio
		images = []
		for filename in self.gif_data:
			images.append(imageio.imread(filename))
		imageio.mimsave('output/a.gif', images)


# View updating during simulation
class GraphStrategy(ViewStrategy):
	def __init__(self, x_dim: float, y_dim: float):
		super().__init__(x_dim, y_dim)
		self.graph = Graph(x_dim, y_dim)

	def update(self, people: List[Person]):
		super().update(people)

		self.graph.update_distribution()
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
		summary = SummaryFigure(self.people)
		summary.show()

