"""
Implementation of a simulated entangled quantum state. 
"""
import numpy as np
from quantum_errors import NormalizationError, ToleranceError
from util import *

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
		""" Computes the overlap of the current state with the singlet state _SINGLET, using 
		the vector representation of the Bell states.  
		"""
		right_side = np.matmul(self.density, VEC_SINGLET_)
		return float(np.matmul(np.conj(VEC_SINGLET_), right_side)) # should we return a Python float or numpy float here?

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

		net_prob = sum(self.normalization)
		if (1.0 + self.epsilon < net_prob) or (net_prob < 1.0 - self.epsilon):
			raise NormalizationError("Entangled state not properly normalized within given epsilon parameter.")

		# This is a functional implementation of the density matrix, mostly for me to practice! 
		# Not particularly readable, so I've included the equivalent code below. Either implementation works.  
		density_basis = list(map(lambda p, state: p*np.outer(state, state), self.normalization, BELL_STATES_))
		self.density = sum(density_basis)

	def density_vector(self):
		""" Computes the density matrix of current state with the vector representation of the Bell states. 
		Currently only for debugging; output of this function matches the self.density object constructed in 
		the initializer. 
		"""
		density_basis = list(map(lambda p, state: p*np.outer(state, state), self.normalization, BELL_VECTORS_))
		return sum(density_basis)

