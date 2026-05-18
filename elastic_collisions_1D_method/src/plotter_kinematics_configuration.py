from plotter_base_configuration import BasePlotterConfiguration
import numpy as np
import matplotlib.pyplot as plt


class BaseEstimatorKinematicsViewerConfiguration(BasePlotterConfiguration):

	def __init__(self):
		super().__init__()

	@staticmethod
	def plot_velocities_against_time(ax, t, v1, v2, color1="crimson", color2="steelblue"):
		label1 = r"$v_1(t)$"
		label2 = r"$v_2(t)$"
		ax.plot(
			t,
			v1,
			color=color1,
			label=label1)
		ax.plot(
			t,
			v2,
			color=color2,
			label=label2)
		return ax

	def autoformat_plot(self, ax, estimator, t, v1, v2):
		ax.set_aspect(
			"equal")
		xlabel = r"Number of Collisions"
		ylabel = r"Velocity $[\frac{m}{s}]$"
		ax = self.visual_settings.autoformat_axis_labels(
			ax=ax,
			xlabel=xlabel,
			ylabel=ylabel,
			title=estimator.method_name,
			)
		xlim = [
			t[0] - 1,
			t[-1],
			]
		ylim = [
			1.125 * min([
				np.min(
					v1),
				np.min(
					v2),
				]),
			1.125 * max([
				np.max(
					v1),
				np.max(
					v2),
				]),
			]
		ax = self.visual_settings.autoformat_axis_limits(
			ax=ax,
			xlim=xlim,
			ylim=ylim)
		ax = self.visual_settings.autoformat_axis_ticks_and_ticklabels(
			ax=ax,
			x_major_ticks=True,
			x_minor_ticks=True,
			y_major_ticks=True,
			y_minor_ticks=True,
			x_major_fmt="{:,.0f}",
			y_major_fmt="{:,.2f}",
			x_major_ticklabels=True,
			x_minor_ticklabels=False,
			y_major_ticklabels=True,
			y_minor_ticklabels=False)
		ax = self.visual_settings.autoformat_grid(
			ax=ax,
			grid_color="gray",
			)
		return ax

	def autoformat_legend(self, fig, ax, estimator):
		handles, labels = ax.get_legend_handles_labels()
		number_columns = len(
			labels)
		if number_columns > 5:
			if number_columns % 2 == 0:
				number_columns = number_columns // 2
			else:
				number_columns = 4
		s_collisions = r"Number Total Collisions: ${:,}$".format(
			estimator.simulation_results["number collisions"])
		s_mass1 = r"$m_1 = {:,.0f}$ kg".format(
			estimator.simulation_parameters["m1"])
		s_mass2 = r"$m_2 = {:,.0f}$ kg".format(
			estimator.simulation_parameters["m2"])
		leg_title = "{}\n{}, {}".format(
			s_collisions,
			s_mass1,
			s_mass2)
		leg = self.visual_settings.get_legend(
			fig=fig,
			ax=ax,
			handles=handles,
			labels=labels,
			number_columns=number_columns,
			title=leg_title,
			)
		return fig, ax, leg

class EstimatorKinematicsViewerConfiguration(BaseEstimatorKinematicsViewerConfiguration):

	def __init__(self):
		super().__init__()

	def view_velocities_against_time(self, estimator, figsize=None, is_save=False):
		number_collisions = int(
			estimator.simulation_results["number collisions"])
		t = np.arange(
			number_collisions + 1)
		v1 = estimator.simulation_results["v1"]
		v2 = estimator.simulation_results["v2"]
		fig, ax = plt.subplots(
			figsize=figsize)
		ax = self.plot_velocities_against_time(
			ax=ax,
			t=t,
			v1=v1,
			v2=v2)
		ax = self.autoformat_plot(
			ax=ax,
			estimator=estimator,
			t=t,
			v1=v1,
			v2=v2)
		fig, ax, leg = self.autoformat_legend(
			fig=fig,
			ax=ax,
			estimator=estimator)
		save_name = "velocity_vs_time" if is_save else None
		self.visual_settings.display_image(
			fig=fig,
			save_name=save_name,
			space_replacement="_")





##