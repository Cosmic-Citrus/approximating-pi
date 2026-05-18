from plotter_base_configuration import BasePlotterConfiguration
import numpy as np
import matplotlib.pyplot as plt


class BaseEstimatorAccuracyViewerConfiguration(BasePlotterConfiguration):

	def __init__(self):
		super().__init__()

	@staticmethod
	def plot_empty_handle_by_radius_label(ax, estimator):
		label = "Inner/Outer Polygons\nusing Circle of Radius\n$r={:,.10}$".format(
			float(
				estimator.radius,
				),
			)
		ax.scatter(
			list(),
			list(),
			color="none",
			alpha=0,
			label=label)
		return ax

	@staticmethod
	def plot_true_value(ax, estimator, facecolor="black"):
		label = r"True Value of $\pi$"
		ax.plot(
			estimator.iterations,
			np.full(
				fill_value=estimator.value_by_true,
				shape=estimator.iterations.shape),
			color=facecolor,
			alpha=0.8,
			label=label,
			linestyle=":",
			)
		return ax

	@staticmethod
	def plot_approximation_value_by_perimeter_midpoint(ax, estimator, facecolor="steelblue"):
		label = "Midpoint of\nApproximation Bounds\nby Perimeter"
		ax.plot(
			estimator.iterations,
			estimator.values_by_perimeter_approximation,
			color=facecolor,
			alpha=0.8,
			label=label,
			linestyle="--",
			)
		ax.scatter(
			estimator.iterations,
			estimator.values_by_perimeter_approximation,
			color=facecolor,
			alpha=0.8,
			marker=".",
			)
		return ax

	@staticmethod
	def plot_approximation_value_by_area_midpoint(ax, estimator, facecolor="crimson"):
		label = "Midpoint of\nApproximation Bounds\nby Area"
		ax.plot(
			estimator.iterations,
			estimator.values_by_area_approximation,
			color=facecolor,
			alpha=0.8,
			label=label,
			linestyle="--",
			)
		ax.scatter(
			estimator.iterations,
			estimator.values_by_area_approximation,
			color=facecolor,
			alpha=0.8,
			marker=".",
			)
		return ax

	@staticmethod
	def plot_approximation_fill_by_bounded_perimeter(ax, estimator, facecolor="steelblue"):
		# label = "Approximation Bounds by\nPerimeter"
		label = r"perimeter(inner) < $2 \pi r$ < perimeter(outer)"
		ax.fill_between(
			estimator.iterations,
			estimator.lower_bounds_by_perimeter_approximation,
			estimator.upper_bounds_by_perimeter_approximation,
			color=facecolor,
			alpha=0.125,
			label=label)
		return ax

	@staticmethod
	def plot_approximation_fill_by_bounded_area(ax, estimator, facecolor="crimson"):
		# label = "Approximation Bounds by\nArea"
		label = r"area(inner) < $\pi r^2$ < area(outer)"
		ax.fill_between(
			estimator.iterations,
			estimator.lower_bounds_by_area_approximation,
			estimator.upper_bounds_by_area_approximation,
			color=facecolor,
			alpha=0.125,
			label=label)
		return ax

	@staticmethod
	def plot_relative_error_by_perimeter_approximation(ax, estimator, facecolor="steelblue"):
		label = "Relative Error of\nMidpoint Approximation \nby Bounded Perimeters"
		ax.plot(
			estimator.iterations,
			estimator.relative_errors_by_perimeter_approximation,
			color=facecolor,
			alpha=0.8,
			linestyle="--",
			label=label,
			)
		ax.scatter(
			estimator.iterations,
			estimator.relative_errors_by_perimeter_approximation,
			color=facecolor,
			alpha=0.8,
			marker=".",
			)
		return ax

	@staticmethod
	def plot_relative_error_by_area_approximation(ax, estimator, facecolor="crimson"):
		label = "Relative Error of\nMidpoint Approximation \nby Bounded Areas"
		ax.plot(
			estimator.iterations,
			estimator.relative_errors_by_area_approximation,
			color=facecolor,
			alpha=0.8,
			linestyle="--",
			label=label,
			)
		ax.scatter(
			estimator.iterations,
			estimator.relative_errors_by_area_approximation,
			color=facecolor,
			alpha=0.8,
			marker=".",
			)
		return ax

	def autoformat_plot(self, ax, estimator, is_show_error):
		## labels
		xlabel = "Number of Polygon Sides"
		if is_show_error:
			ylabel = "Relative Error of Approximation\n" + r"$(\%)$"
		else:
			ylabel = "Approximation Value"
		title = "{}".format(
			estimator.method_name)
		ax = self.visual_settings.autoformat_axis_labels(
			ax=ax,
			xlabel=xlabel,
			ylabel=ylabel,
			title=title)
		## ticks
		x_major_ticks = np.copy(
			estimator.iterations)
		x_major_ticklabels = np.copy(
			estimator.numbers_sides)
		ax = self.visual_settings.autoformat_axis_ticks_and_ticklabels(
			ax=ax,
			x_major_ticks=x_major_ticks,
			x_minor_ticks=True,
			y_major_ticks=True,
			y_minor_ticks=True,
			x_major_ticklabels=x_major_ticklabels,
			x_minor_ticklabels=False,
			y_major_ticklabels=True,
			y_minor_ticklabels=False,
			x_major_fmt="{:,}",
			y_major_fmt="{:.10}")
		ax = self.visual_settings.autoformat_grid(
			ax=ax,
			grid_color="gray")
		## limits
		xlim = [
			estimator.iterations[0],
			estimator.iterations[-1],
			]
		ax = self.visual_settings.autoformat_axis_limits(
			ax=ax,
			xlim=xlim)
		if is_show_error:
			ax.set_ylim(
				bottom=0)
		##
		return ax

	def autoformat_legend(self, fig, ax):
		handles, labels = ax.get_legend_handles_labels()
		number_columns = len(
			labels)
		if number_columns > 4:
			if number_columns % 2 == 0:
				number_columns = number_columns // 2
			else:
				number_columns = 3
		bbox_to_anchor = [
			0,
			-0.1375,
			1,
			1,
			]
		leg_kwargs = {
			"bbox_to_anchor" : bbox_to_anchor,
			"bbox_transform" : fig.transFigure,
			}
		leg = self.visual_settings.get_legend(
			fig=fig,
			ax=ax,
			handles=handles,
			labels=labels,
			number_columns=number_columns,
			**leg_kwargs,
			)
		return fig, ax, leg

