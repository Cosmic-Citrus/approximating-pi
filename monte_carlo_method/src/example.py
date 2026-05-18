from estimator_configuration import EstimatorConfiguration
from ensemble_configuration import EnsembleConfiguration
import numpy as np


# is_save, path_to_save_directory = False, None
is_save, path_to_save_directory = True, "/Users/owner/Desktop/programming/pi_estimation/monte_carlo_method/output/"


if __name__ == "__main__":

	## initialize estimator
	estimator = EstimatorConfiguration()
	estimator.initialize(
		number_dimensions=2,
		number_trial_runs=100,
		number_points=10_000,
		radius=1,
		random_state_seed=0)
	print(
		estimator)

	## plot
	estimator.initialize_visual_settings()
	estimator.update_save_directory(
		path_to_save_directory=path_to_save_directory)
	estimator.view_approximation_method(
		fps=6,
		figsize=(11, 7),
		is_save=is_save,
		extension=".gif")
	
	## initialize ensemble
	ensemble = EnsembleConfiguration()
	ensemble.initialize_visual_settings() ## initializes visual settings for each estimator
	ensemble.update_save_directory(
		path_to_save_directory=path_to_save_directory)
	variable_number_points = np.arange(
		1_000, # 100,
		100_001, # 1001,
		1_000, # 100,
		dtype=int)
	ensemble.initialize(
		variable_number_points=variable_number_points,
		number_dimensions=2,
		number_trial_runs=100,
		radius=1,
		random_state_seed=0)
	print(
		ensemble)

	## plot ensemble
	ensemble.view_approximation_accuracy(
		figsize=(11, 7),
		is_save=is_save)
	ensemble.view_histogram_of_approximation_values(
		bins=24,
		fps=6,
		figsize=(11, 7),
		is_save=is_save,
		extension=".gif")

##