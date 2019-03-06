"""
Implementation of a simulated entangled quantum state. 
"""
import numpy as np
from quantum_errors import NormalizationError, ToleranceError 

###### CONSTANTS ######

# Basis vectors
_UP = np.array([1,0])
_DOWN = np.array([0,1])

# Bell states, as matrices 
_SINGLET = 1/np.sqrt(2) * (np.outer(_UP, _DOWN) - np.outer(_DOWN, _UP))
_TRIP_1 = 1/np.sqrt(2) * (np.outer(_UP, _DOWN) + np.outer(_DOWN, _UP))
_TRIP_2 = 1/np.sqrt(2) * (np.outer(_UP, _UP) + np.outer(_DOWN, _DOWN))
_TRIP_3 = 1/np.sqrt(2) * (np.outer(_UP, _UP) - np.outer(_DOWN, _DOWN))
_BELL_STATES = [_SINGLET, _TRIP_1, _TRIP_2, _TRIP_3] # Useful for some methods below 

# Bell states, as vectors in a four-dimensional Hilbert space spanned by |00>, |01>, |10>, and |11> 
_VEC_SINGLET = np.array([0, -1/np.sqrt(2), 1/np.sqrt(2), 0])
_VEC_TRIP_1 = np.array([0, 1/np.sqrt(2), 1/np.sqrt(2), 0])
_VEC_TRIP_2 = np.array([1/np.sqrt(2), 0, 0, 1/np.sqrt(2)])
_VEC_TRIP_3 = np.array([-1/np.sqrt(2), 0, 0, 1/np.sqrt(2)])
_BELL_VECTORS = [_VEC_SINGLET, _VEC_TRIP_1, _VEC_TRIP_2, _VEC_TRIP_3]

#######################

class QuantumState: 
	""" General quantum state; can be a mixed, pure, entangled or product state. 
	We assume the density matrix is for a two qubit system, where the Hilbert space 
	is spanned by |00>, |01>, |10>, and |11>.
	
	:param density: density matrix for the quantum state, input as a numpy tensor
	"""
	def __init__(self, density):
		self.density = density 
		if self.density.shape != (4,4): 
			raise NormalizationError("Input density matrix is not for a two-qubit quantum state; must be 4x4.s")

	def fidelity(self):
		""" Computes the overlap of the current state with the singlet state __SINGLET, using 
		the vector representation of the Bell states.  
		"""
		right_side = np.matmul(self.density, _VEC_SINGLET)
		return float(np.matmul(np.conj(_VEC_SINGLET), right_side)) # should we return a Python float or numpy float here? 

class DiagonalState(QuantumState): 
	""" Generates an entangled state that is diagonal in the Bell basis. 
	Defaults to the singlet state. 

	:param normalization: list of 4 floats describing the amount to mix each Bell state;
	assumes the order [singlet, triplet1, triplet2, triplet3] as defined in constants above
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
		density_basis = list(map(lambda p, state: p*np.outer(state, state), self.normalization, _BELL_STATES))
		self.density = sum(density_basis)

		## Computing the density matrix, readable code ## 
		"""
		self.density = 0
		for state, p in zip(_BELL_STATES, self.normalization):
			self.density += p*np.outer(state, state)
		"""

	# Moved to QuantumState class 
	""" 
	def fidelity(self):
		# Computes the overlap of the current state with the singlet state __SINGLET, using 
		# the vector representation of the Bell states.  
		
		right_side = np.matmul(self.density, _VEC_SINGLET)
		return float(np.matmul(np.conj(_VEC_SINGLET), right_side)) # should we return a Python float or numpy float here? 
	"""

	def density_vector(self):
		""" Computes the density matrix of current state with the vector representation of the Bell states. 
		Currently only for debugging; output of this function matches the self.density object constructed in 
		the initializer. 
		"""
		density_basis = list(map(lambda p, state: p*np.outer(state, state), self.normalization, _BELL_VECTORS))	 
		return sum(density_basis)



	