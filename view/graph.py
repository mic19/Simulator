import matplotlib.pyplot as plt
from person import Person


class Graph:
	def __init__(self, x_dim: float, y_dim: float):
		self.color_dict = {
			"healthy": [0.2, 0.9, 0.4],
			"infected": [0.9, 0.9, 0],
			"ill": [0.9, 0, 0.1],
			"convalescent": [0.1, 0.1, 0.9],
			"dead": [0, 0, 0]
		}
		self.data = []
		self.counter = 0
		self.plots = []
		self.incub_data = []
		self.figure = plt.figure()
		self.gridspec = self.figure.add_gridspec(nrows=2, ncols=2, wspace=0.2, hspace=0.4)
		self.figure.set_size_inches(14, 7)

		self.dist_axes = self.figure.add_subplot(self.gridspec[:, 0])
		self.dist_axes.set_title('Distribution of population')
		self.dist_axes.set_xlim(-x_dim * 0.6, x_dim * 0.6)
		self.dist_axes.set_ylim(-y_dim * 0.6, y_dim * 0.6)
		self.dist_axes.set_xlabel('x [km]')
		self.dist_axes.set_ylabel('y [km]')
		self.dist_axes.grid(color=[0.9, 0.9, 0.9], linewidth=1)

		self.share_axes = self.figure.add_subplot(self.gridspec[:, 1])
		self.share_axes.set_title('Share of individual groups in population')
		self.share_axes.set_xlabel('t [h]')
		self.share_axes.set_ylabel('n')
		self.share_axes.grid(color=[0.9, 0.9, 0.9], linewidth=1)

		from matplotlib import patches
		self.colors = ['green', 'yellow', 'red', 'blue', 'black']
		self.states = ['healthy', 'infected', 'ill', 'convalescent', 'dead']
		patch_list = []

		for i in range(len(self.colors)):
			patch = patches.Patch(color=self.colors[i], label=self.states[i])
			patch_list.append(patch)

		self.share_axes.legend(handles=patch_list, loc='upper left')

		# self.incub_axes = self.figure.add_subplot(self.gridspec[1, 1])
		# self.incub_axes.set_title('Incubation time')
		# self.incub_axes.set_xlabel('t [day]')
		# self.incub_axes.set_ylabel('n')
		# self.incub_axes.set_xlim(0, 200)

	def update_distribution(self):
		# Population distribution graph
		self.clear_distribution()
		self.counter += 1

		for person in Person.healthy_people:
			color = self.color_dict["healthy"]
			temp = self.dist_axes.scatter(person.x, person.y, c=[color], s=7)
			self.data.append(temp)

		for person in Person.infected_people:
			color = self.color_dict["infected"]
			temp = self.dist_axes.scatter(person.x, person.y, c=[color], s=7)
			self.data.append(temp)

		for person in Person.ill_people:
			color = self.color_dict["ill"]
			temp = self.dist_axes.scatter(person.x, person.y, c=[color], s=7)
			self.data.append(temp)

		for person in Person.convalescent_people:
			color = self.color_dict["convalescent"]
			temp = self.dist_axes.scatter(person.x, person.y, c=[color], s=7)
			self.data.append(temp)

		for person in Person.dead_people:
			color = self.color_dict["dead"]
			temp = self.dist_axes.scatter(person.x, person.y, c=[color], s=7)
			self.data.append(temp)

	def update_share(self, healthy_acc, infected_acc, ill_acc, convalescent_acc, dead_acc):
		# Chart
		self.clear_share()

		time = [i for i in range(len(healthy_acc))]
		plots_data = [healthy_acc, infected_acc, ill_acc, convalescent_acc, dead_acc]

		for i in range(len(plots_data)):
			p = self.share_axes.plot(
				time,
				plots_data[i],
				color=self.colors[i]
			)
			self.plots.append(p)

	def clear_distribution(self):
		# TODO
		for item in self.data:
			item.remove()
		self.data = []

	def clear_share(self):
		for item in self.plots:
			item.remove
		self.plots = []

	def show(self):
		plt.show()

	def imshow(self):
		return plt.imshow()

