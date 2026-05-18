from estimator_configuration import EstimatorConfiguration
from plotter_ensemble_accuracy_configuration import EnsembleAccuracyViewerConfiguration
from plotter_ensemble_histogram_configuration import EnsembleHistogramViewerConfiguration
import numpy as np


class BaseEnsembleConfiguration(EstimatorConfiguration):

	def __init__(self):
		super().__init__()
		self._variable_number_points = None
		self._number_estimators = None
		self._estimators = None
		self._optimal_estimator = None
		self._statistics = None

	@property
	def variable_number_points(self):
		return self._variable_number_points
	
	@property
	def number_estimators(self):
		return self._number_estimators
	
	@property
	def estimators(self):
		return self._estimators
	
	@property
	def optimal_estimator(self):
		return self._optimal_estimator

	@property
	def statistics(self):
		return self._statistics
	
	@staticmethod
	def get_default_variable_number_points():
		variable_number_points = np.arange(
			1000,
			10_000 + 1,
			1000,
			)
		return variable_number_points

	def initialize_variable_number_points(self, variable_number_points):
		if variable_number_points is None:
			modified_variable_number_points = self.get_default_variable_number_points()
		elif isinstance(variable_number_points, (tuple, list, np.ndarray)):
			modified_variable_number_points = np.sort(
				variable_number_points).astype(
					int)
		else:
			raise ValueError("invalid type(variable_number_points): {}".format(type(variable_number_points)))
		self._variable_number_points = modified_variable_number_points

	def initialize_estimators(self):
		estimators = list()
		for number_points in self.variable_number_points:
			estimator = EstimatorConfiguration()
			estimator.initialize_visual_settings(
				tick_size=self.visual_settings.tick_size,
				label_size=self.visual_settings.label_size,
				text_size=self.visual_settings.text_size,
				cell_size=self.visual_settings.cell_size,
				title_size=self.visual_settings.title_size)
			estimator.update_save_directory(
				path_to_save_directory=self.visual_settings.path_to_save_directory)
			estimator.initialize(
				number_dimensions=self.number_dimensions,
				number_trial_runs=self.number_trial_runs,
				number_points=number_points,
				radius=self.radius,
				random_state_seed=None, # self.random_state_seed,
				)
			estimators.append(
				estimator)
		number_estimators = len(
			estimators)
		key_func = lambda index_at_estimator : estimators[index_at_estimator].relative_error
		index_at_optimal_estimator = min(
			range(
				number_estimators),
			key=key_func)
		optimal_estimator = estimators[index_at_optimal_estimator]		
		self._number_estimators = number_estimators
		self._estimators = estimators
		self._optimal_estimator = optimal_estimator

	def initialize_statistics(self):
		mean_values = list()
		median_values = list()
		st_dev_values = list()
		minimum_values = list()
		maximum_values = list()
		for estimator in self.estimators:
			mean_values.append(
				estimator.statistics["mean"])
			median_values.append(
				estimator.statistics["median"])
			st_dev_values.append(
				estimator.statistics["standard deviation"])
			minimum_values.append(
				estimator.statistics["minimum"])
			maximum_values.append(
				estimator.statistics["maximum"])
		statistics = {
			"mean" : np.array(
				mean_values),
			"median" : np.array(
				median_values),
			"standard deviation" : np.array(
				st_dev_values),
			"minimum" : np.array(
				minimum_values),
			"maximum" : np.array(
				maximum_values),
			}
		self._statistics = statistics

class EnsembleConfiguration(BaseEnsembleConfiguration):

	def __init__(self):
		super().__init__()

	def __repr__(self):
		return r"EnsembleConfiguration()"

	def __str__(self):
		method_name = "\n .. method name:\n{}\n".format(
			self.method_name)
		number_dimensions = "number dimensions:\n{:,}\n".format(
			self.number_dimensions)
		number_trial_runs = "number trial runs:\n{:,}\n".format(
			self.number_trial_runs)
		variable_number_points = "\n .. number of points (variable parameter):\n{:,} - {:,}\n".format(
			self.variable_number_points[0],
			self.variable_number_points[-1])
		radius = "\n .. radius:\n{}\n".format(
			self.radius)
		side_length = "side length:\n{}\n".format(
			self.side_length)
		value_by_true = "\n .. true value:\n{:.10f}\n".format(
			self.value_by_true)
		value_by_optimal_approximation = "\n .. approximation value by optimal estimator:\n{:.10f}\n".format(
			self.optimal_estimator.value_by_approximation)
		mean_optimal_relative_error = "\n .. mean relative error of approximation by optimal estimator:\n{}\n".format(
				self.optimal_estimator.relative_error)
		s = "\n".join([
			method_name,
			number_dimensions,
			number_trial_runs,
			variable_number_points,
			radius,
			side_length,
			value_by_true,
			value_by_optimal_approximation,
			mean_optimal_relative_error,
			])
		return s

	def initialize(self, variable_number_points=None, number_dimensions=None, number_trial_runs=None, radius=None, random_state_seed=None):
		self.initialize_method_name()
		self.initialize_references()
		if random_state_seed is not None:
			self.update_random_state_seed(
				random_state_seed=random_state_seed)
		self.initialize_value_by_true()
		self.initialize_number_dimensions(
			number_dimensions=number_dimensions)
		self.initialize_number_trial_runs(
			number_trial_runs=number_trial_runs)
		self.initialize_variable_number_points(
			variable_number_points=variable_number_points)
		self.initialize_radius(
			radius=radius)
		self.initialize_side_length()
		self.initialize_estimators()
		self.initialize_statistics()

	def view_approximation_accuracy(self, *args, **kwargs):
		viewer = EnsembleAccuracyViewerConfiguration()
		viewer.initialize_visual_settings(
			tick_size=self.visual_settings.tick_size,
			label_size=self.visual_settings.label_size,
			text_size=self.visual_settings.text_size,
			cell_size=self.visual_settings.cell_size,
			title_size=self.visual_settings.title_size)
		viewer.update_save_directory(
			path_to_save_directory=self.visual_settings.path_to_save_directory)
		viewer.view_approximation_accuracy(
			self, ## ensemble,
			*args,
			**kwargs)

	def view_histogram_of_approximation_values(self, *args, **kwargs):
		viewer = EnsembleHistogramViewerConfiguration()
		viewer.initialize_visual_settings(
			tick_size=self.visual_settings.tick_size,
			label_size=self.visual_settings.label_size,
			text_size=self.visual_settings.text_size,
			cell_size=self.visual_settings.cell_size,
			title_size=self.visual_settings.title_size)
		viewer.update_save_directory(
			path_to_save_directory=self.visual_settings.path_to_save_directory)
		viewer.view_histogram_of_approximation_values(
			self, ## ensemble,
			*args,
			**kwargs)

##