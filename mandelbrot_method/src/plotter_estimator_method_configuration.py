from plotter_base_configuration import BasePlotterConfiguration
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize, LogNorm
from matplotlib.animation import FuncAnimation


class BasestEstimatorMethodViewerConfiguration(BasePlotterConfiguration):

	def __init__(self):
		super().__init__()
		self._inverse_magnification_scale = None
		self._zoom_factor = None

	@property
	def inverse_magnification_scale(self):
		return self._inverse_magnification_scale
	
	@property
	def zoom_factor(self):
		return self._zoom_factor

	def initialize_zoom_parameters(self, zoom_factor):
		inverse_magnification_scale = 1.0
		if zoom_factor is None:
			zoom_factor = 0.95
		else:
			if not isinstance(zoom_factor, (int, float)):
				raise ValueError("invalid type(zoom_factor): {}".format(type(zoom_factor)))
			if (9 >= zoom_factor) or (zoom_factor > 1):
				raise ValueError("invalid zoom_factor: {}".format(zoom_factor))
		self._inverse_magnification_scale = inverse_magnification_scale
		self._zoom_factor = zoom_factor

	def update_magnification_scale_by_zoom(self):
		self._inverse_magnification_scale *= float(
			self.zoom_factor)

	@staticmethod
	def get_initial_axis_limits_and_extent():
		x_min = -2
		x_max = 1
		y_min = -1.5
		y_max = 1.5
		xlim = (
			x_min,
			x_max,
			)
		ylim = (
			y_min,
			y_max,
			)
		extent = [
			x_min,
			x_max,
			y_min,
			y_max,
			]
		return xlim, ylim, extent

class BaseEstimatorMethodViewerConfiguration(BasestEstimatorMethodViewerConfiguration):

	def __init__(self):
		super().__init__()

	@staticmethod
	def get_frame_parameters(fps, number_frames):
		if number_frames is None:
			number_frames = 180
		else:
			if not isinstance(number_frames, int):
				raise ValueError("invalid type(number_frames): {}".format(type(number_frames)))
			if number_frames < 1:
				raise ValueError("invalid number_frames: {}".format(number_frames))
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
	def get_color_parameters(mat, cmap, constant_color, is_log_color=False):
		if cmap is None:
			cmap = "inferno"
		if constant_color is None:
			constant_color = "gray"
		elif not isinstance(constant_color, str):
			raise ValueError("invalid type(constant_color): {}".format(type(constant_color)))
		if is_log_color:
			vmin = 0.1
			maximum_value = np.max(
				mat)
			log_base = int(
				10)
			# vmax = np.ceil(maximum_value / log_base) * log_base ## round up to nearest factor of 10
			vmax = 10 ** np.ceil(
			np.log10(
			maximum_value)) ## round up to nearest value 10^n
			norm = LogNorm(
				vmin=vmin,
				vmax=vmax)
		else:
			vmin = 0
			vmax = np.max(
				mat)
			norm = Normalize(
				vmin=vmin,
				vmax=vmax)
		return cmap, norm, constant_color

	@staticmethod
	def get_resolution(resolution):
		if resolution is None:
			resolution = 360
		else:
			if not isinstance(resolution, (int, np.int64)):
				raise ValueError("invalid type(resolution): {}".format(type(resolution)))
			if resolution <= 0:
				raise ValueError("invalid resolution: {}".format(resolution))
		return resolution

