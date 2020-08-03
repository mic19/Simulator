import matplotlib.pyplot as plt
from person import Person


class SummaryFigure:
	def __init__(self, people: [Person]):
		self.figure = plt.figure()

		self.gridspec = self.figure.add_gridspec(nrows=1, ncols=1)
		self.incub_axes = self.figure.add_subplot(self.gridspec[0, 0])
		self.incub_axes.set_title('Incubation time')
		self.incub_axes.set_xlabel('t [day]')
		self.incub_axes.set_ylabel('n')
		self.incub_axes.set_xlim(0, 200)
		self.hist_data = []

		for person in people:
			if person.state in (Person.State.Ill, Person.State.Convalescent, Person.State.Dead):
				self.hist_data.append(person.get_incubation_time())

		num_bins = 20
		n, bins, patches = self.incub_axes.hist(self.hist_data, num_bins, density=1)

	def show(self):
		plt.show()