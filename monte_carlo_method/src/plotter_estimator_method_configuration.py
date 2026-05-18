from plotter_base_configuration import BasePlotterConfiguration
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


class BaseEstimatorMethodViewerConfiguration(BasePlotterConfiguration):

	def __init__(self):
		super().__init__()

	@staticmethod
	def get_frame_parameters(estimator, fps):
		number_frames = int(
			estimator.number_trial_runs)
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
	def get_color_parameters(color_inside_circle, color_outside_circle, color_at_boundary, color_text):
		if color_inside_circle is None:
			color_inside_circle = "darkorange"
		elif not isinstance(color_inside_circle, str):
			raise ValueError("invalid type(color_inside_circle): {}".format(type(color_inside_circle)))
		if color_outside_circle is None:
			color_outside_circle = "forestgreen"
		elif not isinstance(color_outside_circle, str):
			raise ValueError("invalid type(color_outside_circle): {}".format(type(color_outside_circle)))
		if color_at_boundary is None:
			color_at_boundary = "black"
		elif not isinstance(color_at_boundary, str):
			raise ValueError("invalid type(color_at_boundary): {}".format(type(color_at_boundary)))
		if color_text is None:
			color_text = "black"
		elif not isinstance(color_text, str):
			raise ValueError("invalid type(color_text): {}".format(type(color_text)))
		return color_inside_circle, color_outside_circle, color_at_boundary, color_text

	def autoformat_plot(self, ax, estimator):
		ax.set_aspect(
			"equal")
		axis_limits = tuple([
			-1 * estimator.radius,
			estimator.radius,
			])
		xlabel = r"$X$"
		ylabel = r"$Y$"
		title = "{}".format(
			estimator.method_name)
		ax = self.visual_settings.autoformat_axis_labels(
			ax=ax,
			xlabel=xlabel,
			ylabel=ylabel,
			title=estimator.method_name,
			)
		ax = self.visual_settings.autoformat_axis_limits(
			ax=ax,
			xlim=axis_limits,
			ylim=axis_limits)
		ax = self.visual_settings.autoformat_axis_ticks_and_ticklabels(
			ax=ax,
			x_major_ticks=True,
			x_minor_ticks=True,
			y_major_ticks=True,
			y_minor_ticks=True,
			x_major_fmt="{:,.5f}",
			y_major_fmt="{:,.5f}",
			x_major_ticklabels=True,
			x_minor_ticklabels=False,
			y_major_ticklabels=True,
			y_minor_ticklabels=False)
		ax = self.visual_settings.autoformat_grid(
			ax=ax,
			grid_color="gray",
			)
		return ax

	@staticmethod
	def get_legend_handles(ax, estimator, color_parameters):
		color_inside_circle, color_outside_circle, color_at_boundary, color_text = color_parameters
		label_inside_circle = "Points inside of the circle"
		label_outside_circle = "Points outside of the circle"
		handle_by_inside_circle = ax.scatter(
			list(),
			list(),
			color=color_inside_circle,
			label=label_inside_circle,
			marker=".")
		handle_by_outside_circle = ax.scatter(
			list(),
			list(),
			color=color_outside_circle,
			label=label_outside_circle,
			marker=".")
		handles = [
			handle_by_inside_circle,
			handle_by_outside_circle,
			]
		return ax, handles

	def autoformat_legend(self, fig, ax, handles):
		labels = [
			handle.get_label()
				for handle in handles]
		number_columns = len(
			labels)
		if number_columns > 5:
			if number_columns % 2 == 0:
				number_columns = number_columns // 2
			else:
				number_columns = 4
		leg_title = ""
		leg = self.visual_settings.get_legend(
			fig=fig,
			ax=ax,
			handles=handles,
			labels=labels,
			number_columns=number_columns,
			title=leg_title,
			)
		return fig, ax, leg

	@staticmethod
	def plot_circle(ax, estimator, color_at_boundary):
		origin = (0, 0)
		circle_patch = plt.Circle(
			origin,
			estimator.radius,
			color=color_at_boundary,
			fill=False)
		ax.add_patch(
			circle_patch)
		return ax

	def get_anim_handles(self, ax, color_parameters):
		color_inside_circle, color_outside_circle, color_at_boundary, color_text = color_parameters
		handle_by_scatter = ax.scatter(
			list(),
			list(),
			marker=".",
			)
		x_left = 0.25
		x_right = 0.6
		x_middle = (x_left + x_right) / 2
		y_top = -0.125
		y_bottom = -0.15
		y_middle = (y_top + y_bottom) / 2
		handle_by_inside_text = ax.text(
			x_left,
			y_top,
			"",
			fontsize=self.visual_settings.text_size,
			color=color_inside_circle,
			horizontalalignment="right",
			verticalalignment="center",
			transform=ax.transAxes)
		handle_by_outside_text = ax.text(
			x_left,
			y_bottom,
			"",
			fontsize=self.visual_settings.text_size,
			color=color_outside_circle,
			horizontalalignment="right",
			verticalalignment="center",
			transform=ax.transAxes)
		handle_by_trial_text = ax.text(
			x_middle,
			y_middle,
			"",
			fontsize=self.visual_settings.text_size,
			color=color_text,
			horizontalalignment="left",
			verticalalignment="center",
			transform=ax.transAxes)
		handle_by_approximation_text = ax.text(
			x_right,
			y_middle,
			"",
			fontsize=self.visual_settings.text_size,
			color=color_text,
			horizontalalignment="left",
			verticalalignment="center",
			transform=ax.transAxes)
		anim_handles = [
			handle_by_scatter,
			handle_by_inside_text,
			handle_by_outside_text,
			handle_by_trial_text,
			handle_by_approximation_text,
			]
		return ax, anim_handles