class BaseEstimatorMethodPlotterConfiguration(BaseEstimatorMethodViewerConfiguration):

	def __init__(self):
		super().__init__()

	@staticmethod
	def plot_mandelbrot_set(ax, mat, cmap, norm, extent):
		im = ax.imshow(
			mat,
			cmap=cmap,
			extent=extent,
			origin="lower",
			norm=norm,
			)
		return ax, im

	def plot_selected_constant(self, ax, constant, constant_color, is_show_constant, is_animated):
		x = constant.real
		y = constant.imag
		label = r"$c = {:,.4} + {:,.4}(i)$".format(
			float(x),
			float(y),
			)
		if is_animated:
			label = "zoom towards {}".format(
				label)
		if is_show_constant:			
			handle_by_scatter = ax.scatter(
				[x],
				[y],
				color=constant_color,
				marker="*",
				label=label,
				)
		else:
			if not is_animated:
				label = " " ## legend requires label and legend corrects spacing of text below ax
			handle_by_scatter = self.visual_settings.get_empty_scatter_handle(
				ax=ax,
				label=label)
		return ax, handle_by_scatter

	def plot_approximation_text(self, ax, estimator):
		x = 0.5
		y = -0.125
		number_digits = estimator.root_parameters["number digits"]
		inner_label = r"\frac{1}{10}"
		s = r"$\pi \approx (\text{{number_iterations}}) \times ({})^{{{}}} = {:,.{}f}$".format(
		    inner_label, 
		    number_digits,
		    estimator.value_by_approximation,
		    number_digits)
		handle_by_approximation_text = ax.text(
			x,
			y,
			s,
			fontsize=self.visual_settings.text_size,
			color="black",
			horizontalalignment="center",
			verticalalignment="center",
			transform=ax.transAxes)
		return ax, handle_by_approximation_text

	def plot_frame_number(self, ax, is_show_constant):
		x = 0.5
		if is_show_constant:
			y = -0.15
		else:
			y = -0.115
		s = ""
		handle_by_frame_text = ax.text(
			x,
			y,
			s,
			fontsize=self.visual_settings.text_size,
			color="black",
			horizontalalignment="center",
			verticalalignment="center",
			transform=ax.transAxes)
		return ax, handle_by_frame_text

	def autoformat_plot(self, ax, estimator, xlim, ylim):
		xlabel = r"$Re(z)$"
		ylabel = r"$Im(z)$"
		title = "{}".format(
			estimator.method_name)
		x_major_fmt = r"${:,.4}$"
		y_major_fmt = r"${:,.4}$"
		ax = self.visual_settings.autoformat_axis_labels(
			ax=ax,
			xlabel=xlabel,
			ylabel=ylabel,
			title=title,
			)
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
			x_major_fmt=x_major_fmt,
			y_major_fmt=y_major_fmt,
			x_major_ticklabels=True,
			x_minor_ticklabels=False,
			y_major_ticklabels=True,
			y_minor_ticklabels=False)
		ax = self.visual_settings.autoformat_grid(
			ax=ax,
			grid_color="gray",
			)
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

	def autoformat_color_bar(self, fig, ax, im):
		cbar_title = "Number of Iterations"
		cbar = self.visual_settings.get_color_bar(
			fig=fig,
			ax=ax,
			handle=im,
			title=cbar_title,
			shrink=0.76,
			pad=0.2,
			)
		return fig, ax, im, cbar

