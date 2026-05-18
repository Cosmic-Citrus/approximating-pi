from plotter_base_configuration import BasePlotterConfiguration
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


class BaseEnsembleHistogramViewerConfiguration(BasePlotterConfiguration):

	def __init__(self):
		super().__init__()

	@staticmethod
	def get_frame_parameters(ensemble, fps):
		number_frames = int(
			ensemble.number_estimators) # * ensemble.number_trial_runs
		frames = range(
			number_frames)
		if fps is None:
			fps = 12
		else:
			if not isinstance(fps, int):
				raise ValueError("invalid type(fps): {}".format(type(fps)))
			if fps <= 0:
				raise ValueError("invalid fps: {}".format(fps))
		return number_frames, frames, fps

	@staticmethod
	def plot_histogram(ax, bin_midpoints, width, bin_counts, bin_color="gray", label=None):
		kwargs = {
			"align" : "center",
			"width" : width,
			"facecolor" : bin_color,
			"alpha" : 0.3,
			}
		if label is not None:
			kwargs["label"] = label
		handle_by_bar = ax.bar(
			bin_midpoints,
			bin_counts,
			**kwargs)
		return ax, handle_by_bar

	@staticmethod
	def plot_true_value(ax, ensemble, true_color="darkorange"):
		label = r"True Value of $\pi$"
		handle_by_true = ax.axvline(
			x=ensemble.value_by_true,
			color=true_color,
			label=label,
			linestyle="--")
		return ax, handle_by_true

	@staticmethod
	def plot_empty_legend_handle(ax, ensemble, approximation_color="purple", mean_color="black", median_color="forestgreen"):
		label_by_approximation_values = "Approximation Values"
		label_by_mean_approximation = "Mean Approximation"
		label_by_median_approximation = "Median Approximation"
		handle_by_trial, = ax.plot(
			list(),
			list(),
			color=approximation_color,
			label=label_by_approximation_values)
		handle_by_mean, = ax.plot(
			list(),
			list(),
			color=mean_color,
			label=label_by_mean_approximation,
			linestyle="--")
		handle_by_median, = ax.plot(
			list(),
			list(),
			color=median_color,
			label=label_by_median_approximation,
			linestyle="--")
		handles = [
			handle_by_trial,
			handle_by_mean,
			handle_by_median,
			]
		return ax, handles

	def autoformat_plot(self, ax, ensemble, bin_edges):
		x_major_fmt = "${:,.10}$"
		y_major_fmt = "${:,.3}$"			
		xlabel = "Approximation Value"
		ylabel = "Multiplicity"
		xlim = [
			bin_edges[0],
			bin_edges[-1],
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

	def autoformat_legend(self, fig, ax, ensemble):
		handles, labels = ax.get_legend_handles_labels()
		number_columns = len(
			labels)
		if number_columns > 5:
			if number_columns % 2 == 0:
				number_columns = number_columns // 2
			else:
				number_columns = 4
		leg_title = r"${:,}$ Trials for each of ${:,}$ Variable Number of Points".format(
			int(
				ensemble.optimal_estimator.number_trial_runs),
			int(
				ensemble.variable_number_points.size),
			)
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
			title=leg_title,
			# **leg_kwargs,
			)
		return fig, ax, leg

	def get_animation_handles(self, ax, approximation_color="purple", mean_color="black", median_color="forestgreen", text_color="black"):
		handle_by_approximation_step, = ax.step(
			list(),
			list(),
			where="mid",
			color=approximation_color)
		handle_by_mean = ax.axvline(
			x=np.pi,
			color=mean_color,
			alpha=0,
			linestyle="--")
		handle_by_median = ax.axvline(
			x=np.pi,
			color=median_color,
			alpha=0,
			linestyle="--")
		handle_by_text = ax.text(
			0.5,
			-0.1375,
			"",
			fontsize=self.visual_settings.text_size,
			color=text_color,
			horizontalalignment="center",
			verticalalignment="center",
			transform=ax.transAxes)
		anim_handles = [
			handle_by_approximation_step,
			handle_by_mean,
			handle_by_median,
			handle_by_text,
			]
		return ax, anim_handles

class EnsembleHistogramViewerConfiguration(BaseEnsembleHistogramViewerConfiguration):

	def __init__(self):
		super().__init__()

	def view_histogram_of_approximation_values(self, ensemble, fps=None, figsize=None, is_save=False, extension=None, **kwargs):
		
		def update_frame(index_at_frame, ensemble, anim_handles, bin_midpoints, bin_edges):
			[handle_by_approximation_step, handle_by_mean, handle_by_median, handle_by_text] = anim_handles
			estimator = ensemble.estimators[index_at_frame]
			trial_values = estimator.trial_data["approximation values"]
			bin_counts, _ = np.histogram(
				trial_values,
				bins=bin_edges)
			handle_by_approximation_step.set_xdata(
				bin_midpoints)
			handle_by_approximation_step.set_ydata(
				bin_counts)
			handle_by_mean.set_xdata([
				estimator.statistics["mean"],
				estimator.statistics["mean"],
				])
			handle_by_mean.set_alpha(
				0.8)
			handle_by_median.set_xdata([
				estimator.statistics["median"],
				estimator.statistics["median"],
				])
			handle_by_median.set_alpha(
				0.8)
			top_label = r"mean approximation: $\pi \approx {:,.8}$".format(
				estimator.value_by_approximation)
			bottom_label = r"relative error of mean approximation: ${:,.8} \%$".format(
				estimator.relative_error * 100)
			label = "{}\n{}".format(
				top_label,
				bottom_label)
			handle_by_text.set_text(
				label)
			return [handle_by_approximation_step, handle_by_mean, handle_by_median, handle_by_text]

		number_frames, frames, fps = self.get_frame_parameters(
			ensemble=ensemble,
			fps=fps)
		bin_counts, bin_edges = np.histogram(
			ensemble.statistics["mean"],
			**kwargs)
		# rescaled_bin_counts = bin_counts / ensemble.variable_number_points.size 
		rescaled_bin_counts = bin_counts / (ensemble.optimal_estimator.number_trial_runs * ensemble.variable_number_points.size * np.mean(np.diff(bin_edges)))
		bin_midpoints = (bin_edges[:-1] + bin_edges[1:]) / 2
		width = np.diff(
			bin_edges)
		label_by_bar = "Normalized Histogram"
		fig, ax = plt.subplots(
			figsize=figsize)
		ax, handle_by_bar = self.plot_histogram(
			ax=ax,
			bin_midpoints=bin_midpoints,
			width=width,
			bin_counts=rescaled_bin_counts, # bin_counts,
			label=label_by_bar)
		ax, handle_by_true = self.plot_true_value(
			ax=ax,
			ensemble=ensemble)
		ax, _ = self.plot_empty_legend_handle(
			ax=ax,
			ensemble=ensemble)
		ax = self.autoformat_plot(
			ax=ax,
			ensemble=ensemble,
			bin_edges=bin_edges)
		fig, ax, leg = self.autoformat_legend(
			fig=fig,
			ax=ax,
			ensemble=ensemble)
		ax, anim_handles = self.get_animation_handles(
			ax=ax)
		fargs = (
			ensemble,
			anim_handles,
			bin_midpoints,
			bin_edges,
			)
		anim = FuncAnimation(
			fig,
			update_frame,
			fargs=fargs,
			frames=frames,
			blit=True,
			interval=100,
			)
		save_name = "ensemble_approximation_histogram" if is_save else None
		self.visual_settings.display_animation(
			anim,
			fps=fps,
			save_name=save_name,
			space_replacement="_",
			extension=extension)

##