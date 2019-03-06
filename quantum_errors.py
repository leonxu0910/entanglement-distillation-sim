"""
Defines custom errors for the EntangledState class. 

References: 
https://docs.python.org/3/tutorial/errors.html#tut-userexceptions
https://stackoverflow.com/questions/1319615/proper-way-to-declare-custom-exceptions-in-modern-python
"""

class Error(Exception): 
	pass

class NormalizationError(Error):
	def __init__(self, message):
		self.message = message

	def __str__(self):
		return self.message

class ToleranceError(Error):	
	def __init__(self, message):
		self.message = message

	def __str__(self):
		return self.message