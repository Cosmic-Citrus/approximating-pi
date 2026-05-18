from estimator_configuration import EstimatorConfiguration


# is_save, path_to_save_directory = False, None
is_save, path_to_save_directory = True, "/Users/owner/Desktop/programming/pi_estimation/archimedes_method/output/"


if __name__ == "__main__":

	## initialize estimator
	estimator = EstimatorConfiguration()
	estimator.initialize(
		radius=1,
		number_side_doublings=5)
	print(
		estimator)

	## plot
	estimator.initialize_visual_settings()
	estimator.update_save_directory(
		path_to_save_directory=path_to_save_directory)

	estimator.view_approximation_method(
		figsize=(11, 7),
		is_save=is_save,
		extension=".gif")
	estimator.view_approximation_accuracy(
		figsize=(12, 7),
		is_save=is_save)
	estimator.view_approximation_error(
		figsize=(12, 7),
		is_save=is_save)

##