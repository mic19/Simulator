import numpy as np
from person import Person
from view_strategy import *


if __name__ == "__main__":
	population = 100
	x_dim = 2
	y_dim = 1
	dx = 0.005
	MR = 0.1  # Ratio of mobile people
	DR = 0.03  # Death ration
	dt = 1
	sim_time = 100
	incubation_time = 120  # Incubation mean time
	recovery_time = 500
	infection_time = 3  # Time required for infection

	infection_distance = 0.05

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
	view_strategy = GraphStrategy(x_dim, y_dim)
	view_strategy.update(people)
	view_strategy.start()

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
			ratio = len(Person.mobile_people) / len(people)
			if ratio < MR and people[i].state is not Person.State.Ill:
				x = np.random.rand(1) * x_dim - x_dim / 2
				y = np.random.rand(1) * y_dim - y_dim / 2

				if people[i].movement_state is Person.MovementState.Idle:
					people[i].set_destination(x, y)

			if people[i].movement_state is Person.MovementState.GoingTo and people[i].state is not Person.State.Ill:
				people[i].move_to_destination(dx, dx)

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

		# Making view
		view_strategy.update(people)

	view_strategy.finish()
