from plotter_base_configuration import BasePlotterConfiguration
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


class BaseEstimatorPhaseSpaceViewerConfiguration(BasePlotterConfiguration):

	def __init__(self):
		super().__init__()

	@staticmethod
	def plot_constant_energy_level_curve(ax, r, energy_color="black"):
		label = r"$\frac{(p_1^\prime)^2}{2m_1} + \frac{(p_2^\prime)^2}{2m_2} \equiv constant$"
		circle = plt.Circle(
			(0, 0),
			radius=r,
			color=energy_color,
			fill=False,
			linestyle="--",
			alpha=0.6,
			label=label)
		ax.add_patch(
			circle)
		return ax

	@staticmethod
	def plot_phase_space_trajectory(ax, x, y, trajectory_color="steelblue"):
		label = "Phase-Space Trajectory"
		ax.plot(
			x,
			y,
			color=trajectory_color,
			alpha=0.8,
			marker="o",
			linestyle="-",
			label=label)
		return ax

	def autoformat_plot(self, ax, estimator, r):
		ax.set_aspect(
			"equal")
		xlabel = r"Scaled Canonical Momentum $p_1^\prime = \sqrt{m_1} v_1$"
		ylabel = r"Scaled Canonical Momentum $p_2^\prime = \sqrt{m_2} v_2$"
		ax = self.visual_settings.autoformat_axis_labels(
			ax=ax,
			xlabel=xlabel,
			ylabel=ylabel,
			title=estimator.method_name,
			)
		xlim = [
			-1.125 * r,
			1.125 * r,
			]
		ylim = [
			-1.125 * r,
			1.125 * r,
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
			x_major_fmt="{:,.2f}",
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

	def autoformat_legend(self, fig, ax, estimator, is_animated):
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
		leg_kwargs = dict()
		# if is_animated:
		# 	bbox_to_anchor = [
		# 		0,
		# 		-0.0175,
		# 		1,
		# 		1,
		# 		]
		# 	leg_kwargs = {
		# 		"bbox_to_anchor" : bbox_to_anchor,
		# 		"bbox_transform" : fig.transFigure,
		# 		}
		leg = self.visual_settings.get_legend(
			fig=fig,
			ax=ax,
			handles=handles,
			labels=labels,
			number_columns=number_columns,
			title=leg_title,
			**leg_kwargs,
			)
		return fig, ax, leg

	@staticmethod
	def get_frame_parameters(estimator, fps):
		number_frames = int(
			estimator.simulation_results["number collisions"])
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
	def get_animation_handles(ax, trajectory_color="mediumorchid", pre_collision_color="gray", m_wall_collision_color="crimson", m_m_collision_color="steelblue", leading_color="limegreen"):
		trajectory_label = "Elapsed Trajectory"
		pre_collision_label = "Initial State"
		m_wall_collision_label = r"Collision between $m_1$ and $m_2$"
		m_m_collision_label = r"Collision between $m_1$ and Wall"
		leading_label = "Running State"
		handle_by_trajectory, = ax.plot(
			list(),
			list(),
			color=trajectory_color,
			label=trajectory_label)
		handle_by_pre_collision = ax.scatter(
			list(),
			list(),
			color=pre_collision_color,
			marker="o",
			label=pre_collision_label)
		handle_by_m_wall_collision = ax.scatter(
			list(),
			list(),
			color=m_wall_collision_color,
			marker="o",
			label=m_wall_collision_label)
		handle_by_m_m_collision = ax.scatter(
			list(),
			list(),
			color=m_m_collision_color,
			marker="o",
			label=m_m_collision_label)
		handle_by_leading_collision, = ax.plot(
			list(),
			list(),
			color=leading_color,
			marker="o",
			label=leading_label)
		anim_handles = [
			handle_by_trajectory,
			handle_by_pre_collision,
			handle_by_m_wall_collision,
			handle_by_m_m_collision,
			handle_by_leading_collision,
			]
		return ax, anim_handles

	@staticmethod
	def get_xy_at_frame(index_at_frame, estimator, x, y):
		collision_status = estimator.simulation_results["collision status"]
		collision_mapping = estimator.simulation_results["collision mapping"]
		coordinates_by_none = list()
		coordinates_by_m1_wall_collision = list()
		coordinates_by_m1_m2_collision = list()
		for it in range(index_at_frame + 1):
			collision_status_at_it = collision_status[it]
			if collision_status_at_it == None:
				coordinates_by_none.append(
					(x[it], y[it]))
			elif collision_status_at_it == "m1-wall":
				coordinates_by_m1_wall_collision.append(
					(x[it], y[it]))
			elif collision_status_at_it == "m1-m2":
				coordinates_by_m1_m2_collision.append(
					(x[it], y[it]))
		return coordinates_by_none, coordinates_by_m1_wall_collision, coordinates_by_m1_m2_collision

class EstimatorPhaseSpaceViewerConfiguration(BaseEstimatorPhaseSpaceViewerConfiguration):

	def __init__(self):
		super().__init__()

	def view_phase_space(self, estimator, fps=None, figsize=None, is_save=False, is_animated=False, extension=None):

		def update_frame(index_at_frame, anim_handles, estimator, x, y):
			[handle_by_trajectory, handle_by_pre_collision, handle_by_m_wall_collision, handle_by_m_m_collision, handle_by_leading_collision] = anim_handles
			handle_by_trajectory.set_data(
				x[:index_at_frame+1],
				y[:index_at_frame+1],
				)
			coordinates_by_none, coordinates_by_m1_wall_collision, coordinates_by_m1_m2_collision = self.get_xy_at_frame(
				index_at_frame=index_at_frame,
				estimator=estimator,
				x=x,
				y=y)
			if coordinates_by_none:
				handle_by_pre_collision.set_offsets(
					coordinates_by_none)
			if coordinates_by_m1_wall_collision:
				handle_by_m_wall_collision.set_offsets(
					coordinates_by_m1_wall_collision)
			if coordinates_by_m1_m2_collision:
				handle_by_m_m_collision.set_offsets(
					coordinates_by_m1_m2_collision)
			handle_by_leading_collision.set_data(
				[x[index_at_frame]],
				[y[index_at_frame]])
			return [handle_by_trajectory, handle_by_pre_collision, handle_by_m_wall_collision, handle_by_m_m_collision, handle_by_leading_collision]

		m1 = estimator.simulation_parameters["m1"]
		m2 = estimator.simulation_parameters["m2"]
		v1 = estimator.simulation_results["v1"]
		v2 = estimator.simulation_results["v2"]
		v1i = estimator.simulation_parameters["v1"]
		v2i = estimator.simulation_parameters["v2"]
		x = np.sqrt(m1) * v1
		y = np.sqrt(m2) * v2
		r = np.sqrt(m1 * v1i ** 2 + m2 * v2i ** 2)
		save_name = "phase_space" if is_save else None
		fig, ax = plt.subplots(
			figsize=figsize)
		ax = self.plot_constant_energy_level_curve(
			ax=ax,
			r=r)
		if is_animated:
			ax = self.autoformat_plot(
				ax=ax,
				estimator=estimator,
				r=r)
			number_frames, frames, fps = self.get_frame_parameters(
				estimator=estimator,
				fps=fps)
			ax, anim_handles = self.get_animation_handles(
				ax=ax)
			fig, ax, leg = self.autoformat_legend(
				fig=fig,
				ax=ax,
				estimator=estimator,
				is_animated=is_animated,
				)
			fargs = (
				anim_handles,
				estimator,
				x,
				y)
			anim = FuncAnimation(
				fig,
				update_frame,
				fargs=fargs,
				frames=frames,
				blit=True,
				interval=100,
				)
			self.visual_settings.display_animation(
				anim,
				fps=fps,
				save_name=save_name,
				space_replacement="_",
				extension=extension)
		else:
			ax = self.plot_phase_space_trajectory(
				ax=ax,
				x=x,
				y=y)
			ax = self.autoformat_plot(
				ax=ax,
				estimator=estimator,
				r=r)
			fig, ax, leg = self.autoformat_legend(
				fig=fig,
				ax=ax,
				estimator=estimator,
				is_animated=is_animated,
				)
			self.visual_settings.display_image(
				fig=fig,
				save_name=save_name,
				space_replacement="_")

##