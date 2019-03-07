""" 
Sandbox for EntangledState class development.
"""
from entangled_state import QuantumState, DiagonalState
from util import *

###### Class constants from EntangledState; useful for debugging ######

if __name__ == "__main__":
	# Various implementations of density matrix construction 
	test = [SINGLET_, TRIP_1_]
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
	vector_test = (np.inner(VEC_SINGLET_, VEC_TRIP_3_), np.inner(VEC_TRIP_3_, VEC_TRIP_2_), np.inner(VEC_TRIP_1_, VEC_SINGLET_))
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

	# Testing unitary y rotation
	# Pure state test
	psi_p = DiagonalState(normalization=[0.0, 1.0, 0.0, 0.0])
	psi_p.uni_y_rot()
	print("Psi+ -> Phi- rotated: \n", psi_p.density_vector())
	print("Phi-: \n", np.outer(TRIP_3_, TRIP_3_))
	# Mixed state test
	F = 0.7
	mostly_psi_n = DiagonalState(normalization=werner_norm(F, 0))
	mostly_psi_n.uni_y_rot()
	mostly_phi_p = DiagonalState(normalization=werner_norm(F, 2))
	print("Mostly phi+ state rotated: \n", mostly_psi_n.density_vector())
	print("Mostly phi+ state: \n", mostly_phi_p.density_vector())


