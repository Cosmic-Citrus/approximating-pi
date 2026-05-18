from plotter_base_configuration import BasePlotterConfiguration
from plotter_kinematics_configuration import EstimatorKinematicsViewerConfiguration
from plotter_phase_space_configuration import EstimatorPhaseSpaceViewerConfiguration
import numpy as np


class BasestEstimatorConfiguration(BasePlotterConfiguration):

	def __init__(self):
		super().__init__()
		self._method_name = None
		self._references = None
		self._value_by_true = None

	@property
	def method_name(self):
		return self._method_name
	
	@property
	def references(self):
		return self._references

	@property
	def value_by_true(self):
		return self._value_by_true

	def initialize_method_name(self):
		method_name = r"$1-D$ Elastic Collisions"
		self._method_name = method_name

	def initialize_references(self):
		references = {
			"video 1" : "https://www.youtube.com/watch?v=HEfHFsfGXjs",
			"article 1" : "https://arxiv.org/pdf/1901.06260.pdf",
			"article 2" : "https://www.3blue1brown.com/lessons/clacks-solution",
			}
		self._references = references

	def initialize_value_by_true(self):
		value_by_true = np.pi
		self._value_by_true = value_by_true

class BaseEstimatorConfiguration(BasestEstimatorConfiguration):

	def __init__(self):
		super().__init__()
		self._simulation_parameters = None
		self._simulation_results = None
		self._value_by_approximation = None

	@property
	def simulation_parameters(self):
		return self._simulation_parameters
	
	@property
	def simulation_results(self):
		return self._simulation_results

	@property
	def value_by_approximation(self):
		return self._value_by_approximation
	
	@staticmethod
	def get_momentum(m, v):
		p = m * v
		return p

	@staticmethod
	def get_energy(m, v):
		u = m * v * v / 2
		return u

	def initialize_simulation_parameters(self, mass_ratio_power):
		if mass_ratio_power is None:
			mass_ratio_power = 2
		else:
			if not isinstance(mass_ratio_power, (int, float)):
				raise ValueError("invalid type(mass_ratio_power): {}".format(type(mass_ratio_power)))
			if mass_ratio_power <= 0:
				raise ValueError("invalid mass_ratio_power: {}".format(mass_ratio_power))
		m1 = 1
		m2 = 100 ** (mass_ratio_power - 1)
		v1 = 0
		v2 = -1
		p1 = self.get_momentum(
			m=m1,
			v=v1)
		p2 = self.get_momentum(
			m=m2,
			v=v2)
		u1 = self.get_energy(
			m=m1,
			v=v1)
		u2 = self.get_energy(
			m=m2,
			v=v2)
		simulation_parameters = {
			"mass ratio power" : mass_ratio_power,
			"m1" : m1,
			"m2" : m2,
			"v1" : v1,
			"v2" : v2,
			"p1" : p1,
			"p2" : p2,
			"u1" : u1,
			"u2" : u2,
			}
		self._simulation_parameters = simulation_parameters

	def initialize_simulation_results(self):
		m1 = float(
			self.simulation_parameters["m1"])
		v1 = float(
			self.simulation_parameters["v1"])
		p1 = float(
			self.simulation_parameters["p1"])
		u1 = float(
			self.simulation_parameters["u1"])
		m2 = float(
			self.simulation_parameters["m2"])
		v2 = float(
			self.simulation_parameters["v2"])
		p2 = float(
			self.simulation_parameters["p2"])
		u2 = float(
			self.simulation_parameters["u2"])
		container_v1 = [
			v1,
			]
		container_v2 = [
			v2,
			]
		collision_mapping = {
			"m1-wall" : 1,
			None : 0,
			"m1-m2" : -1,
			}
		container_collision_status = [
			# int(
			# 	collision_mapping[None]),
			None,
			]
		container_number_collisions_per_loop = [
			0,
			]
		number_collisions = 0
		number_iterations = 0
		while True:
			is_not_colliding = ((v1 < v2) and (v2 > 0))
			if is_not_colliding:
				break
			else:
				p1 = m1 * v1
				p2 = m2 * v2
				m_total = m1 + m2
				p_total = p1 + p2
				dv = v2 - v1
				v1 = (p_total + m2 * dv) / m_total
				v2 = (p_total + m1 * (-1 * dv)) / m_total
				collision_status = [
					"m1-m2",
					]
				number_partial_collisions = 1
				container_v1.append(
					v1)
				container_v2.append(
					v2)
				if v1 < 0:
					v1 *= -1 ## bounce off wall
					collision_status.append(
						"m1-wall")
					container_v1.append(
						v1)
					container_v2.append(
						v2)
				number_partial_collisions = len(
					collision_status)
				container_collision_status.extend(
					collision_status)
				container_number_collisions_per_loop.append(
					number_partial_collisions)
				number_collisions += number_partial_collisions
				number_iterations += 1

		container_v1 = np.array(
			container_v1)
		container_v2 = np.array(
			container_v2)
		container_p1 = self.get_momentum(
			m=m1,
			v=container_v1)
		container_p2 = self.get_momentum(
			m=m1,
			v=container_v1)
		container_u1 = self.get_energy(
			m=m1,
			v=container_v1)
		container_u2 = self.get_energy(
			m=m2,
			v=container_v2)
		container_collision_status = np.array(
			container_collision_status)
		container_is_wall_collision = (container_collision_status == collision_mapping["m1-wall"])
		container_is_mass_collision = (container_collision_status == collision_mapping["m1-m2"])
		container_number_collisions_per_loop = np.array(
			container_number_collisions_per_loop)
		simulation_results = {
			"v1" : container_v1, 
			"p1" : container_p1,
			"u1" : container_u1,
			"v2" : container_v2,
			"p2" : container_p2,
			"u2" : container_u2,
			"is m1-wall collision" : container_is_wall_collision,
			"i1 m1-m2 collision" : container_is_mass_collision,
			"collision status" : container_collision_status,
			"number collisions per loop" : container_number_collisions_per_loop,
			"number collisions" : number_collisions,
			"number iterations" : number_iterations,
			"collision mapping" : collision_mapping,
			}
		self._simulation_results = simulation_results

	def initialize_value_by_approximation(self):
		number_collisions = self.simulation_results["number collisions"]
		mass_ratio_power = self.simulation_parameters["mass ratio power"]
		value_by_approximation = number_collisions / (10 ** (mass_ratio_power - 1))
		self._value_by_approximation = value_by_approximation