class EstimatorAccuracyViewerConfiguration(BaseEstimatorAccuracyViewerConfiguration):

	def __init__(self):
		super().__init__() 

	def view_approximation_accuracy(self, estimator, figsize=None, is_save=False):
		fig, ax = plt.subplots(
			figsize=figsize)
		ax = self.plot_empty_handle_by_radius_label(
			ax=ax,
			estimator=estimator)
		ax = self.plot_true_value(
			ax=ax,
			estimator=estimator)
		ax = self.plot_approximation_value_by_perimeter_midpoint(
			ax=ax,
			estimator=estimator)
		ax = self.plot_approximation_value_by_area_midpoint(
			ax=ax,
			estimator=estimator)
		ax = self.plot_approximation_fill_by_bounded_perimeter(
			ax=ax,
			estimator=estimator)
		ax = self.plot_approximation_fill_by_bounded_area(
			ax=ax,
			estimator=estimator)
		ax = self.autoformat_plot(
			ax=ax,
			estimator=estimator,
			is_show_error=False)
		fig, ax, leg = self.autoformat_legend(
			fig=fig,
			ax=ax)
		save_name = "approximation_accuracy" if is_save else None
		self.visual_settings.display_image(
			fig=fig,
			save_name=save_name)

	def view_approximation_error(self, estimator, figsize=None, is_save=False):
		fig, ax = plt.subplots(
			figsize=figsize)
		ax = self.plot_relative_error_by_perimeter_approximation(
			ax=ax,
			estimator=estimator)
		ax = self.plot_relative_error_by_area_approximation(
			ax=ax,
			estimator=estimator)
		ax = self.autoformat_plot(
			ax=ax,
			estimator=estimator,
			is_show_error=True)
		fig, ax, leg = self.autoformat_legend(
			fig=fig,
			ax=ax)
		save_name = "approximation_error" if is_save else None
		self.visual_settings.display_image(
			fig=fig,
			save_name=save_name)

##