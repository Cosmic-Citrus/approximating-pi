

class BaseErrorConfiguration():

	def __init__(self):
		super().__init__()
		self._value_true = None
		self._value_estimate = None
		self._absolute_error = None
		self._relative_error = None
		self._relative_error_as_percent = None

	@property
	def value_true(self):
		return self._value_true
	
	@property
	def value_estimate(self):
		return self._value_estimate
	
	@property
	def absolute_error(self):
		return self._absolute_error
	
	@property
	def relative_error(self):
		return self._relative_error
	
	@property
	def relative_error_as_percent(self):
		return self._relative_error_as_percent
	
	def initialize_values_to_compare(self, value_true, value_estimate):
		if not isinstance(value_true, (int, float)):
			raise ValueError("invalid type(value_true): {}".format(type(value_true)))
		if not isinstance(value_estimate, (int, float)):
			raise ValueError("invalid type(value_estimate): {}".format(type(value_estimate)))
		self._value_true = value_true
		self._value_estimate = value_estimate

	def initialize_error_values(self):
		absolute_error = abs(
			self.value_true - self.value_estimate)
		relative_error = absolute_error / self.value_true
		relative_error_as_percent = relative_error * 100
		self._absolute_error = absolute_error
		self._relative_error = relative_error
		self._relative_error_as_percent = relative_error_as_percent

class ErrorConfiguration(BaseErrorConfiguration):

	def __init__(self):
		super().__init__()

	def __repr__(self):
		return f"ErrorConfiguration()"

	def __str__(self):
		value_true = "\n .. true value:\n{:.10f}\n".format(
			self.value_true)
		value_estimate = "\n .. estimate value:\n{:.10f}\n".format(
			self.value_estimate)
		absolute_error = "\n .. absolute error:\n{:.10f}\n".format(
			self.absolute_error)
		relative_error = "\n .. relative error:\n{:.10f}\n".format(
			self.relative_error)
		relative_error_as_percent = "\n .. relative error as percentage:\n{:.10f} %\n".format(
			self.relative_error_as_percent)
		s = "\n".join([
			value_true,
			value_estimate,
			absolute_error,
			relative_error,
			relative_error_as_percent,
			])
		return s

	def initialize(self, value_estimate, value_true):
		self.initialize_values_to_compare(
			value_estimate=value_estimate,
			value_true=value_true)
		self.initialize_error_values()

##