class EstimatorConfiguration(BaseEstimatorConfiguration):

	def __init__(self):
		super().__init__()

	def __repr__(self):
		s = "EstimatorConfiguration()"
		return s

	def __str__(self):
		method_name = "\n .. method name:\n{}\n".format(
			self.method_name)
		value_by_true = "\n .. true value:\n{:.10f}\n".format(
			self.value_by_true)
		value_by_approximation = "\n .. approximate value:\n{:.10f}\n".format(
			self.value_by_approximation)
		number_collisions = "\n .. number collisions:\n{}\n".format(
			self.simulation_results["number collisions"])
		number_iterations = "\n .. number iterations:\n{}\n".format(
			self.simulation_results["number iterations"])
		s = "\n".join([
			method_name,
			value_by_true,
			value_by_approximation,
			number_collisions,
			number_iterations,
			])
		return s

	def initialize(self, mass_ratio_power=None):
		self.initialize_method_name()
		self.initialize_references()
		self.initialize_value_by_true()
		self.initialize_simulation_parameters(
			mass_ratio_power=mass_ratio_power)
		self.initialize_simulation_results()
		self.initialize_value_by_approximation()

	def view_velocities_against_time(self, *args, **kwargs):
		viewer = EstimatorKinematicsViewerConfiguration()
		viewer.initialize_visual_settings(
			tick_size=self.visual_settings.tick_size,
			label_size=self.visual_settings.label_size,
			text_size=self.visual_settings.text_size,
			cell_size=self.visual_settings.cell_size,
			title_size=self.visual_settings.title_size)
		viewer.update_save_directory(
			path_to_save_directory=self.visual_settings.path_to_save_directory)
		viewer.view_velocities_against_time(
			self, ## estimator,
			*args,
			**kwargs)

	def view_phase_space(self, *args, **kwargs):
		viewer = EstimatorPhaseSpaceViewerConfiguration()
		viewer.initialize_visual_settings(
			tick_size=self.visual_settings.tick_size,
			label_size=self.visual_settings.label_size,
			text_size=self.visual_settings.text_size,
			cell_size=self.visual_settings.cell_size,
			title_size=self.visual_settings.title_size)
		viewer.update_save_directory(
			path_to_save_directory=self.visual_settings.path_to_save_directory)
		viewer.view_phase_space(
			self, ## estimator,
			*args,
			**kwargs)

##