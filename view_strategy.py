import matplotlib.pyplot as plt
from typing import List
from person import Person
from abc import ABC


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
		pass

	def show(self):
		pass

	def finish(self):
		pass


class NoViewStrategy(ViewStrategy):
	def __init__(self, x_dim: float, y_dim: float):
		super().__init__(x_dim, y_dim)


class GraphStrategy(ViewStrategy):
	def __init__(self, x_dim: float, y_dim: float):
		super().__init__(x_dim, y_dim)

		self.color_dict = {
			"healthy": [0.2, 0.9, 0.4],
			"infected": [0.9, 0.9, 0],
			"ill": [0.9, 0, 0],
			"convalescent": [0.1, 0.1, 0.9],
			"dead": [0, 0, 0]
		}

		plt.subplot(1, 2, 1)
		plt.gcf().set_size_inches(12, 5)
		plt.title('Rozkład populacji')
		plt.xlim(-x_dim * 0.6, x_dim * 0.6)
		plt.ylim(-y_dim * 0.6, y_dim * 0.6)
		plt.xlabel('x')
		plt.ylabel('y')
		plt.grid(True, color=[0.9, 0.9, 0.9], linewidth=1)

		plt.subplot(1, 2, 2)
		plt.title('Populacja')

	def update(self, people: List[Person]):
		# Population graph
		plt.subplot(1, 2, 1)
		self.clear()

		for person in people:
			temp = None
			if person.state == Person.State.Healthy:
				color = self.color_dict["healthy"]
				temp = plt.scatter(person.x, person.y, c=[color], s=7)
				self.healthy.append(temp)
			elif person.state == Person.State.Infected:
				color = self.color_dict["infected"]
				temp = plt.scatter(person.x, person.y, c=[color], s=7)
				self.infected.append(temp)
			elif person.state == Person.State.Ill:
				color = self.color_dict["ill"]
				temp = plt.scatter(person.x, person.y, c=[color], s=7)
				self.ill.append(temp)
			elif person.state == Person.State.Convalescent:
				color = self.color_dict["convalescent"]
				temp = plt.scatter(person.x, person.y, c=[color], s=7)
				self.convalescent.append(temp)
			elif person.state == Person.State.Dead:
				color = self.color_dict["dead"]
				temp = plt.scatter(person.x, person.y, c=[color], s=7)
				self.dead.append(temp)

		# Chart
		self.time += 1
		self.healthy_accumulation.append(len(self.healthy))
		self.infected_accumulation.append(len(self.infected))
		self.ill_accumulation.append(len(self.ill))
		self.convalescent_accumulation.append(len(self.convalescent))
		self.dead_accumulation.append(len(self.dead))

		plt.subplot(1, 2, 2)
		plt.cla()
		plt.title("Udział poszczególnych grup w populacji")
		plt.xlabel("t")
		plt.ylabel("n")
		plt.grid(True, color=[0.9, 0.9, 0.9], linewidth=1)

		from matplotlib import cycler
		cycle = cycler(color=['green', 'yellow', 'red', 'blue', 'black'])

		plt.rc('lines', linewidth=1)
		plt.rc('axes', prop_cycle=cycle)

		plt.plot(
			[i for i in range(self.time)],
			self.healthy_accumulation,
			[i for i in range(self.time)],
			self.infected_accumulation,
			[i for i in range(self.time)],
			self.ill_accumulation,
			[i for i in range(self.time)],
			self.convalescent_accumulation,
			[i for i in range(self.time)],
			self.dead_accumulation,
		)

		plt.pause(0.05)

	def clear(self):
		# TODO
		for item in self.healthy:
			item.remove()
		for item in self.infected:
			item.remove()
		for item in self.ill:
			item.remove()
		for item in self.convalescent:
			item.remove()
		for item in self.dead:
			item.remove()

		self.healthy = []
		self.infected = []
		self.ill = []
		self.convalescent = []
		self.dead = []

	def show(self):
		plt.show()