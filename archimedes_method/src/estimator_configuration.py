from plotter_base_configuration import BasePlotterConfiguration
from plotter_estimator_method_configuration import EstimatorMethodViewerConfiguration
from plotter_estimator_accuracy_configuration import EstimatorAccuracyViewerConfiguration
import numpy as np


class BasestEstimatorConfiguration(BasePlotterConfiguration):

	def __init__(self):
		super().__init__()
		self._method_name = None
		self._references = None
		self._value_by_true = None
		self._radius = None
		self._number_initial_sides = None
		self._number_side_doublings = None

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
	def radius(self):
		return self._radius

	@property
	def number_initial_sides(self):
		return self._number_initial_sides
	
	@property
	def number_side_doublings(self):
		return self._number_side_doublings

	def initialize_method_name(self):
		method_name = "Approximation of Pi\nArchimedes Method"
		self._method_name = method_name

	def initialize_references(self):
		references = {
			"article 1" : "https://mathscholar.org/2019/02/simple-proofs-archimedes-calculation-of-pi/",
			"article 2" : "https://www.craig-wood.com/nick/articles/pi-archimedes/",
			"article 3" : "https://github.com/umcconnell/archimedes-pi",
			}
		self._references = references

	def initialize_value_by_true(self):
		value_by_true = np.pi
		self._value_by_true = value_by_true

	def initialize_radius(self, radius):
		if radius is None:
			radius = 1
		else:
			if not isinstance(radius, (int, float)):
				raise ValueError("invalid type(radius): {}".format(type(radius)))
			if radius <= 0:
				raise ValueError("invalid radius: {}".format(radius))
		self._radius = radius

	def initialize_number_initial_sides(self):
		number_initial_sides = 6 ## hexagon
		self._number_initial_sides = number_initial_sides

	def initialize_number_side_doublings(self, number_side_doublings):
		if number_side_doublings is None:
			number_side_doublings = 5
		else:
			if not isinstance(number_side_doublings, int):
				raise ValueError("invalid type(number_side_doublings): {}".format(type(number_side_doublings)))
			if number_side_doublings <= 0:
				raise ValueError("invalid number_side_doublings: {}".format(number_side_doublings))
		self._number_side_doublings = number_side_doublings

