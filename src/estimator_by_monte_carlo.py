from error_configuration import ErrorConfiguration
import numpy as np


class BaseEstimatorByMonteCarlo():

	def __init__(self):
		super().__init__()
		self._name = None
		self._references = None
		self._radius = None
		self._side_length = None
		self._number_dimensions = None
		self._number_points_total = None
		self._number_points_inside_circle = None
		self._number_points_outside_circle = None
		self._value_estimate = None

	@property
	def name(self):
		return self._name

	@property
	def references(self):
		return self._references

	@property
	def radius(self):
		return self._radius
	
	@property
	def side_length(self):
		return self._side_length
	
	@property
	def number_dimensions(self):
		return self._number_dimensions
	
	@property
	def number_points_total(self):
		return self._number_points_total
	
	@property
	def number_points_inside_circle(self):
		return self._number_points_inside_circle
	
	@property
	def number_points_outside_circle(self):
		return self._number_points_outside_circle
	
	@property
	def value_estimate(self):
		return self._value_estimate

	def initialize_name(self):
		name = "Monte Carlo"
		self._name = name

	def initialize_references(self):
		references = {
			"article 1" : "https://arxiv.org/ftp/arxiv/papers/1909/1909.13212.pdf"}
		self._references = references

	def initialize_size(self, radius):
		if not isinstance(radius, (float, int)):
			raise ValueError("invalid type(radius): {}".format(type(radius)))
		if radius <= 0:
			raise ValueError("invalid radius: {}".format(radius))
		side_length = radius + radius
		number_dimensions = len([
			"x",
			"y"])
		self._radius = radius
		self._side_length = side_length
		self._number_dimensions = number_dimensions

	def initialize_number_points(self, number_points_total):
		if not isinstance(number_points_total, int):
			raise ValueError("invalid type(number_points_total): {}".format(type(number_points_total)))
		if number_points_total <= 0:
			raise ValueError("invalid number_points_total: {}".format(number_points_total))
		lower_bound = -1 * self.radius
		upper_bound = 1 * self.radius
		coordinates = np.random.uniform(
			low=lower_bound,
			high=upper_bound,
			size=(number_points_total, self.number_dimensions),
			)
		distances = np.sqrt(
			np.sum(
				np.square(
					coordinates),
				axis=1))
		is_points_inside_circle = (distances <= self.radius)
		number_points_inside_circle = int(
			np.sum(
				is_points_inside_circle))
		number_points_outside_circle = number_points_total - number_points_inside_circle
		self._number_points_total = number_points_total
		self._number_points_inside_circle = number_points_inside_circle
		self._number_points_outside_circle = number_points_outside_circle

	def initialize_value_estimate(self):
		number_quadrants = 4
		value_estimate = number_quadrants * self.number_points_inside_circle / self.number_points_total
		self._value_estimate = value_estimate

class EstimatorByMonteCarlo(BaseEstimatorByMonteCarlo):

	def __init__(self):
		super().__init__()

	def initialize(self, radius, number_points_total):
		self.initialize_name()
		self.initialize_references()
		self.initialize_size(
			radius=radius)
		self.initialize_number_points(
			number_points_total=number_points_total)
		self.initialize_value_estimate()

class BaseEstimatorByMonteCarloEnsemble(BaseEstimatorByMonteCarlo):

	def __init__(self):
		super().__init__()
		self._number_trials = None
		self._ensemble_value_estimates = None
		self._value_estimate_statistics = None

	@property
	def number_trials(self):
		return self._number_trials
		
	@property
	def ensemble_value_estimates(self):
		return self._ensemble_value_estimates
	
	@property
	def value_estimate_statistics(self):
		return self._value_estimate_statistics

	def initialize_name(self):
		name = "Monte Carlo Ensemble"
		self._name = name

	def initialize_number_trials(self, number_trials):
		if not isinstance(number_trials, int):
			raise ValueError("invalid type(number_trials): {}".format(type(number_trials)))
		if number_trials <= 0:
			raise ValueError("invalid number_trials: {}".format(number_trials))
		self._number_trials = number_trials

	def initialize_ensemble_value_estimates(self):
		ensemble_value_estimates = list()
		for trial_index in range(self.number_trials):
			estimator = EstimatorByMonteCarlo()
			estimator.initialize(
				radius=self.radius,
				number_points_total=self.number_points_total)
			ensemble_value_estimates.append(
				estimator.value_estimate)
		ensemble_value_estimates = np.array(
			ensemble_value_estimates)
		self._ensemble_value_estimates = ensemble_value_estimates

	def initialize_value_estimate_statistics(self):
		value_estimate_statistics = {
			"mean" : np.mean(
				self.ensemble_value_estimates),
			"median" : np.median(
				self.ensemble_value_estimates),
			"standard deviation" : np.std(				
				self.ensemble_value_estimates,
				ddof=1),
			"minimum" : np.min(
				self.ensemble_value_estimates),
			"maximum" : np.max(
				self.ensemble_value_estimates),
			}
		self._value_estimate_statistics = value_estimate_statistics

class EstimatorByMonteCarloEnsemble(BaseEstimatorByMonteCarloEnsemble):

	def __init__(self):
		super().__init__()

	def initialize(self, radius, number_points_total, number_trials):
		self.initialize_name()
		self.initialize_references()
		self.initialize_size(
			radius=radius)
		self.initialize_number_points(
			number_points_total=number_points_total)
		self.initialize_number_trials(
			number_trials=number_trials)
		self.initialize_ensemble_value_estimates()
		self.initialize_value_estimate_statistics()


if __name__ == "__main__":

	np.random.seed(
		0)
	estimator = EstimatorByMonteCarlo()
	estimator.initialize(
		radius=1,
		number_points_total=5000)

	error_check = ErrorConfiguration()
	error_check.initialize(
		value_true=np.pi,
		value_estimate=estimator.value_estimate)

	print(estimator.name)
	print(error_check)


	ensemble_estimator = EstimatorByMonteCarloEnsemble()
	ensemble_estimator.initialize(
		radius=1,
		number_points_total=5000,
		number_trials=100)

	ensemble_error_check = ErrorConfiguration()
	ensemble_error_check.initialize(
		value_true=np.pi,
		value_estimate=ensemble_estimator.value_estimate_statistics["mean"],
		# value_estimate=ensemble_estimator.value_estimate_statistics["median"],
		)

	print(ensemble_estimator.name)
	print(ensemble_error_check)
	print(ensemble_estimator.value_estimate_statistics)

##