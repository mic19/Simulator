import matplotlib.pyplot as plt
from person import Person
from typing import List


class Graph:
	def __init__(self, x_dim: float, y_dim: float):
		self.color_dict = {
			"healthy": [0.2, 0.9, 0.4],
			"infected": [0.9, 0.9, 0],
			"ill": [0.9, 0, 0],
			"convalescent": [0.1, 0.1, 0.9],
			"dead": [0, 0, 0]
		}
		self.data = []

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

	def update_distribution(self, people: List[Person]):
		# Population distribution graph
		plt.subplot(1, 2, 1)
		self.clear()

		for person in people:
			temp = None
			if person.state == Person.State.Healthy:
				color = self.color_dict["healthy"]
				temp = plt.scatter(person.x, person.y, c=[color], s=7)
			elif person.state == Person.State.Infected:
				color = self.color_dict["infected"]
				temp = plt.scatter(person.x, person.y, c=[color], s=7)
			elif person.state == Person.State.Ill:
				color = self.color_dict["ill"]
				temp = plt.scatter(person.x, person.y, c=[color], s=7)
			elif person.state == Person.State.Convalescent:
				color = self.color_dict["convalescent"]
				temp = plt.scatter(person.x, person.y, c=[color], s=7)
			elif person.state == Person.State.Dead:
				color = self.color_dict["dead"]
				temp = plt.scatter(person.x, person.y, c=[color], s=7)

			self.data.append(temp)

	def update_share(self, healthy_acc, infected_acc, ill_acc, convalescent_acc, dead_acc):
		# Chart
		plt.subplot(1, 2, 2)
		plt.cla()
		plt.title("Udział poszczególnych grup w populacji")
		plt.xlabel("t")
		plt.ylabel("n")
		plt.grid(True, color=[0.9, 0.9, 0.9], linewidth=1)

		plt.rc('lines', linewidth=1)
		time = [i for i in range(len(healthy_acc))]
		plots = [healthy_acc, infected_acc, ill_acc, convalescent_acc, dead_acc]
		colors = ['green', 'yellow', 'red', 'blue', 'black']

		for i in range(len(plots)):
			plt.plot(
				time,
				plots[i],
				color=colors[i]
			)

	def clear(self):
		# TODO
		for item in self.data:
			item.remove()
		self.data = []

	def show(self):
		plt.show()

