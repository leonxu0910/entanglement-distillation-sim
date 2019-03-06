""" 
Sandbox for EntangledState class development.
"""
from entangled_state import QuantumState, DiagonalState 
import numpy as np

###### Class constants from EntangledState; useful for debugging ###### 

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

if __name__ == "__main__":
	# Various implementations of density matrix construction 
	test = [_SINGLET, _TRIP_1]
	test2 = [0.4, 0.6] 

	result = 0
	for state, p in zip(test, test2):
		result += p*np.outer(state, state)	
	#print("Density matrix, naive method: {}".format(result))

	output = list(map(lambda state, p: p*np.outer(state, state), test, test2))
	#print("Density matrix, functional programming: {} ".format(sum(output)))

	### Testing class implementation ### 
	basic_state = DiagonalState(normalization=[0.4, 0.6, 0.0, 0.0])
	#print("Density matrix, class implementation: {}".format(basic_state.density))

	# All of the above density matrices match! 

	# Testing implemented errors; behave as expected 
	# normalization_error = EntangledState(normalization=[1.0, 0.0, 0.0, 1.0, 2.0])
	# tolerance_error = EntangledState(epsilon=0.3)

	# Testing vector representation of Bell states 
	vector_test = (np.inner(_VEC_SINGLET, _VEC_TRIP_3), np.inner(_VEC_TRIP_3, _VEC_TRIP_2), np.inner(_VEC_TRIP_1, _VEC_SINGLET)) 
	print(vector_test) # returns (0.0, 0.0, 0.0) as expected 

	# Testing fidelity function 
	pure_state = DiagonalState()
	print(pure_state.fidelity()) # returns ~1, as expected 
	print(type(pure_state.fidelity())) # currently returning a Python float 

	pure_triplet = DiagonalState(normalization=[0.0, 1.0, 0.0, 0.0])
	print(pure_triplet.fidelity()) # returns 0.0, as expected 

	# Let's ensure that density matrix calculated with vector representation is correct 
	## Triplet 1 state ## 
	print("Triplet 1 density matrix: {}".format(pure_triplet.density))
	print("Triplet 1 density matrix, with vecto rep: {}".format(pure_triplet.density_vector()))
	## Singlet state ## 
	print("Singlet density matrix: {}".format(pure_state.density))
	print("Singlet density matrix, with vecto rep: {}".format(pure_state.density_vector()))
	# These match! Our implementation is correct <3 

	# Testing the QuantumState parent class
	singlet = np.array([[0,0,0,0],[0, 0.5, -0.5, 0],[0, -0.5, 0.5, 0],[0,0,0,0]]) 
	general_state = QuantumState(singlet)
	print(general_state.fidelity()) # returns 1.0, as expected 



