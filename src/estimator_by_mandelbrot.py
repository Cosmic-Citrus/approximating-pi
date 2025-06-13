from error_configuration import ErrorConfiguration
import numpy as np


class BaseEstimatorByMandelbrot():

	def __init__(self):
		super().__init__()
		self._name = None
		self._references = None
		self._number_digits = None
		self._eps = None
		self._c = None
		self._number_iterations = None
		self._value_estimate = None

	@property
	def name(self):
		return self._name

	@property
	def references(self):
		return self._references

	@property
	def number_digits(self):
		return self._number_digits
	
	@property
	def eps(self):
		return self._eps
	
	@property
	def c(self):
		return self._c
	
	@property
	def number_iterations(self):
		return self._number_iterations
	
	@property
	def value_estimate(self):
		return self._value_estimate

	def initialize_name(self):
		name = "Mandelbrot"
		self._name = name

	def initialize_references(self):
		references = {
			"video 1" : "https://www.youtube.com/watch?v=d0vY0CKYhPY"}
		self._references = references

	def initialize_number_digits(self, number_digits):
		if not isinstance(number_digits, int):
			raise ValueError("invalid type(number_digits): {}".format(type(number_digits)))
		if number_digits <= 0:
			raise ValueError("invalid number_digits: {}".format(number_digits))
		self._number_digits = number_digits

	def initialize_epsilon(self):
		eps = (1 / 10) ** self.number_digits
		self._eps = eps

	def initialize_constant(self):
		c = -1 * 0.75 + self.eps * 1j
		self._c = c

	def initialize_number_iterations(self):
		z = float(
			0)
		number_iterations = 0
		while True:
			if abs(z) >= 2:
				break
			z = (z ** 2) + self.c
			number_iterations += 1
		self._number_iterations = number_iterations

	def initialize_value_estimate(self):
		value_estimate = self.eps * self.number_iterations
		self._value_estimate = value_estimate

class EstimatorByMandelbrot(BaseEstimatorByMandelbrot):

	def __init__(self):
		super().__init__()

	def initialize(self, number_digits):
		self.initialize_name()
		self.initialize_references()
		self.initialize_number_digits(
			number_digits=number_digits)
		self.initialize_epsilon()
		self.initialize_constant()
		self.initialize_number_iterations()
		self.initialize_value_estimate()


if __name__ == "__main__":

	number_digits = 4
	estimator = EstimatorByMandelbrot()
	estimator.initialize(
		number_digits=number_digits)

	error_check = ErrorConfiguration()
	error_check.initialize(
		value_true=np.pi,
		value_estimate=estimator.value_estimate)

	print(estimator.name)
	print(error_check)

##