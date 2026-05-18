from plotter_base_configuration import BasePlotterConfiguration
from plotter_estimator_method_configuration import EstimatorMethodViewerConfiguration
import numpy as np



class BasestEstimatorConfiguration(BasePlotterConfiguration):

	def __init__(self):
		super().__init__()
		self._method_name = None
		self._references = None
		self._value_by_true = None
		self._random_state_seed = None
		self._number_dimensions = None
		self._number_trial_runs = None
		self._number_points = None
		self._radius = None
		self._side_length = None

	@property
	def method_name(self):
		return self._method_name
	
	@property
	def references(self):
		return self._references

	@property
	def value_by_true(self):
		return self._value_by_true

	@property
	def random_state_seed(self):
		return self._random_state_seed
	
	@property
	def number_dimensions(self):
		return self._number_dimensions
	
	@property
	def number_trial_runs(self):
		return self._number_trial_runs
	
	@property
	def number_points(self):
		return self._number_points
	
	@property
	def radius(self):
		return self._radius
	
	@property
	def side_length(self):
		return self._side_length
	
	def initialize_method_name(self):
		method_name = "Approximation of Pi\nMonte Carlo Method"
		self._method_name = method_name

	def initialize_references(self):
		references = {
			"article 1" : "https://arxiv.org/ftp/arxiv/papers/1909/1909.13212.pdf",
			"article 2" : "https://en.wikipedia.org/wiki/Approximations_of_pi#/media/File:Pi_monte_carlo_en.gif",
			}
		self._references = references

	def initialize_value_by_true(self):
		value_by_true = np.pi
		self._value_by_true = value_by_true

	def update_random_state_seed(self, random_state_seed):
		np.random.seed(
			random_state_seed)
		self._random_state_seed = random_state_seed

	@staticmethod
	def get_default_number_dimensions():
		number_dimensions = 2
		return number_dimensions

	def initialize_number_dimensions(self, number_dimensions):
		if number_dimensions is None:
			number_dimensions = self.get_default_number_dimensions()
		else:
			if not isinstance(number_dimensions, (int, np.int64)):
				raise ValueError("invalid type(number_dimensions): {}".format(type(number_dimensions)))
			if number_dimensions < 2:
				raise ValueError("invalid number_dimensions: {}".format(number_dimensions))
		if number_dimensions != 2:
			raise ValueError("not yet implemented")
		self._number_dimensions = number_dimensions

	@staticmethod
	def get_default_number_trial_runs():
		number_trial_runs = 100
		return number_trial_runs

	def initialize_number_trial_runs(self, number_trial_runs):
		if number_trial_runs is None:
			number_trial_runs = self.get_default_number_trial_runs()
		else:
			if not isinstance(number_trial_runs, (int, np.int64)):
				raise ValueError("invalid type(number_trial_runs): {}".format(type(number_trial_runs)))
			if number_trial_runs < 1:
				raise ValueError("invalid number_trial_runs: {}".format(number_trial_runs))
		self._number_trial_runs = number_trial_runs

	@staticmethod
	def get_default_number_points():
		number_points = 10_000
		return number_points

	def initialize_number_points(self, number_points):
		if number_points is None:
			number_points = self.get_default_number_points()
		else:
			if not isinstance(number_points, (int, np.int64)):
				raise ValueError("invalid type(number_points): {}".format(type(number_points)))
			if number_points < 5:
				raise ValueError("invalid number_points: {}".format(number_points))
		self._number_points = number_points

	def initialize_radius(self, radius):
		if radius is None:
			radius = 1
		else:
			if not isinstance(radius, (int, np.int64, float)):
				raise ValueError("invalid type(radius): {}".format(type(radius)))
			if radius <= 0:
				raise ValueError("invalid radius: {}".format(radius))
		self._radius = radius

	def initialize_side_length(self):
		side_length = 2 * self.radius
		self._side_length = side_length

