import numpy as np
from view.view_strategy import *
import random
import math


def get_incubation_time(incubation_mean: float) -> float:
	return np.random.normal(incubation_mean, 30)


def get_recovery_time(recovery_mean: float) -> float:
	return np.random.normal(recovery_mean, 120)


def get_direction() -> [float, float]:
	angle = np.random.rand(1) * 2 * math.pi
	x = abs(math.sin(angle))
	y = abs(math.cos(angle))

	angle = angle/math.pi * 180
	if 90 <= angle < 180:
		y = -y
	elif 180 <= angle < 270:
		x, y = -x, -y
	elif 270 <= angle:
		x = -x

	return x, y


def main():
	population = 150
	x_dim = 2  # km
	y_dim = 2  # km
	dx = 0.005
	MR = 0.3  # Ratio of mobile people
	DR = 0.03  # Death ration
	dt = 1
	sim_time = 700
	incubation_time = 140  # Incubation mean time
	recovery_time = 400
	infection_time = 3  # Time required for infection
	hospital_capacity = population * 0.2
	infection_distance = 0.1
	wandering_distance = 0.5
	quarantine_ratio = 0.9
	quarantine_flag = False
	isolation_distance = 0.2

	Px = np.random.rand(population) * x_dim - x_dim / 2
	Py = np.random.rand(population) * y_dim - y_dim / 2
	Ps = np.zeros(population, dtype=int)
	Ps[0] = 1

	nt = 0

	people = [Person(Px[i], Py[i]) for i in range(population)]
	people[0].infect(get_incubation_time(incubation_time), get_recovery_time(recovery_time))
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
		ratio = len(Person.mobile_people) / len(people)
		if ratio < MR:
			num_to_select = MR * len(people) - len(Person.mobile_people)
			selected = random.choices(Person.idle_people, k=int(num_to_select))

			for person in selected:
				distance = np.random.rand(1) * wandering_distance
				direction = get_direction()
				vector = direction * distance
				destination = person.get_destination() + vector

				person.set_destination(destination[0], destination[1])

		for person in Person.mobile_people:
			person.move_to_destination(dx, dx)

		# Changing state
		for person in Person.healthy_people:
			if person.get_expose_time() >= infection_time:
				person.infect(get_incubation_time(incubation_time), get_recovery_time(recovery_time))

		for person in Person.infected_people:
			person.increase_incubation(dt)

		for person in Person.ill_people:
			if person.get_recon_time() >= person.get_recovery_needed():
				if np.random.random(1) > DR:
					person.cure()
				else:
					person.kill()
			person.reconvalesce(dt)

		# Making view
		view_strategy.update(people)

	view_strategy.finish()


if __name__ == "__main__":
	main()
