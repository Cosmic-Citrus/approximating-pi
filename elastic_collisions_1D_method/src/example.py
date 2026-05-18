from estimator_configuration import EstimatorConfiguration
import numpy as np


# is_save, path_to_save_directory = False, None
is_save, path_to_save_directory = True, "/Users/owner/Desktop/programming/pi_estimation/elastic_collisions_1D_method/output/"


if __name__ == "__main__":

	## initialize estimator
	estimator = EstimatorConfiguration()
	estimator.initialize(
		mass_ratio_power=2,
		# mass_ratio_power=3,
		)
	print(
		estimator)

	## plot
	estimator.initialize_visual_settings()
	estimator.update_save_directory(
		path_to_save_directory=path_to_save_directory)
	estimator.view_velocities_against_time(
		figsize=(11, 7),
		is_save=is_save)
	estimator.view_phase_space(
		figsize=(11, 7),
		is_save=is_save)
	estimator.view_phase_space(
		figsize=(12, 9),
		is_save=is_save,
		is_animated=True,
		extension=".gif")

##