class BaseEstimatorConfiguration(BasestEstimatorConfiguration):

	def __init__(self):
		super().__init__()
		self._number_final_sides = None ## at last iteration
		self._numbers_sides = None ## at each iteration of side-doubling
		self._iterations = None
		self._lower_bounds_by_perimeter_approximation = None ## at each iteration of side-doubling
		self._upper_bounds_by_perimeter_approximation = None ## at each iteration of side-doubling
		self._lower_bounds_by_area_approximation = None ## at each iteration of side-doubling
		self._upper_bounds_by_area_approximation = None ## at each iteration of side-doubling
		self._values_by_perimeter_approximation = None ## at each iteration of side-doubling
		self._value_by_perimeter_approximation = None ## at last iteration
		self._values_by_area_approximation = None ## at each iteration of side-doubling
		self._value_by_area_approximation = None ## at last iteration

	@property
	def number_final_sides(self):
		return self._number_final_sides

	@property
	def numbers_sides(self):
		return self._numbers_sides
	
	@property
	def iterations(self):
		return self._iterations
	
	@property
	def lower_bounds_by_perimeter_approximation(self):
		return self._lower_bounds_by_perimeter_approximation
	
	@property
	def upper_bounds_by_perimeter_approximation(self):
		return self._upper_bounds_by_perimeter_approximation

	@property
	def lower_bounds_by_area_approximation(self):
		return self._lower_bounds_by_area_approximation
	
	@property
	def upper_bounds_by_area_approximation(self):
		return self._upper_bounds_by_area_approximation

	@property
	def values_by_perimeter_approximation(self):
		return self._values_by_perimeter_approximation

	@property
	def value_by_perimeter_approximation(self):
		return self._value_by_perimeter_approximation

	@property
	def values_by_area_approximation(self):
		return self._values_by_area_approximation

	@property
	def value_by_area_approximation(self):
		return self._value_by_area_approximation

	def update_side_doublings(self):
		## equilateral triangle ==> radius == length of side
		inscribed_side_length_at_it = float(
			self.radius)
		## 6 --> 12 --> 24 ... 6 * (2)^n
		number_sides_at_it = int(
			self.number_initial_sides)
		numbers_sides = list()
		## approximation bounds across all side-doublings
		lower_bounds_by_perimeter_approximation = list()
		upper_bounds_by_perimeter_approximation = list()
		lower_bounds_by_area_approximation = list()
		upper_bounds_by_area_approximation = list()
		values_by_perimeter_approximation = list()
		values_by_area_approximation = list()
		## iterate
		for it in range(self.number_side_doublings):
			## get approximation by midpoint of inner/outer perimeter and area
			inner_polygon_parameters_at_it = self.get_inner_polygon_parameters(
				number_sides=number_sides_at_it,
				inscribed_side_length=inscribed_side_length_at_it)
			bisector_height = inner_polygon_parameters_at_it["height bisector"]
			outer_polygon_parameters_at_it = self.get_outer_polygon_parameters(
				number_sides=number_sides_at_it,
				inscribed_side_length=inscribed_side_length_at_it,
				bisector_height=bisector_height)
			lower_bound_by_perimeter_approximation_at_it = inner_polygon_parameters_at_it["perimeter"] / (2 * self.radius)
			upper_bound_by_perimeter_approximation_at_it = outer_polygon_parameters_at_it["perimeter"] / (2 * self.radius)
			lower_bound_by_area_approximation_at_it = inner_polygon_parameters_at_it["area"] / (self.radius ** 2)
			upper_bound_by_area_approximation_at_it = outer_polygon_parameters_at_it["area"] / (self.radius ** 2)
			value_by_perimeter_approximation_at_it = self.get_midpoint(
				lower_bound_by_perimeter_approximation_at_it,
				upper_bound_by_perimeter_approximation_at_it)
			value_by_area_approximation_at_it = self.get_midpoint(
				lower_bound_by_area_approximation_at_it,
				upper_bound_by_area_approximation_at_it)
			## update data containers
			numbers_sides.append(
				number_sides_at_it)
			lower_bounds_by_perimeter_approximation.append(
				lower_bound_by_perimeter_approximation_at_it)
			upper_bounds_by_perimeter_approximation.append(
				upper_bound_by_perimeter_approximation_at_it)
			lower_bounds_by_area_approximation.append(
				lower_bound_by_area_approximation_at_it)
			upper_bounds_by_area_approximation.append(
				upper_bound_by_area_approximation_at_it)
			values_by_perimeter_approximation.append(
				value_by_perimeter_approximation_at_it)
			values_by_area_approximation.append(
				value_by_area_approximation_at_it)
			## apply side-doubling
			inscribed_half_side_length = inner_polygon_parameters_at_it["half side-length"]
			radius_height_difference = inner_polygon_parameters_at_it["radius-height difference"]
			inscribed_side_length_at_it = np.sqrt(
				np.square(inscribed_half_side_length) + np.square(radius_height_difference))
			number_sides_at_it += number_sides_at_it ## addition preserves integer
			# number_sides_at_it *= 2
		## select last iteration as optimal estimate
		value_by_perimeter_approximation = values_by_perimeter_approximation[-1]
		value_by_area_approximation = values_by_area_approximation[-1]
		## collect attributes
		numbers_sides = np.array(
			numbers_sides)
		lower_bounds_by_perimeter_approximation = np.array(
			lower_bounds_by_perimeter_approximation)
		upper_bounds_by_perimeter_approximation = np.array(
			upper_bounds_by_perimeter_approximation)
		lower_bounds_by_area_approximation = np.array(
			lower_bounds_by_area_approximation)
		upper_bounds_by_area_approximation = np.array(
			upper_bounds_by_area_approximation)
		values_by_perimeter_approximation = np.array(
			values_by_perimeter_approximation)
		values_by_area_approximation = np.array(
			values_by_area_approximation)
		iterations = np.array(
			list(
				range(
					numbers_sides.size)))
		self._number_final_sides = number_sides_at_it
		self._numbers_sides = numbers_sides
		self._iterations = iterations
		self._lower_bounds_by_perimeter_approximation = lower_bounds_by_perimeter_approximation
		self._upper_bounds_by_perimeter_approximation = upper_bounds_by_perimeter_approximation
		self._lower_bounds_by_area_approximation = lower_bounds_by_area_approximation
		self._upper_bounds_by_area_approximation = upper_bounds_by_area_approximation
		self._values_by_perimeter_approximation = values_by_perimeter_approximation
		self._values_by_area_approximation = values_by_area_approximation
		self._value_by_perimeter_approximation = value_by_perimeter_approximation
		self._value_by_area_approximation = value_by_area_approximation

	def get_inner_polygon_parameters(self, number_sides, inscribed_side_length):
		inscribed_half_side_length = inscribed_side_length / 2
		bisector_height = np.sqrt(
			np.square(self.radius) - np.square(inscribed_half_side_length))
		radius_height_difference = self.radius - bisector_height
		perimeter = self.get_polygon_perimeter(
			number_sides=number_sides,
			side_length=inscribed_side_length)
		area = self.get_polygon_area(
			number_sides=number_sides,
			base=inscribed_side_length,
			height=bisector_height)
		parameters = {
			"side-length" : inscribed_side_length,
			"half side-length" : inscribed_half_side_length,
			"height bisector" : bisector_height,
			"radius-height difference" : radius_height_difference,
			"perimeter" : perimeter,
			"area" : area,
			}
		return parameters

	def get_outer_polygon_parameters(self, number_sides, inscribed_side_length, bisector_height):
		circumscribed_side_length = inscribed_side_length * (self.radius / bisector_height)
		circumscribed_half_side_length = circumscribed_side_length / 2
		perimeter = self.get_polygon_perimeter(
			number_sides=number_sides,
			side_length=circumscribed_side_length)
		area = self.get_polygon_area(
			number_sides=number_sides,
			base=circumscribed_side_length,
			height=self.radius)
		parameters = {
			"side-length" : circumscribed_side_length,
			"half side-length" : circumscribed_half_side_length,
			"perimeter" : perimeter,
			"area" : area,
			}
		return parameters

	@staticmethod
	def get_polygon_perimeter(number_sides, side_length):
		perimeter = number_sides * side_length
		return perimeter

	@staticmethod
	def get_polygon_area(number_sides, base, height):
		area = number_sides * (base * height) / 2
		return area

	@staticmethod
	def get_midpoint(a, b):
		midpoint = (a + b) / 2
		return midpoint

