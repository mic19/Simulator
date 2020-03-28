import numpy as np
import matplotlib.pyplot as plt
from enum import Enum
from typing import List
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


class Graph:
	def __init__(self, x_dim: float, y_dim: float):
		self.x_dim = x_dim
		self.y_dim = y_dim

		self.healthy = []
		self.infected = []
		self.ill = []
		self.convalescent = []
		self.dead = []

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

		# Pie
		plt.subplot(1, 2, 2)
		plt.cla()
		plt.pie((len(self.healthy), len(self.infected), len(self.ill),
					len(self.convalescent), len(self.dead)),
					# TODO: czy dokumentacja gwarantuje kolejnosc wartosci?
					colors=self.color_dict.values(),
					labels=self.color_dict.keys(),
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


if __name__ == "__main__":
	population = 100
	x_dim = 2
	y_dim = 1
	dx = 0.05
	MR = 0.2  # Ratio of mobile people
	DR = 0.03  # Death ration
	dt = 1
	sim_time = 1000
	incubation_time = 120  # Incubation mean time
	recovery_time = 500
	infection_time = 3  # Time required for infection

	infection_distance = 0.1

	Px = np.random.rand(population) * x_dim - x_dim / 2
	Py = np.random.rand(population) * y_dim - y_dim / 2
	Ps = np.zeros(population, dtype=int)
	Pss = np.zeros(population, dtype=int)
	Pa = np.zeros(population, dtype=int)
	Ps[0] = 1
	stat = []

	nt = 0

	people = [Person(Px[i], Py[i]) for i in range(population)]
	people[0].state = Person.State.Infected
	graph = Graph(x_dim, y_dim)
	graph.update(people)

	# Simulation
	for t in range(0, sim_time, dt):
		nt += 1

		# Exposition to infection
		for i in range(population - 1):
			for j in range(i + 1, population):
				distance = people[i].get_distance_from(people[j])
				if distance < infection_distance:
					if people[i].state is Person.State.Infected or people[i].state is Person.State.Ill:
						people[j].expose(dt)
					if people[j].state is Person.State.Infected or people[j].state is Person.State.Ill:
						people[i].expose(dt)

		# Moving
		for i in range(population):
			if np.random.random() < MR and people[i].state is not Person.State.Ill:
				x = np.random.random() * dx - dx / 2
				y = np.random.random() * dx - dx / 2

				people[i].move(x, y)

		# Changing state
		for i in range(population):
			if people[i].get_expose_time() >= infection_time:
				people[i].infect()

			if people[i].get_incubation_time() >= incubation_time:
				people[i].ill()

			if people[i].state is Person.State.Ill:
				if people[i].get_recon_time() >= recovery_time:
					if np.random.random(1) > DR:
						people[i].cure()
					else:
						people[i].kill()

			if people[i].state is Person.State.Infected:
				people[i].increase_incubation(dt)

			if people[i].state is Person.State.Ill:
				people[i].reconvalesce(dt)


		# Making graph
		graph.update(people)

	graph.show()
