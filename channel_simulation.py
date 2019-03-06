"""
Simulation of a noisy quantum channel. We construct an instance of the EntangledState 
class, and pass it through a Pauli-diagonal noisy channel. 
"""
import numpy as np 
from quantum_errors import NormalizationError, ToleranceError
from entangled_state import QuantumState
#from functools import reduce 
import random

###### MODULE CONSTANTS ######

# NOTE: using spin-1 operators will throw an error below, 
# because the density matrix for the system is 4x4. 
# TODO: what operators are used to model the noisy quantum channel? 

_SPIN_X = np.sqrt(2)*np.array([0, 1, 0],[1, 0, 1],[0, 1, 0])
_SPIN_Y = np.sqrt(2)*np.array([0, -1j, 0],[1j, 0, -1j],[0, 1j, 0])
_SPIN_Z = 2.0*np.array([1, 0, 0],[0, 0, 0],[0, 0, -1])
_SPINS_VEC = [_SPIN_X, _SPIN_Y, _SPIN_Z]

random.seed(a=12345) # for reproducibility
_SAMPLE = 1000 # maximum of range for random sampling 

##############################

def noisy_channel(pure_state, probs=None, epsilon = 0.01):
	""" Implementation of a Pauli-diagonal noisy quantum channel.

	:param pure_state: instance of the QuantumState class, generally assumed to be a pure state 
	:param probs: optional tuple of 3 floats specifying mixture of spin-1 Pauli matrices, sum normalized to 1.0 
	:param probs: float < 0.1 describing the tolerance range for errors in float addition
	:returns: A QuantumState object representing the density matrix after the noisy channel 
	"""
	if probs != None: 
		if not isinstance(probs, tuple) or len(probs) != 3:
			raise NormalizationError("Must specify probs as a list of 3 probabilities.") 
		p_1, p_2, p_3 = probs 
	else: 
		# Select three random probabilities, normalized to 1.0 
		not_normed = random.sample(range(_SAMPLE), 3)
		p_1, p_2, p_3 = tuple(map(lambda x, y: x/y, not_normed, [sum(not_normed)]*3))

	net_prob = p_1 + p_2 + p_3 
	if (1.0 + self.epsilon < net_prob) or (net_prob < 1.0 - self.epsilon):
			raise NormalizationError("Probabilities are not normalized within given epsilon parameter.")
	elif epsilon > 0.1: 
		raise ToleranceError("Epsilon must be < 0.1.")

	noisy_state = 0 
	for p, spin in zip(probs, _SPINS_VEC):
		noisy_state += p*reduce(np.matmul, [spin, pure_state.density, spin]) 

	return QuantumState(noisy_state)


	
