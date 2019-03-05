"""
Implementation of a simulated entangled quantum state. 
"""
import numpy as np
from quantum_errors import NormalizationError, ToleranceError 

# Basis vectors
_UP = np.array([1,0])
_DOWN = np.array([0,1])

# Bell states, as matrices 
_SINGLET = 1/np.sqrt(2) * (np.outer(_UP, _DOWN) - np.outer(_DOWN, _UP))
_TRIP_1 = 1/np.sqrt(2) * (np.outer(_UP, _DOWN) + np.outer(_DOWN, _UP))
_TRIP_2 = 1/np.sqrt(2) * (np.outer(_UP, _UP) + np.outer(_DOWN, _DOWN))
_TRIP_3 = 1/np.sqrt(2) * (np.outer(_UP, _UP) - np.outer(_DOWN, _DOWN))
_BELL_STATES = [_SINGLET, _TRIP_1, _TRIP_2, _TRIP_3] # Useful for some methods below 

class EntangledState: 
	""" Generates an entangled state over a basis of Bell states.
	Defaults to the singlet state. 

	:param normalization: list of 4 floats describing the amount to mix each Bell state
	:param epsilon: float < 0.1 describing the tolerance range for errors in float addition 
	"""
	def __init__(self, normalization = [1.0, 0.0, 0.0, 0.0], epsilon = 0.01):
		if len(normalization) != 4:
			raise NormalizationError("Too few/too many probabilities entered; param normalization must have length of 4.")
		elif epsilon > 0.1: 
			raise ToleranceError("Epsilon must be < 0.1.")

		self.epsilon = epsilon
		self.normalization = normalization

		self.singlet_p = self.normalization[0]
		self.trip_1_p = self.normalization[1]
		self.trip_2_p = self.normalization[2]
		self.trip_3_p = self.normalization[3]

		net_prob = sum(self.normalization)
		if (1.0 + self.epsilon < net_prob) or (net_prob < 1.0 - self.epsilon):
			raise NormalizationError("Entangled state not properly normalized within given epsilon parameter.")

		# This is a functional implementation of the density matrix, mostly for me to practice! 
		# Not particularly readable, so I've included the equivalent code below. Either implementation works.  
		density_basis = list(map(lambda p, state: p*np.outer(state, state), normalization, _BELL_STATES))
		self.density = sum(density_basis)

		## Computing the density matrix, readable code ## 
		"""
		self.density = 0
		for state, p in zip(_BELL_STATES, self.normalization):
			self.density += p*np.outer(state, state)
		"""

	def fidelity(self):
		""" Computes the overlap of the current state with the singlet state _SINGLET. 
		"""
		raise NotImplementedError

############ Testing ############
if __name__ == "__main__":
	test = [_SINGLET, _TRIP_1]
	test2 = [0.4, 0.6] 
	
	result = 0
	for state, p in zip(test, test2):
		result += p*np.outer(state, state)	
	#print("Density matrix, naive method: {}".format(result))

	output = list(map(lambda state, p: p*np.outer(state, state), test, test2))
	#print("Density matrix, functional programming: {} ".format(sum(output)))

	### Testing class implementation ### 
	basic_state = EntangledState(normalization=[0.4, 0.6, 0.0, 0.0])
	#print("Density matrix, class implementation: {}".format(basic_state.density))

	# All of the above density matrices match! 

	# Testing implemented errors; behave as expected 
	# normalization_error = EntangledState(normalization=[1.0, 0.0, 0.0, 1.0, 2.0])
	# tolerance_error = EntangledState(epsilon=0.3)


	