class EstimatorErrorConfiguration(BaseEstimatorConfiguration):

	def __init__(self):
		super().__init__()
		self._absolute_errors_by_perimeter_approximation = None ## at each iteration of side-doubling
		self._absolute_errors_by_area_approximation = None ## at each iteration of side-doubling
		self._relative_errors_by_perimeter_approximation = None ## at each iteration of side-doubling
		self._relative_errors_by_area_approximation = None ## at each iteration of side-doubling
		self._absolute_error_by_perimeter_approximation = None ## at last iteration
		self._absolute_error_by_area_approximation = None ## at last iteration
		self._relative_error_by_perimeter_approximation = None ## at last iteration
		self._relative_error_by_area_approximation = None ## at last iteration

	@property
	def absolute_errors_by_perimeter_approximation(self):
		return self._absolute_errors_by_perimeter_approximation
	
	@property
	def absolute_errors_by_area_approximation(self):
		return self._absolute_errors_by_area_approximation
	
	@property
	def relative_errors_by_perimeter_approximation(self):
		return self._relative_errors_by_perimeter_approximation
	
	@property
	def relative_errors_by_area_approximation(self):
		return self._relative_errors_by_area_approximation
	
	@property
	def absolute_error_by_perimeter_approximation(self):
		return self._absolute_error_by_perimeter_approximation
	
	@property
	def absolute_error_by_area_approximation(self):
		return self._absolute_error_by_area_approximation
	
	@property
	def relative_error_by_perimeter_approximation(self):
		return self._relative_error_by_perimeter_approximation
	
	@property
	def relative_error_by_area_approximation(self):
		return self._relative_error_by_area_approximation

	def get_absolute_error(self, value_by_approximation):
		absolute_error = np.abs(
			self.value_by_true - value_by_approximation)
		return absolute_error

	def get_relative_error(self, absolute_error):
		relative_error_as_decimal = absolute_error / self.value_by_true
		relative_error_as_percent = relative_error_as_decimal * 100
		return relative_error_as_decimal, relative_error_as_percent

	def initialize_errors(self):
		absolute_errors_by_perimeter_approximation = self.get_absolute_error(
			value_by_approximation=self.values_by_perimeter_approximation)
		absolute_errors_by_area_approximation = self.get_absolute_error(
			value_by_approximation=self.values_by_area_approximation)
		_, relative_errors_by_perimeter_approximation = self.get_relative_error(
			absolute_error=absolute_errors_by_perimeter_approximation)
		_, relative_errors_by_area_approximation = self.get_relative_error(
			absolute_error=absolute_errors_by_area_approximation)
		absolute_error_by_perimeter_approximation = absolute_errors_by_perimeter_approximation[-1]
		absolute_error_by_area_approximation = absolute_errors_by_area_approximation[-1]
		relative_error_by_perimeter_approximation = relative_errors_by_perimeter_approximation[-1]
		relative_error_by_area_approximation = relative_errors_by_area_approximation[-1]
		self._absolute_errors_by_perimeter_approximation = absolute_errors_by_perimeter_approximation
		self._absolute_errors_by_area_approximation = absolute_errors_by_area_approximation
		self._relative_errors_by_perimeter_approximation = relative_errors_by_perimeter_approximation
		self._relative_errors_by_area_approximation = relative_errors_by_area_approximation
		self._absolute_error_by_perimeter_approximation = absolute_error_by_perimeter_approximation
		self._absolute_error_by_area_approximation = absolute_error_by_area_approximation
		self._relative_error_by_perimeter_approximation = relative_error_by_perimeter_approximation
		self._relative_error_by_area_approximation = relative_error_by_area_approximation