class EstimatorMethodViewerConfiguration(BaseEstimatorMethodViewerConfiguration):

	def __init__(self):
		super().__init__()

	def view_approximation_method(self, estimator, fps=None, color_inside_circle=None, color_outside_circle=None, color_at_boundary=None, color_text=None, figsize=None, is_save=False, extension=None):

		def update_frame(index_at_frame, estimator, anim_handles, color_parameters):
			coordinates = estimator.trial_data["coordinates"][index_at_frame]
			(x, y) = coordinates.T
			is_points_inside_circle = estimator.trial_data["is inside circle"][index_at_frame]
			number_points_inside_circle = estimator.trial_data["number points inside circle"][index_at_frame]
			value_by_approximation = estimator.trial_data["approximation values"][index_at_frame]
			number_points_outside_circle = estimator.trial_data["number points outside circle"][index_at_frame]
			color_inside_circle, color_outside_circle, color_at_boundary, color_text = color_parameters
			facecolors = np.where(
				is_points_inside_circle,
				color_inside_circle,
				color_outside_circle)
			[handle_by_scatter, handle_by_inside_text, handle_by_outside_text, handle_by_trial_text, handle_by_approximation_text] = anim_handles
			handle_by_scatter.set_offsets(
				np.c_[x, y])
			handle_by_scatter.set_facecolors(
				facecolors)
			handle_by_inside_text.set_text(
				r"$N$(inside circle)" + r"$ = {:,}$".format(
					number_points_inside_circle))
			handle_by_outside_text.set_text(
				r"$N$(outside circle)" + r"$ = {:,}$".format(
					number_points_outside_circle))
			handle_by_trial_text.set_text(
				r"Trial {:,}".format(
					index_at_frame+1))
			s1 = r"$\frac{Area(circle)}{Area(square)} = \frac{\pi r^2}{l^2} = \frac{\pi (\frac{l}{2})^2}{l^2} = \frac{\pi}{4}$"
			s2 = r"$\pi \approx 4 \times \frac{N(inside circle)}{N(inside circle) + N(outside circle)}$" + r"$= {:,.4f}$".format(
					value_by_approximation)
			ss = "\t{}\n{}".format(
				s1,
				s2)
			handle_by_approximation_text.set_text(
				ss)
			return [handle_by_scatter, handle_by_inside_text, handle_by_outside_text, handle_by_trial_text, handle_by_approximation_text]

		if estimator.number_dimensions != 2:
			raise ValueError("estimator.number_dimensions={} is not compatible with this plotting method".format(estimator.number_dimensions))
		## get frames
		number_frames, frames, fps = self.get_frame_parameters(
			estimator=estimator,
			fps=fps)
		## get color parameters
		color_parameters = self.get_color_parameters(
			color_inside_circle=color_inside_circle,
			color_outside_circle=color_outside_circle,
			color_at_boundary=color_at_boundary,
			color_text=color_text)
		color_inside_circle, color_outside_circle, color_at_boundary, color_text = color_parameters
		## initialize plot
		fig, ax = plt.subplots(
			figsize=figsize)
		## autoformat plot
		ax = self.autoformat_plot(
			ax=ax,
			estimator=estimator)
		## initialize legend
		ax, legend_handles = self.get_legend_handles(
			ax=ax,
			estimator=estimator,
			color_parameters=color_parameters)
		fig, ax, leg = self.autoformat_legend(
			fig=fig,
			ax=ax,
			handles=legend_handles)
		## plot unchanging circle
		ax = self.plot_circle(
			ax=ax,
			estimator=estimator,
			color_at_boundary=color_at_boundary)
		## initialize animation
		ax, anim_handles = self.get_anim_handles(
			ax=ax,
			color_parameters=color_parameters)
		fargs = (
			estimator,
			anim_handles,
			color_parameters)
		anim = FuncAnimation(
			fig,
			update_frame,
			fargs=fargs,
			frames=frames,
			blit=True,
			interval=100,
			)
		## save or show
		save_name = "approximation_method" if is_save else None
		self.visual_settings.display_animation(
			anim,
			fps=fps,
			save_name=save_name,
			space_replacement="_",
			extension=extension)

##