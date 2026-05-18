from estimator_configuration import EstimatorConfiguration


# is_save, path_to_save_directory = False, None
is_save, path_to_save_directory = True, "/Users/owner/Desktop/programming/pi_estimation/mandelbrot_method/output/"


if __name__ == "__main__":

	## initialize estimator
	estimator = EstimatorConfiguration()
	estimator.initialize(
		c_real=-0.75,
		number_digits=5)
	print(
		estimator)

	## plot
	estimator.initialize_visual_settings()
	estimator.update_save_directory(
		path_to_save_directory=path_to_save_directory)

	# constant = -0.743643 + 0.131825 * 1j ## fractal-zoom is infinite
	constant = None ## use constant from estimator 
	estimator.view_mandelbrot_set(
		resolution=1080,
		constant=constant,
		is_show_constant=True,
		is_log_color=True,
		figsize=(11, 6),
		is_save=is_save,
		is_animated=False,
		)
	estimator.view_mandelbrot_set(
		resolution=1080,
		constant=constant,
		is_show_constant=True,
		is_log_color=True,
		number_maximum_iterations=360,
		figsize=(11, 6),
		is_save=is_save,
		is_animated=True,
		extension=".gif",
		)

	estimator.view_mandelbrot_set(
		resolution=1080,
		constant=constant,
		is_show_constant=True,
		is_log_color=False,
		number_maximum_iterations=360,
		figsize=(11, 6),
		is_save=is_save,
		is_animated=True,
		extension=".gif",
		)


	estimator.view_mandelbrot_set(
		resolution=1080,
		constant=constant,
		is_show_constant=False,
		is_log_color=True,
		number_maximum_iterations=360,
		figsize=(11, 6),
		is_save=is_save,
		is_animated=True,
		extension=".gif",
		)

	estimator.view_mandelbrot_set(
		resolution=1080,
		constant=constant,
		is_show_constant=False,
		is_log_color=False,
		number_maximum_iterations=360,
		figsize=(11, 6),
		is_save=is_save,
		is_animated=True,
		extension=".gif",
		)







##