from plotter_base_configuration import BasePlotterConfiguration
import numpy as np
import matplotlib.pyplot as plt


class BaseEnsembleAccuracyViewerConfiguration(BasePlotterConfiguration):

	def __init__(self):
		super().__init__()

	@staticmethod
	def plot_standard_deviation_fill(ax, ensemble, color="purple"):
		mean_values = ensemble.statistics["mean"]
		st_dev_values = ensemble.statistics["standard deviation"]
		y1 = np.clip(
			mean_values - st_dev_values,
			a_min=0,
			a_max=None)
		y2 = np.clip(
			mean_values + st_dev_values,
			a_min=0,
			a_max=None)
		label = "Within $1$ Standard Deviation\n of Mean Approximation Value"
		ax.fill_between(
			ensemble.variable_number_points,
			y1,
			y2,
			color=color,
			alpha=0.225,
			label=label,
			)
		return ax

	@staticmethod
	def plot_mean_values(ax, ensemble, color="darkorange"):
		label = "Mean Approximation Value"
		ax.plot(
			ensemble.variable_number_points,
			ensemble.statistics["mean"],
			color=color,
			alpha=0.8,
			linestyle="-",
			label=label,
			)
		return ax

	@staticmethod
	def plot_median_values(ax, ensemble, color="steelblue"):
		label = "Median Approximation Value"
		ax.plot(
			ensemble.variable_number_points,
			ensemble.statistics["median"],
			color=color,
			alpha=0.8,
			linestyle="-",
			label=label,
			)
		return ax

	@staticmethod
	def plot_true_values(ax, ensemble, color="forestgreen"):
		y = np.full(
			fill_value=ensemble.value_by_true,
			shape=ensemble.variable_number_points.shape)
		label = r"True Value of $\pi$"
		ax.plot(
			ensemble.variable_number_points,
			y,
			color=color,
			alpha=0.8,
			linestyle="--",
			label=label,
			)
		return ax

	def autoformat_plot(self, ax, ensemble):
		x_major_fmt = "${:,}$"
		y_major_fmt = "${:,.8}$"			
		xlabel = "Number of Points"
		ylabel = "Approximation Value"
		xlim = [
			ensemble.variable_number_points[0],
			ensemble.variable_number_points[-1],
			]
		ax = self.visual_settings.autoformat_axis_ticks_and_ticklabels(
			ax=ax,
			x_major_ticks=True,
			x_minor_ticks=True,
			y_major_ticks=True,
			y_minor_ticks=True,
			x_major_ticklabels=True,
			x_minor_ticklabels=False,
			y_major_ticklabels=True,
			y_minor_ticklabels=False,
			x_major_fmt=x_major_fmt,
			y_major_fmt=y_major_fmt,
			)
		ax = self.visual_settings.autoformat_grid(
			ax=ax,
			grid_color="gray")
		title = "Ensemble: {}".format(
			ensemble.method_name)
		ax = self.visual_settings.autoformat_axis_labels(
			ax=ax,
			xlabel=xlabel,
			ylabel=ylabel,
			title=title)
		ax = self.visual_settings.autoformat_axis_limits(
			ax=ax,
			xlim=xlim)
		return ax

	def autoformat_legend(self, fig, ax):
		handles, labels = ax.get_legend_handles_labels()
		number_columns = len(
			labels)
		if number_columns > 5:
			if number_columns % 2 == 0:
				number_columns = number_columns // 2
			else:
				number_columns = 4
		# bbox_to_anchor = [
		# 	0,
		# 	-0.1375,
		# 	1,
		# 	1,
		# 	]
		# leg_kwargs = {
		# 	"bbox_to_anchor" : bbox_to_anchor,
		# 	"bbox_transform" : fig.transFigure,
		# 	}
		leg = self.visual_settings.get_legend(
			fig=fig,
			ax=ax,
			handles=handles,
			labels=labels,
			number_columns=number_columns,
			# **leg_kwargs,
			)
		return fig, ax, leg

class EnsembleAccuracyViewerConfiguration(BaseEnsembleAccuracyViewerConfiguration):

	def __init__(self):
		super().__init__()

	def view_approximation_accuracy(self, ensemble, figsize=None, is_save=False):
		fig, ax = plt.subplots(
			figsize=figsize)
		ax = self.plot_standard_deviation_fill(
			ax=ax,
			ensemble=ensemble)
		ax = self.plot_mean_values(
			ax=ax,
			ensemble=ensemble)
		ax = self.plot_median_values(
			ax=ax,
			ensemble=ensemble)
		ax = self.plot_true_values(
			ax=ax,
			ensemble=ensemble)
		ax = self.autoformat_plot(
			ax=ax,
			ensemble=ensemble)
		fig, ax, leg = self.autoformat_legend(
			fig=fig,
			ax=ax)
		save_name = "ensemble_approximation_accuracy" if is_save else None
		self.visual_settings.display_image(
			fig=fig,
			save_name=save_name,
			space_replacement="_")







##