class EstimatorMethodViewerConfiguration(BaseEstimatorMethodPlotterConfiguration):

	def __init__(self):
		super().__init__()

	def view_mandelbrot_set(self, estimator, fps=None, number_frames=None, zoom_factor=None, resolution=None, constant=None, number_maximum_iterations=None, cmap=None, constant_color=None, is_show_constant=False, is_log_color=False, figsize=None, is_save=False, is_animated=False, extension=None):

		def update_frame(index_at_frame, ax, estimator, anim_handles, resolution, constant, number_maximum_iterations):
			[im, handle_by_frame_text] = anim_handles
			handle_by_frame_text.set_text(
				r"frame ${:,}$".format(
					index_at_frame),
				)
			c_real = constant.real ## x
			c_imag = constant.imag ## y
			self.update_magnification_scale_by_zoom()
			extent = im.get_extent()
			half_extent_x = (extent[1] - extent[0]) / 2
			half_extent_y = (extent[3] - extent[2]) / 2
			if (self.inverse_magnification_scale < 0.5 * half_extent_x): # or (self.inverse_magnification_scale < 0.5 * half_extent_y):
				new_half_extent_x = self.inverse_magnification_scale * 1.5
				new_half_extent_y = new_half_extent_x
				x_min = c_real - new_half_extent_x
				x_max = c_real + new_half_extent_x
				y_min = c_imag - new_half_extent_y
				y_max = c_imag + new_half_extent_y
				xlim = [
					x_min,
					x_max,
					]
				ylim = [
					y_min,
					y_max,
					]
				new_extent = [
					*xlim,
					*ylim,
					]
				matrix_by_number_iterations, matrix_by_root_value = estimator.get_matrices_by_root_value_and_number_iterations(
					xlim=xlim,
					ylim=ylim,
					resolution=resolution,
					number_maximum_iterations=number_maximum_iterations)
				im.set_data(
					matrix_by_number_iterations)
				im.set_extent(
					new_extent)
				# number_decimals = min([
				# 	abs(np.log10(x_max - x_min)),
				# 	abs(np.log10(y_max - y_min)),
				# 	])
				# fmt = ":,.{}".format(
				# 	number_decimals + 1)
				# ax.xaxis.set_major_formatter(
				# 	ticker.FormatStrFormatter(
				# 		fmt))
				# ax.yaxis.set_major_formatter(
				# 	ticker.FormatStrFormatter(
				# 		fmt))
			new_xlim = (
				c_real - self.inverse_magnification_scale,
				c_real + self.inverse_magnification_scale)
			new_ylim = (
				c_imag - self.inverse_magnification_scale,
				c_imag + self.inverse_magnification_scale)
			ax.set_xlim(
				new_xlim)
			ax.set_ylim(
				new_ylim)
			return [im, handle_by_frame_text]

		resolution = self.get_resolution(
			resolution=resolution)
		if constant is None:
			constant = estimator.root_parameters["constant"]
		elif not isinstance(constant, complex):
			raise ValueError("invalid type(constant): {}".format(type(constant)))
		number_maximum_iterations = estimator.get_number_maximum_iterations(
			number_maximum_iterations=number_maximum_iterations)
		xlim, ylim, extent = self.get_initial_axis_limits_and_extent()
		matrix_by_number_iterations, matrix_by_root_value = estimator.get_matrices_by_root_value_and_number_iterations(
			xlim=xlim,
			ylim=ylim,
			resolution=resolution,
			number_maximum_iterations=number_maximum_iterations)
		cmap, norm, constant_color = self.get_color_parameters(
			mat=matrix_by_number_iterations,
			cmap=cmap,
			constant_color=constant_color,
			is_log_color=is_log_color)
		fig, ax = plt.subplots(
			figsize=figsize)
		ax.set_aspect(
			"equal")
		ax, im = self.plot_mandelbrot_set(
			ax=ax,
			mat=matrix_by_number_iterations,
			cmap=cmap,
			norm=norm,
			extent=extent)
		ax, handle_by_scatter = self.plot_selected_constant(
			ax=ax,
			constant=constant,
			constant_color=constant_color,
			is_show_constant=is_show_constant,
			is_animated=is_animated)
		if (is_show_constant) and (constant == estimator.root_parameters["constant"]):
			ax, handle_by_approximation_text = self.plot_approximation_text(
				ax=ax,
				estimator=estimator)			
		ax = self.autoformat_plot(
			ax=ax,
			estimator=estimator,
			xlim=xlim,
			ylim=ylim)
		fig, ax, leg = self.autoformat_legend(
			fig=fig,
			ax=ax)
		fig, ax, im, cbar = self.autoformat_color_bar(
			fig=fig,
			ax=ax,
			im=im)
		if is_save:
			save_name = "mandelbrot_set"
			if is_show_constant:
				save_name += "-wConstant"
			if is_log_color:
				save_name += "-wLogColor"
		else:
			save_name = None
		if is_animated:
			ax, handle_by_frame_text = self.plot_frame_number(
				ax=ax,
				is_show_constant=is_show_constant)
			anim_handles = [
				im,
				handle_by_frame_text]
			self.initialize_zoom_parameters(
				zoom_factor=zoom_factor)
			number_frames, frames, fps = self.get_frame_parameters(
				fps=fps,
				number_frames=number_frames)
			fargs = (
				ax,
				estimator,
				anim_handles,
				resolution,
				constant,
				number_maximum_iterations,
				)
			anim = FuncAnimation(
				fig,
				update_frame,
				frames=frames,
				blit=False,
				interval=100,
				fargs=fargs)
			self.visual_settings.display_animation(
				anim,
				fps=fps,
				save_name=save_name,
				space_replacement="_",
				extension=extension)
		else:
			self.visual_settings.display_image(
				fig,
				save_name=save_name,
				space_replacement="_",
				extension=extension)

##