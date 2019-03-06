import numpy as np
from math import *
from cmath import *

# two qubits states in vector representation
s00 = np.matrix([1,0,0,0])	# |00>
s01 = np.matrix([0,1,0,0])	# |01>
s10 = np.matrix([0,0,1,0])	# |10>
s11 = np.matrix([0,0,0,1])	# |11>

# vector representation of bell states
amp = 1/np.sqrt(2)
psi_p = amp * (s01 + s10)	# |psi+>
psi_n = amp * (s01 - s10)	# |psi->
phi_p = amp * (s00 + s11)	# |phi+>
phi_n = amp * (s00 - s11)	# |phi->

# density matrices of bell states
rho_psi_p = np.outer(psi_p, psi_p)	# |psi+><psi+|
rho_psi_n = np.outer(psi_n, psi_n)	# |psi-><psi-|
rho_phi_p = np.outer(phi_p, phi_p)	# |phi+><phi+|
rho_phi_n = np.outer(phi_n, phi_n)	# |phi-><phi-|
# print("rho_psi_p\n", rho_psi_p)
# print("rho_psi_n\n", rho_psi_n)
# print("rho_phi_p\n", rho_phi_p)
# print("rho_phi_n\n", rho_phi_n)

# unilateral pauli rotations
uni_rot_y_pi = np.kron(np.matrix([[0,-1],[1,0]]), np.identity(2))	# unilateral pauli-y rotation by pi degrees
uni_rot_z_pi = np.kron(np.matrix([[complex(0,-1),0],[0,complex(0,1)]]), np.identity(2))
uni_rot_x_pi = np.kron(np.matrix([[0,complex(0,-1)],[complex(0,-1),0]]), np.identity(2))

# bilateral rotations
rot_y = np.matrix([[np.sqrt(2)/2,-np.sqrt(2)/2],[np.sqrt(2)/2,np.sqrt(2)/2]])
bi_rot_y = np.kron(rot_y, rot_y)
rot_z = np.matrix([[complex(np.sqrt(2)/2, -np.sqrt(2)/2), 0], [0, complex(np.sqrt(2)/2, np.sqrt(2)/2)]])
bi_rot_z = np.kron(rot_z, rot_z)
rot_x = np.matrix([[np.sqrt(2)/2, complex(0, -np.sqrt(2)/2)], [complex(0, -np.sqrt(2)/2), np.sqrt(2)/2]])
bi_rot_x = np.kron(rot_x, rot_x)

# unitary xor operation
U_xor = np.outer(s11, s10) + np.outer(s10, s11) + np.outer(s00, s00) + np.outer(s01, s01)
def base_vec(ind):
	vec = np.array([0 for i in range(16)])
	vec[ind] = 1
	return vec
BXOR = np.outer(base_vec(0),base_vec(0))+np.outer(base_vec(1),base_vec(1))+np.outer(base_vec(2),base_vec(2))+np.outer(base_vec(3),base_vec(3))+np.outer(base_vec(4),base_vec(5))+np.outer(base_vec(5),base_vec(4))+np.outer(base_vec(6),base_vec(7))+np.outer(base_vec(7),base_vec(6))+np.outer(base_vec(8),base_vec(10))+np.outer(base_vec(9),base_vec(11))+np.outer(base_vec(10),base_vec(8))+np.outer(base_vec(11),base_vec(9))+np.outer(base_vec(12),base_vec(15))+np.outer(base_vec(13),base_vec(14))+np.outer(base_vec(14),base_vec(13))+np.outer(base_vec(15),base_vec(12))

# print(BXOR)


def two_qubits_state(prob_psi_n, prob_psi_p, prob_phi_p, prob_phi_n):
	# define density matrix of an arbitary state in bell basis
	# prob_psi_n: probability of |psi-> component of the state, same pattern as other three parameters
	return prob_psi_n * rho_psi_n + prob_psi_p * rho_psi_p + prob_phi_p * rho_phi_p + prob_phi_n * rho_phi_n
	
def fidelity(M):
	# fidelity of a given state M projected onto the singlet state 
	# F = <psi-|M|psi->
	return np.inner(psi_n, np.matmul(M, psi_n.T).T).item(0)
	
def purity(M):
	# purity of the density matrix M
	# p = Trace(M^2)
	# M is pure if p = 1, mixed if p < 1
	return np.trace(np.matmul(M, M))

def F_prime(F):
	# recurrence fidelity of F'
	return (F**2 + (1/9)*(1-F)**2) / (F**2 + (2/3)*F*(1-F) + (5/9)*(1-F)**2)
	
def operate(O, M):
	# apply operator O onto density matrix M
	return np.matmul(O, np.matmul(M, O.getH()))

F = 0.4
state = two_qubits_state(F, (1-F)/3, (1-F)/3, (1-F)/3)
print(fidelity(state))

# BXOR test
# state1 = np.kron(rho_psi_p, rho_psi_n)
# state2 = np.kron(rho_psi_n, rho_phi_n)
# result = operate(np.matrix(BXOR), np.matrix(state1))
# print(state1)
# print(result)
# print(np.array_equal(state2,result))

# unilateral y rotation test code
# protocol A step 1: rotate a mostly psi- Werner state to a mostly phi+ state, ie. (R_y(pi) tp I_2) W_F (R_y(pi) tp I_2)^T
# Note: R_y(pi) is rotation around y axis by pi degrees which acts only on the first qubit. R_y(pi) = e^(-i*(pi/2)*sigma_y)) where signma_y is pauli-y matrix
#		I_2 is 2D identity matrix
#		tp is tensor product
# F = 1	# fidelity of Werner state
# mostly_psi_n = two_qubits_state(F, (1-F)/3, (1-F)/3, (1-F)/3)
# mostly_phi_p = two_qubits_state((1-F)/3, (1-F)/3, F, (1-F)/3)
# mostly_psi_n_after = np.matmul(uni_rot_y_pi, np.matmul(mostly_psi_n, uni_rot_y_pi.T))	# after rotation
# print(mostly_psi_n)
# print(mostly_phi_p)
# print(mostly_psi_n_after)	# mostly_psi_n_after should be the same as mostly_phi_p