class EstimatorConfiguration(EstimatorErrorConfiguration):

	def __init__(self):
		super().__init__()

	def __repr__(self):
		s = "EstimatorConfiguration()"
		return s

	def __str__(self):
		method_name = "\n .. method name:\n{}\n".format(
			self.method_name)
		radius = "\n .. radius:\n{}\n".format(
			self.radius)
		value_by_true = "\n .. true value:\n{:.10f}\n".format(
			self.value_by_true)
		value_by_perimeter_approximation = "\n .. approximate value (by perimeter):\n{:.10f}\n".format(
			self.value_by_perimeter_approximation)
		relative_error_by_perimeter_approximation = "\n .. relative error of approximation (by perimeter):\n{:.10f}\n".format(
			self.relative_error_by_perimeter_approximation)
		value_by_area_approximation = "\n .. approximate value (by area):\n{:.10f}\n".format(
			self.value_by_area_approximation)
		relative_error_by_area_approximation = "\n .. relative error of approximation (by area):\n{:.10f}\n".format(
			self.relative_error_by_area_approximation)
		s = "\n".join([
			method_name,
			radius,
			value_by_true,
			value_by_perimeter_approximation,
			relative_error_by_perimeter_approximation,
			value_by_area_approximation,
			relative_error_by_area_approximation,
			])
		return s

	def initialize(self, radius=None, number_side_doublings=None):
		self.initialize_method_name()
		self.initialize_references()
		self.initialize_value_by_true()
		self.initialize_radius(
			radius=radius)
		self.initialize_number_initial_sides()
		self.initialize_number_side_doublings(
			number_side_doublings=number_side_doublings)
		self.update_side_doublings()
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

	def view_approximation_accuracy(self, *args, **kwargs):
		viewer = EstimatorAccuracyViewerConfiguration()
		viewer.initialize_visual_settings(
			tick_size=self.visual_settings.tick_size,
			label_size=self.visual_settings.label_size,
			text_size=self.visual_settings.text_size,
			cell_size=self.visual_settings.cell_size,
			title_size=self.visual_settings.title_size)
		viewer.update_save_directory(
			path_to_save_directory=self.visual_settings.path_to_save_directory)
		viewer.view_approximation_accuracy(
			self, ## estimator,
			*args,
			**kwargs)

	def view_approximation_error(self, *args, **kwargs):
		viewer = EstimatorAccuracyViewerConfiguration()
		viewer.initialize_visual_settings(
			tick_size=self.visual_settings.tick_size,
			label_size=self.visual_settings.label_size,
			text_size=self.visual_settings.text_size,
			cell_size=self.visual_settings.cell_size,
			title_size=self.visual_settings.title_size)
		viewer.update_save_directory(
			path_to_save_directory=self.visual_settings.path_to_save_directory)
		viewer.view_approximation_error(
			self, ## estimator,
			*args,
			**kwargs)

##