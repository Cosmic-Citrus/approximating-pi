from error_configuration import ErrorConfiguration
import numpy as np


class BaseEstimatorByOneDimensionalCollisions():

	def __init__(self):
		super().__init__()
		self._name = None
		self._references = None
		self._number_digits = None
		self._m1 = None
		self._m2 = None
		self._number_collisions = None
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
	def m1(self):
		return self._m1
	
	@property
	def m2(self):
		return self._m2

	@property
	def number_collisions(self):
		return self._number_collisions
	
	@property
	def value_estimate(self):
		return self._value_estimate
	
	def initialize_name(self):
		name = "1-D Collisions"
		self._name = name

	def initialize_references(self):
		references = {
			"video 1" : "https://www.youtube.com/watch?v=HEfHFsfGXjs",
			"article 1" : "https://arxiv.org/pdf/1901.06260.pdf",
			"article 2" : "https://www.3blue1brown.com/lessons/clacks-solution"}
		self._references = references

	def initialize_number_digits(self, number_digits):
		if not isinstance(number_digits, int):
			raise ValueError("invalid type(number_digits): {}".format(type(number_digits)))
		if number_digits <= 1:
			raise ValueError("invalid number_digits: {}".format(number_digits))
		self._number_digits = number_digits

	def initialize_masses(self):
		m1 = 1
		m2 = 100 ** (self.number_digits - 1)
		self._m1 = m1
		self._m2 = m2

	def pre_initialize_number_collisions(self):
		self._number_collisions = 0

	def initialize_number_collisions(self):

		def is_last_collision(v1, v2):
			condition = ((v1 < v2) and (v2 > 0))
			return condition

		def evaluate_collision(v1, v2):
			p1 = self.m1 * v1
			p2 = self.m2 * v2
			dv = v2 - v1
			v1 = (p1 + p2 + self.m2 * dv) / (self.m1 + self.m2)
			v2 = (p1 + p2 + self.m1 * (-1 * dv)) / (self.m1 + self.m2)
			self._number_collisions += 1
			if v1 < 0:
				## bounce of wall
				v1 *= -1
				self._number_collisions += 1
			return v1, v2

		v1 = 0
		v2 = -10
		while True:
			if is_last_collision(v1, v2):
				break
			v1, v2 = evaluate_collision(
				v1=v1,
				v2=v2)

	def initialize_value_estimate(self):
		digits_as_string = str(
			self.number_collisions)
		value_as_string = digits_as_string[:1] + "." + digits_as_string[1:]
		value_estimate = float(
			value_as_string)
		self._value_estimate = value_estimate

class EstimatorByOneDimensionalCollisions(BaseEstimatorByOneDimensionalCollisions):

	def __init__(self):
		super().__init__()

	def initialize(self, number_digits):
		self.initialize_name()
		self.initialize_references()
		self.initialize_number_digits(
			number_digits=number_digits)
		self.initialize_masses()
		self.pre_initialize_number_collisions()
		self.initialize_number_collisions()
		self.initialize_value_estimate()


if __name__ == "__main__":

	number_digits = 4
	estimator = EstimatorByOneDimensionalCollisions()
	estimator.initialize(
		number_digits=number_digits)

	error_check = ErrorConfiguration()
	error_check.initialize(
		value_true=np.pi,
		value_estimate=estimator.value_estimate)

	print(estimator.name)
	print(error_check)

##