class BaseEstimatorConfiguration(BasestEstimatorConfiguration):

	def __init__(self):
		super().__init__()
		self._trial_data = None
		self._statistics = None
		self._value_by_approximation = None

	@property
	def trial_data(self):
		return self._trial_data

	@property
	def statistics(self):
		return self._statistics
	
	@property
	def value_by_approximation(self):
		return self._value_by_approximation


	def initialize_trial_data(self):
		container_coordinates = list()
		container_distances = list()
		container_is_inside_circle = list()
		container_is_outside_circle = list()
		container_is_on_circle = list()
		container_number_points_inside_circle = list()
		container_number_points_outside_circle = list()
		container_number_points_on_circle = list()
		container_number_points_total = list()
		container_approximation_values = list()
		for it in range(self.number_trial_runs):
			coordinates = np.random.uniform(
				-1 * self.radius,
				self.radius,
				size=(
					self.number_points,
					self.number_dimensions,
					),
				)
			distances_from_origin = np.sqrt(
				np.sum(
					np.square(
						coordinates),
					axis=1))
			is_points_inside_circle = (distances_from_origin < self.radius)
			is_points_outside_circle = (distances_from_origin > self.radius)
			is_points_on_circle = (distances_from_origin == self.radius)
			number_points_inside_circle = int(
				np.sum(
					is_points_inside_circle))
			number_points_outside_circle = int(
				np.sum(
					is_points_outside_circle))
			number_points_on_circle = int(
				np.sum(
					is_points_on_circle))
			number_points_total = number_points_inside_circle + number_points_outside_circle + number_points_on_circle
			value_by_approximation = 4 * number_points_inside_circle / self.number_points
			container_coordinates.append(
				coordinates)
			container_distances.append(
				distances_from_origin)
			container_is_inside_circle.append(
				is_points_inside_circle)
			container_is_outside_circle.append(
				is_points_outside_circle)
			container_is_on_circle.append(
				is_points_on_circle)
			container_number_points_inside_circle.append(
				number_points_inside_circle)
			container_number_points_outside_circle.append(
				number_points_outside_circle)
			container_number_points_on_circle.append(
				number_points_on_circle)
			container_number_points_total.append(
				number_points_total)
			container_approximation_values.append(
				value_by_approximation)
		trial_data = {
			"coordinates" : np.array(
				container_coordinates),
			"distances from origin" : np.array(
				container_distances),
			"is inside circle" : np.array(
				container_is_inside_circle),
			"is outside circle" : np.array(
				container_is_outside_circle),
			"is on circle" : np.array(
				container_is_on_circle),
			"number points inside circle" : np.array(
				container_number_points_inside_circle),
			"number points outside circle" : np.array(
				container_number_points_outside_circle),
			"number points on circle" : np.array(
				container_number_points_on_circle),
			"number points total" : np.array(
				container_number_points_total),
			"approximation values" : np.array(
				container_approximation_values),
			}
		self._trial_data = trial_data

	def initialize_statistics(self):
		approximation_values = self.trial_data["approximation values"]
		mean_value = np.mean(
			approximation_values)
		median_value = np.median(
			approximation_values)
		st_dev_value = np.std(
			approximation_values)
		minimum_value = np.min(
			approximation_values)
		maximum_value = np.max(
			approximation_values)
		statistics = {
			"mean" : mean_value,
			"median" : median_value,
			"standard deviation" : st_dev_value,
			"minimum" : minimum_value,
			"maximum" : maximum_value,
			}
		self._statistics = statistics

	def initialize_value_by_approximation(self):
		# approximation_values = self.trial_data["approximation values"]
		# value_by_approximation = np.mean(
		# 	approximation_values)
		value_by_approximation = float(
			self.statistics["mean"])
		self._value_by_approximation = value_by_approximation

