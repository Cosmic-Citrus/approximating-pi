from plotter_base_configuration import BasePlotterConfiguration
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


class BaseEstimatorMethodViewerConfiguration(BasePlotterConfiguration):

	def __init__(self):
		super().__init__()

	@staticmethod
	def get_geometry():
		radius = 1 ## unit circle
		number_polygon_sides = 6 ## hexagon
		number_side_doublings = 5 ## 6 (0) --> 12 (1) --> 24 (2) --> 48 (3) --> 96 (4)
		return radius, number_polygon_sides, number_side_doublings

	@staticmethod
	def get_frame_parameters(fps, number_frames_per_polygon_sides, number_side_doublings):
		if fps is None:
			fps = 12
		else:
			if not isinstance(fps, int):
				raise ValueError("invalid type(fps): {}".format(type(fps)))
			if fps <= 0:
				raise ValueError("invalid fps: {}".format(fps))
		if number_frames_per_polygon_sides is None:
			number_frames_per_polygon_sides = 60
		else:
			if not isinstance(number_frames_per_polygon_sides, int):
				raise ValueError("invalid type(number_frames_per_polygon_sides): {}".format(type(number_frames_per_polygon_sides)))
			if number_frames_per_polygon_sides <= 0:
				raise ValueError("invalid number_frames_per_polygon_sides: {}".format(number_frames_per_polygon_sides))
			if number_frames_per_polygon_sides % 2 != 0:
				raise ValueError("invalid number_frames_per_polygon_sides: {}".format(number_frames_per_polygon_sides))
		number_frames = int(
			number_frames_per_polygon_sides * (number_side_doublings + 1))
		frames = range(
			number_frames)
		return number_frames, number_frames_per_polygon_sides, frames, fps

	@staticmethod
	def get_color_parameters(color_circle=None, color_inner_polygon=None, color_outer_polygon=None, color_triangle=None, color_bisector=None):
		if color_circle is None:
			color_circle = "gray"
		elif not isinstance(color_circle, str):
			raise ValueError("invalid type(color_circle): {}".format(type(color_circle)))
		if color_inner_polygon is None:
			color_inner_polygon = "steelblue"
		elif not isinstance(color_inner_polygon, str):
			raise ValueError("invalid type(color_inner_polygon): {}".format(type(color_inner_polygon)))
		if color_outer_polygon is None:
			color_outer_polygon = "darkorange"
		elif not isinstance(color_outer_polygon, str):
			raise ValueError("invalid type(color_outer_polygon): {}".format(type(color_outer_polygon)))
		if color_triangle is None:
			color_triangle = "crimson"
		elif not isinstance(color_triangle, str):
			raise ValueError("invalid type(color_triangle): {}".format(type(color_triangle)))
		if color_bisector is None:
			color_bisector = "black"
		elif not isinstance(color_bisector, str):
			raise ValueError("invalid type(color_bisector): {}".format(type(color_bisector)))
		return color_circle, color_inner_polygon, color_outer_polygon, color_triangle, color_bisector

	@staticmethod
	def get_linestyle_parameters():
		linestyle_circle = "-"
		linestyle_inner_polygon = "-"
		linestyle_outer_polygon = "-"
		linestyle_triangles = "--"
		linestyle_triangle = "-"
		linestyle_bisector = ":"
		return linestyle_circle, linestyle_inner_polygon, linestyle_outer_polygon, linestyle_triangles, linestyle_triangle, linestyle_bisector

	def autoformat_plot(self, fig, ax_left, ax_right, estimator, radius):
		for ax in (ax_left, ax_right):
			ax.set_aspect(
				"equal")
		extended_radius = 1.5 * radius
		left_axis_limits = tuple([
			-1 * extended_radius,
			extended_radius,
			])
		differential_radius = radius * (1.125 - 1)
		right_axis_limits = tuple([
			0 - differential_radius,
			radius + differential_radius,
			])
		left_xlabel = r"$X$"
		left_ylabel = r"$Y$"
		right_xlabel = r"$X$"
		right_ylabel = None
		for ax, xlabel, ylabel in zip((ax_left, ax_right), (left_xlabel, right_xlabel), (left_ylabel, right_ylabel)):
			ax = self.visual_settings.autoformat_axis_labels(
				ax=ax,
				xlabel=xlabel,
				ylabel=ylabel)
		ax_left = self.visual_settings.autoformat_axis_limits(
			ax=ax_left,
			xlim=left_axis_limits,
			ylim=left_axis_limits)
		ax_right = self.visual_settings.autoformat_axis_limits(
			ax=ax_right,
			xlim=right_axis_limits,
			ylim=right_axis_limits)
		for ax in (ax_left, ax_right):
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
				x_major_fmt="${:,.2}$",
				y_major_fmt="${:,.2}$",
				)
			ax = self.visual_settings.autoformat_grid(
				ax=ax,
				grid_color="gray",
				)
		fig.suptitle(
			estimator.method_name,
			fontsize=self.visual_settings.title_size)
		return fig, ax_left, ax_right

	@staticmethod
	def get_legend_handles(ax, radius, color_parameters, linestyle_parameters):
		## extract colors and linestyles
		color_circle, color_inner_polygon, color_outer_polygon, color_triangle, color_bisector = color_parameters
		linestyle_circle, linestyle_inner_polygon, linestyle_outer_polygon, linestyle_triangles, linestyle_triangle, linestyle_bisector = linestyle_parameters
		## make labels
		label_circle = "circle (radius $r={:,.4})$".format(
				float(
					radius))
		label_inner_polygon = "inner polygon"
		label_outer_polygon = "outer polygon"
		label_triangle = "triangle"
		label_bisector = "angle bisector"
		## get handles
		handle_by_circle_marker = ax.scatter(
			list(),
			list(),
			facecolor="none",
			edgecolor=color_circle,
			label=label_circle,
			marker="o")
		handle_by_inner_polygon, = ax.plot(
			list(),
			list(),
			color=color_inner_polygon,
			label=label_inner_polygon,
			linestyle=linestyle_inner_polygon)
		handle_by_outer_polygon, = ax.plot(
			list(),
			list(),
			color=color_outer_polygon,
			label=label_outer_polygon,
			linestyle=linestyle_outer_polygon)
		handle_by_triangle, = ax.plot(
			list(),
			list(),
			color=color_triangle,
			label=label_triangle,
			linestyle=linestyle_triangle)
		handle_by_angle_bisector, = ax.plot(
			list(),
			list(),
			color=color_bisector,
			label=label_bisector,
			linestyle=linestyle_bisector)
		handles = [
			handle_by_circle_marker,
			handle_by_inner_polygon,
			handle_by_outer_polygon,
			handle_by_triangle,
			handle_by_angle_bisector,
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
	def plot_circle(ax, radius, color_circle):
		handle_by_circle = plt.Circle(
			(0, 0),
			radius,
			color=color_circle,
			alpha=0.8,
			fill=False,
			lw=0.5,
			)
		ax.add_artist(
			handle_by_circle)
		return ax, handle_by_circle

	def plot_formulas(self, ax, color_bisector):
		s_height_bisector_inside_triangle = r"height of bisector inside triangle: $h = \sqrt{r^{2} - (\frac{s_{n}}{2}})^2$" + "\n" r"where $s_{n}$ is side-length of inscribed n-sided polygon"
		s_height_bisector_outside_triangle = r"length of bisector between inner triangle and circle: $l = r - h$"
		s_next_polygon_side_length = r"hypotenuse of right triangle with base $\frac{s_{n}}{2}$ and height $l$: $s_{2n} = \sqrt{(\frac{s_{n}}{2})^2 + l^2}$"
		s = "{}\n\n{}\n\n{}".format(
			s_height_bisector_inside_triangle,
			s_height_bisector_outside_triangle,
			s_next_polygon_side_length)
		handle_by_text_bisector_height_inside_triangle = ax.text(
			0.5,
			-0.125,
			s,
			fontsize=self.visual_settings.text_size,
			color=color_bisector,
			horizontalalignment="center",
			verticalalignment="top",
			transform=ax.transAxes)
		return ax

	def get_anim_handles(self, ax_left, ax_right, color_parameters, linestyle_parameters):
		color_circle, color_inner_polygon, color_outer_polygon, color_triangle, color_bisector = color_parameters
		linestyle_circle, linestyle_inner_polygon, linestyle_outer_polygon, linestyle_triangles, linestyle_triangle, linestyle_bisector = linestyle_parameters
		handle_by_previous_inner_polygon, = ax_left.plot(
			list(),
			list(),
			color=color_inner_polygon,
			# alpha=0.2,
			linestyle=linestyle_inner_polygon)
		handle_by_current_inner_polygon, = ax_left.plot(
			list(),
			list(),
			color=color_inner_polygon,
			# alpha=0.2,
			linestyle=linestyle_inner_polygon)
		handle_by_previous_outer_polygon, = ax_left.plot(
			list(),
			list(),
			color=color_outer_polygon,
			# alpha=0.8,
			linestyle=linestyle_outer_polygon)
		handle_by_current_outer_polygon, = ax_left.plot(
			list(),
			list(),
			color=color_outer_polygon,
			# alpha=0.8,
			linestyle=linestyle_outer_polygon)
		handle_by_left_triangles, = ax_left.plot(
			list(),
			list(),
			color=color_triangle,
			# alpha=0.2,
			linestyle=linestyle_triangles)
		handle_by_left_triangle, = ax_left.plot(
			list(),
			list(),
			color=color_triangle,
			# alpha=0.8,
			linestyle=linestyle_triangle)
		handle_by_next_right_triangle, = ax_right.plot(
			list(),
			list(),
			color=color_triangle,
			# alpha=0.8,
			linestyle=linestyle_triangle)
		handle_by_current_right_triangle, = ax_right.plot(
			list(),
			list(),
			color=color_triangle,
			# alpha=0.8,
			linestyle=linestyle_triangle)
		handle_by_bisector, = ax_right.plot(
			list(),
			list(),
			color=color_bisector,
			# alpha=0.8,
			linestyle=linestyle_bisector)
		handle_by_text_iterations = ax_left.text(
			0.5,
			-0.125,
			"",
			fontsize=self.visual_settings.text_size,
			horizontalalignment="center",
			verticalalignment="top",
			transform=ax_left.transAxes)
		handle_by_text_polygon_sides = ax_left.text(
			0.5,
			-0.175,
			"",
			fontsize=self.visual_settings.text_size,
			horizontalalignment="center",
			verticalalignment="top",
			transform=ax_left.transAxes)
		anim_handles = [
			handle_by_previous_inner_polygon,
			handle_by_current_inner_polygon,
			handle_by_previous_outer_polygon,
			handle_by_current_outer_polygon,
			handle_by_left_triangles,
			handle_by_left_triangle,
			handle_by_next_right_triangle,
			handle_by_current_right_triangle,
			handle_by_bisector,
			handle_by_text_iterations,
			handle_by_text_polygon_sides,
			]
		return ax_left, ax_right, anim_handles

	@staticmethod
	def get_xy_vertices_inner_polygon(number_polygon_sides, radius):
		theta = np.linspace(
			0,
			2 * np.pi,
			number_polygon_sides + 1)
		x = radius * np.cos(theta)
		y = radius * np.sin(theta)
		return x, y

	@staticmethod
	def get_xy_vertices_outer_polygon(number_polygon_sides, radius):
		theta = np.linspace(
			0,
			2 * np.pi,
			number_polygon_sides + 1)
		r_out = radius / np.cos(np.pi / number_polygon_sides)
		phi = theta + np.pi / number_polygon_sides
		x = r_out * np.cos(phi)
		y = r_out * np.sin(phi)
		return x, y

	@staticmethod
	def get_xy_vertices_triangle(xy_inner_polygon, index_at_root):
		origin = (
			0,
			0,
			)
		x, y = xy_inner_polygon
		# x_AB = (
		# 	vertex_A[0],
		# 	vertex_B[0],
		# 	)
		# y_AB = (
		# 	vertex_A[1],
		# 	vertex_B[1],
		# 	)
		# x_BC = (
		# 	vertex_B[0],
		# 	vertex_C[0],
		# 	)
		# y_BC = (
		# 	vertex_B[1],
		# 	vertex_C[1],
		# 	)
		# x_AC = (
		# 	vertex_A[0],
		# 	vertex_C[0],
		# 	)
		# y_AC = (
		# 	vertex_A[1],
		# 	vertex_C[1],
		# 	)
		## (A, B, origin, A, None)
		## (A+B, B+origin, origin+A, lift pen)
		xx = [
			x[index_at_root],
			x[index_at_root + 1],
			origin[0],
			x[index_at_root],
			None, 
			]
		yy = [
			y[index_at_root],
			y[index_at_root + 1],
			origin[1],
			y[index_at_root],
			None, 
			]
		return xx, yy

	def get_xy_vertices_triangles(self, xy_inner_polygon, number_polygon_sides):
		xx, yy = list(), list()
		for index_at_root in range(number_polygon_sides):
			x, y = self.get_xy_vertices_triangle(
				xy_inner_polygon=xy_inner_polygon,
				index_at_root=index_at_root)
			xx.extend(
				x)
			yy.extend(
				y)
		return xx, yy

	@staticmethod
	def get_bisector_endpoints(xy_outer_polygon, index_at_root):
		origin = (
			0,
			0)
		x, y = xy_outer_polygon
		xx = [
			origin[0],
			x[index_at_root],
			]
		yy = [
			origin[1],
			y[index_at_root],
			]
		return xx, yy

class EstimatorMethodViewerConfiguration(BaseEstimatorMethodViewerConfiguration):

	def __init__(self):
		super().__init__()

	def view_approximation_method(self, estimator, fps=None, number_frames_per_polygon_sides=None, color_circle=None, color_inner_polygon=None, color_outer_polygon=None, color_triangle=None, color_bisector=None, figsize=None, is_save=False, extension=None):

		def update_frame(index_at_frame, anim_handles, number_frames_per_polygon_sides, number_initial_polygon_sides, radius):
			## get number sides and remainder frames
			number_current_elapsed_side_doublings, number_current_remainder_frames = divmod(
				index_at_frame,
				number_frames_per_polygon_sides,
				)
			number_current_polygon_sides = int(
				number_initial_polygon_sides * (2 ** number_current_elapsed_side_doublings))
			number_next_polygon_sides = int(
				2 * number_current_polygon_sides)
			## get xy-coordinates
			xy_current_inner_polygon = self.get_xy_vertices_inner_polygon(
				number_polygon_sides=number_current_polygon_sides,
				radius=radius)
			x_current_inner_polygon, y_current_inner_polygon = xy_current_inner_polygon
			xy_current_outer_polygon = self.get_xy_vertices_outer_polygon(
				number_polygon_sides=number_current_polygon_sides,
				radius=radius)
			x_current_outer_polygon, y_current_outer_polygon = xy_current_outer_polygon
			x_left_triangles, y_left_triangles  = self.get_xy_vertices_triangles(
				xy_inner_polygon=xy_current_inner_polygon,
				number_polygon_sides=number_current_polygon_sides)
			x_left_triangle, y_left_triangle  = self.get_xy_vertices_triangle(
				xy_inner_polygon=xy_current_inner_polygon,
				index_at_root=0)
			xy_next_inner_polygon = self.get_xy_vertices_inner_polygon(
				number_polygon_sides=number_next_polygon_sides,
				radius=radius)
			x_next_right_triangle, y_next_right_triangle  = self.get_xy_vertices_triangle(
				xy_inner_polygon=xy_next_inner_polygon,
				index_at_root=0)
			x_bisector, y_bisector = self.get_bisector_endpoints(
				xy_outer_polygon=xy_current_outer_polygon,
				index_at_root=0)
			## get handles
			[handle_by_previous_inner_polygon, handle_by_current_inner_polygon, handle_by_previous_outer_polygon, handle_by_current_outer_polygon, handle_by_left_triangles, handle_by_left_triangle, handle_by_next_right_triangle, handle_by_current_right_triangle, handle_by_bisector, handle_by_text_iterations, handle_by_text_polygon_sides] = anim_handles
			## update coordinates
			handle_by_current_inner_polygon.set_data(
				x_current_inner_polygon,
				y_current_inner_polygon)
			handle_by_current_outer_polygon.set_data(
				x_current_outer_polygon,
				y_current_outer_polygon)
			handle_by_left_triangles.set_data(
				x_left_triangles,
				y_left_triangles)
			handle_by_left_triangle.set_data(
				x_left_triangle,
				y_left_triangle)
			handle_by_next_right_triangle.set_data(
				x_next_right_triangle,
				y_next_right_triangle)
			handle_by_current_right_triangle.set_data(
				x_left_triangle,
				y_left_triangle)
			handle_by_bisector.set_data(
				x_bisector,
				y_bisector)
			## update alpha transparency
			handle_by_current_inner_polygon.set_alpha(
				0.825)
			handle_by_current_outer_polygon.set_alpha(
				0.825)
			handle_by_left_triangles.set_alpha(
				0.175)
			handle_by_left_triangle.set_alpha(
				0.8)
			if number_current_remainder_frames < number_frames_per_polygon_sides / 2:
				unclipped_alpha_current_right_triangle = 1
				unclipped_alpha_next_right_triangle = 0
				unclipped_alpha_bisector = number_current_remainder_frames / (number_frames_per_polygon_sides / 2)
			else:
				unclipped_alpha_current_right_triangle = 1 - (number_current_remainder_frames - number_frames_per_polygon_sides / 2) / (number_frames_per_polygon_sides / 2)
				unclipped_alpha_next_right_triangle = (number_current_remainder_frames - number_frames_per_polygon_sides / 2) / (number_frames_per_polygon_sides / 2)
				unclipped_alpha_bisector = 1
			alpha_current_right_triangle = max(
				0,
				min(
					1,
					unclipped_alpha_current_right_triangle),
				)
			alpha_next_right_triangle = max(
				0,
				min(
					1,
					unclipped_alpha_next_right_triangle),
				)
			alpha_bisector = max(
				0,
				min(
					1,
					unclipped_alpha_bisector),
				)
			handle_by_current_right_triangle.set_alpha(
				alpha_current_right_triangle)
			handle_by_next_right_triangle.set_alpha(
				alpha_next_right_triangle)
			handle_by_bisector.set_alpha(
				alpha_bisector)
			## update text
			s_text_iterations = r"number of iterations: ${:,}$".format(
				number_current_elapsed_side_doublings)
			s_text_polygon_sides = "number of inner/outer polygon sides\n" + r"$6 \times 2^{:,} = {:,}$".format(
				number_current_elapsed_side_doublings,
				number_current_polygon_sides)
			handle_by_text_iterations.set_text(
				s_text_iterations)
			handle_by_text_polygon_sides.set_text(
				s_text_polygon_sides)
			## update previous polygon
			if index_at_frame >= number_frames_per_polygon_sides:
				## get number sides and remainder frames
				number_previous_elapsed_side_doublings, number_previous_remainder_frames = divmod(
					index_at_frame - number_frames_per_polygon_sides,
					number_frames_per_polygon_sides,
					)
				number_previous_polygon_sides = int(
					number_initial_polygon_sides * (2 ** number_previous_elapsed_side_doublings))
				## get xy-coordinates
				x_previous_inner_polygon, y_previous_inner_polygon = self.get_xy_vertices_inner_polygon(
					number_polygon_sides=number_previous_polygon_sides,
					radius=radius)
				x_previous_outer_polygon, y_previous_outer_polygon = self.get_xy_vertices_outer_polygon(
					number_polygon_sides=number_previous_polygon_sides,
					radius=radius)
				## update coordinates
				handle_by_previous_inner_polygon.set_data(
					x_previous_inner_polygon,
					y_previous_inner_polygon)
				handle_by_previous_outer_polygon.set_data(
					x_previous_outer_polygon,
					y_previous_outer_polygon)
				## update alpha transparency
				handle_by_previous_inner_polygon.set_alpha(
					0.175)
				handle_by_previous_outer_polygon.set_alpha(
					0.175)
			return [handle_by_previous_inner_polygon, handle_by_current_inner_polygon, handle_by_previous_outer_polygon, handle_by_current_outer_polygon, handle_by_left_triangles, handle_by_left_triangle, handle_by_next_right_triangle, handle_by_current_right_triangle, handle_by_bisector, handle_by_text_iterations, handle_by_text_polygon_sides]

		## get pre-requisite geometry
		radius, number_polygon_sides, number_side_doublings = self.get_geometry()
		## get frames and modulo
		number_frames, number_frames_per_polygon_sides, frames, fps = self.get_frame_parameters(
			fps=fps,
			number_frames_per_polygon_sides=number_frames_per_polygon_sides,
			number_side_doublings=number_side_doublings)
		## get color parameters
		color_parameters = self.get_color_parameters(
			color_circle=color_circle,
			color_inner_polygon=color_inner_polygon,
			color_outer_polygon=color_outer_polygon,
			color_triangle=color_triangle,
			color_bisector=color_bisector)
		color_circle, color_inner_polygon, color_outer_polygon, color_triangle, color_bisector = color_parameters
		## get linestyle parameters
		linestyle_parameters = self.get_linestyle_parameters()
		linestyle_circle, linestyle_inner_polygon, linestyle_outer_polygon, linestyle_triangles, linestyle_triangle, linestyle_bisector = linestyle_parameters
		## initialize plot
		fig, (ax_left, ax_right) = plt.subplots(
			nrows=1,
			ncols=2,
			figsize=figsize)
		## autoformat subplots
		fig, ax_left, ax_right = self.autoformat_plot(
			fig=fig,
			ax_left=ax_left,
			ax_right=ax_right,
			estimator=estimator,
			radius=radius)
		## initialize legend
		ax_left, legend_handles = self.get_legend_handles(
			ax=ax_left,
			radius=radius,
			color_parameters=color_parameters,
			linestyle_parameters=linestyle_parameters)
		fig, ax_left, leg = self.autoformat_legend(
			fig=fig,
			ax=ax_left,
			handles=legend_handles)
		## plot unchanging circle in both subplots
		ax_left, handle_by_left_circle = self.plot_circle(
			ax=ax_left,
			radius=radius,
			color_circle=color_circle)
		ax_right, handle_by_right_circle = self.plot_circle(
			ax=ax_right,
			radius=radius,
			color_circle=color_circle)
		## plot unchanging formulas below right subplot
		ax_right = self.plot_formulas(
			ax=ax_right,
			color_bisector=color_bisector)
		## initialize animation
		ax_left, ax_right, anim_handles = self.get_anim_handles(
			ax_left=ax_left,
			ax_right=ax_right,
			color_parameters=color_parameters,
			linestyle_parameters=linestyle_parameters)
		fargs = (
			anim_handles,
			number_frames_per_polygon_sides,
			number_polygon_sides,
			radius)
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