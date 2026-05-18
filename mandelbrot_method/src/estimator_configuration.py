from plotter_base_configuration import BasePlotterConfiguration
from plotter_estimator_method_configuration import EstimatorMethodViewerConfiguration
import numpy as np


class BasestEstimatorConfiguration(BasePlotterConfiguration):

	def __init__(self):
		super().__init__()
		self._method_name = None
		self._references = None
		self._value_by_true = None
		self._root_parameters = None
		self._value_by_approximation = None
	
	@property
	def root_parameters(self):
		return self._root_parameters

	@property
	def value_by_approximation(self):
		return self._value_by_approximation

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
		method_name = "Mandelbrot Set"
		self._method_name = method_name

	def initialize_references(self):
		references = {
			"video 1" : "https://www.youtube.com/watch?v=d0vY0CKYhPY",
			}
		self._references = references

	def initialize_value_by_true(self):
		value_by_true = np.pi
		self._value_by_true = value_by_true

	@staticmethod
	def f(z, c):
		z = (z ** 2) + c
		return z

	@staticmethod
	def get_default_c_real():
		c_real = -1 * 0.75
		return c_real

	def initialize_root_parameters(self, c_real, number_digits):
		if number_digits is None:
			number_digits = 5
		else:
			if not isinstance(number_digits, (int, np.int64)):
				raise ValueError("invalid type(number_digits): {}".format(type(number_digits)))
			if number_digits <= 0:
				raise ValueError("invalid number_digits: {}".format(number_digits))
		eps = (1 / 10) ** number_digits
		if c_real is None:
			c_real = self.get_default_c_real()
		elif not isinstance(c_real, (int, np.int64, float)):
			raise ValueError("invalid type(c_real): {}".format(type(c_real)))
		constant = c_real + eps * 1j
		upper_bound = 2
		number_iterations = 0
		z = 0
		while True:
			if abs(z) >= upper_bound:
				break
			z = self.f(
				z=z,
				c=constant)
			number_iterations += 1
		root_parameters = {
			"number digits" : number_digits,
			"epsilon" : eps,
			"constant" : constant,
			"z" : z,
			"number iterations" : number_iterations,
			}
		self._root_parameters = root_parameters

	def initialize_value_by_approximation(self):
		eps = self.root_parameters["epsilon"]
		number_iterations = self.root_parameters["number iterations"]
		value_by_approximation = eps * number_iterations
		self._value_by_approximation = value_by_approximation

class BaseEstimatorConfiguration(BasestEstimatorConfiguration):

	def __init__(self):
		super().__init__()

	@staticmethod
	def get_number_maximum_iterations(number_maximum_iterations):
		if number_maximum_iterations is None:
			number_maximum_iterations = 100
		else:
			if not isinstance(number_maximum_iterations, (int, np.int64)):
				raise ValueError("invalid type(number_maximum_iterations): {}".format(type(number_maximum_iterations)))
			if number_maximum_iterations <= 0:
				raise ValueError("invalid number_maximum_iterations: {}".format(number_maximum_iterations))
		return number_maximum_iterations

	def get_matrices_by_root_value_and_number_iterations(self, xlim, ylim, resolution, number_maximum_iterations):
		x = np.linspace(
			*xlim,
			resolution)
		y = np.linspace(
			*ylim,
			resolution)
		matrix_by_number_iterations = np.full(
			fill_value=0,
			shape=(
				y.size,
				x.size),
			dtype=int)
		matrix_by_root_value = np.full(
			fill_value=0,
			shape=(
				y.size,
				x.size),
			dtype=float)
		for r, yi in enumerate(y):
			for c, xi in enumerate(x):
				constant = xi + yi * 1j
				it, zi = self.get_number_iterations_by_mandelbrot(
					constant=constant,
					number_maximum_iterations=number_maximum_iterations)
				matrix_by_number_iterations[r, c] = it
				matrix_by_root_value[r, c] = zi
		return matrix_by_number_iterations, matrix_by_root_value

	def get_number_iterations_by_mandelbrot(self, constant, number_maximum_iterations):
		upper_bound = 2
		z = 0
		for it in range(number_maximum_iterations):
			if abs(z) >= upper_bound:
				break
			z = self.f(
				z=z,
				c=constant)
		return it, z

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
		constant = "\n .. constant:\n{}\n".format(
			self.root_parameters["constant"])
		z = "\n .. root z:\n{}\n".format(
			self.root_parameters["z"])
		number_iterations = "\n .. number iterations:\n{}\n".format(
			self.root_parameters["number iterations"])
		s = "\n".join([
			method_name,
			value_by_true,
			value_by_approximation,
			constant,
			z,
			number_iterations,
			])
		return s

	def initialize(self, number_digits=None, c_real=None):
		self.initialize_method_name()
		self.initialize_references()
		self.initialize_value_by_true()
		self.initialize_root_parameters(
			number_digits=number_digits,
			c_real=c_real)
		self.initialize_value_by_approximation()

	def view_mandelbrot_set(self, *args, **kwargs):
		viewer = EstimatorMethodViewerConfiguration()
		viewer.initialize_visual_settings(
			tick_size=self.visual_settings.tick_size,
			label_size=self.visual_settings.label_size,
			text_size=self.visual_settings.text_size,
			cell_size=self.visual_settings.cell_size,
			title_size=self.visual_settings.title_size)
		viewer.update_save_directory(
			path_to_save_directory=self.visual_settings.path_to_save_directory)
		viewer.view_mandelbrot_set(
			self, ## estimator,
			*args,
			**kwargs)

##