class EstimatorErrorConfiguration(BaseEstimatorConfiguration):

	def __init__(self):
		super().__init__()
		self._absolute_errors = None ## using approximation value per trial
		self._relative_errors = None ## using approximation value per trial
		self._absolute_error = None ## using mean approximation value
		self._relative_error = None ## using mean approximation value

	@property
	def absolute_errors(self):
		return self._absolute_errors
	
	@property
	def relative_errors(self):
		return self._relative_errors

	@property
	def absolute_error(self):
		return self._absolute_error
	
	@property
	def relative_error(self):
		return self._relative_error
	
	def get_absolute_error(self, value_by_approximation):
		absolute_error = np.abs(
			self.value_by_true - value_by_approximation)
		return absolute_error

	def get_relative_error(self, absolute_error):
		relative_error_as_decimal = absolute_error / self.value_by_true
		relative_error_as_percent = relative_error_as_decimal * 100
		return relative_error_as_decimal, relative_error_as_percent

	def initialize_errors(self):
		approximation_values = self.trial_data["approximation values"]
		absolute_errors = self.get_absolute_error(
			value_by_approximation=approximation_values)
		_, relative_errors = self.get_relative_error(
			absolute_error=absolute_errors)
		absolute_error = self.get_absolute_error(
			value_by_approximation=self.value_by_approximation)
		_, relative_error = self.get_relative_error(
			absolute_error=absolute_error)
		self._absolute_errors = absolute_errors
		self._relative_errors = relative_errors
		self._absolute_error = absolute_error
		self._relative_error = relative_error

class EstimatorConfiguration(EstimatorErrorConfiguration):

	def __init__(self):
		super().__init__()

	def __repr__(self):
		s = "EstimatorConfiguration()"
		return s

	def __str__(self):
		method_name = "\n .. method name:\n{}\n".format(
			self.method_name)
		number_dimensions = "number dimensions:\n{:,}\n".format(
			self.number_dimensions)
		number_trial_runs = "number trial runs:\n{:,}\n".format(
			self.number_trial_runs)
		number_points = "number points:\n{:,}\n".format(
			self.number_points)
		radius = "\n .. radius:\n{}\n".format(
			self.radius)
		side_length = "side length:\n{}\n".format(
			self.side_length)
		value_by_true = "\n .. true value:\n{:.10f}\n".format(
			self.value_by_true)
		value_by_approximation = "\n .. approximation value:\n{:.10f}\n".format(
			self.value_by_approximation)
		mean_relative_error = "\n .. mean relative error of approximation:\n{}\n".format(
			np.mean(
				self.relative_error),
			)
		s = "\n".join([
			method_name,
			number_dimensions,
			number_trial_runs,
			number_points,
			radius,
			side_length,
			value_by_true,
			value_by_approximation,
			mean_relative_error,
			])
		return s

	def initialize(self, number_dimensions=None, number_trial_runs=None, number_points=None, radius=None, random_state_seed=None):
		self.initialize_method_name()
		self.initialize_references()
		self.initialize_value_by_true()
		self.initialize_number_dimensions(
			number_dimensions=number_dimensions)
		self.initialize_number_trial_runs(
			number_trial_runs=number_trial_runs)
		self.initialize_number_points(
			number_points=number_points)
		self.initialize_radius(
			radius=radius)
		self.initialize_side_length()
		if random_state_seed is not None:
			self.update_random_state_seed(
				random_state_seed=random_state_seed)
		self.initialize_trial_data()
		self.initialize_statistics()
		self.initialize_value_by_approximation()
		self.initialize_errors()

	def view_approximation_method(self, *args, **kwargs):
		viewer = EstimatorMethodViewerConfiguration()
		viewer.initialize_visual_settings(
			tick_size=self.visual_settings.tick_size,
			label_size=self.visual_settings.label_size,
			text_size=self.visual_settings.text_size,
			cell_size=self.visual_settings.cell_size,
			title_size=self.visual_settings.title_size)
		viewer.update_save_directory(
			path_to_save_directory=self.visual_settings.path_to_save_directory)
		viewer.view_approximation_method(
			self, ## estimator,
			*args,
			**kwargs)

##