import numpy as np
###### CONSTANTS ######

# Basis vectors
UP_ = np.array([1,0])
DOWN_ = np.array([0,1])

# Bell states, as matrices
SINGLET_ = 1/np.sqrt(2) * (np.outer(UP_, DOWN_) - np.outer(DOWN_, UP_))
TRIP_1_ = 1/np.sqrt(2) * (np.outer(UP_, DOWN_) + np.outer(DOWN_, UP_))
TRIP_2_ = 1/np.sqrt(2) * (np.outer(UP_, UP_) + np.outer(DOWN_, DOWN_))
TRIP_3_ = 1/np.sqrt(2) * (np.outer(UP_, UP_) - np.outer(DOWN_, DOWN_))
BELL_STATES_ = [SINGLET_, TRIP_1_, TRIP_2_, TRIP_3_] # Useful for some methods below

# Bell states, as vectors in a four-dimensional Hilbert space spanned by |00>, |01>, |10>, and |11>
VEC_SINGLET_ = np.array([0, -1/np.sqrt(2), 1/np.sqrt(2), 0])
VEC_TRIP_1_ = np.array([0, 1/np.sqrt(2), 1/np.sqrt(2), 0])
VEC_TRIP_2_ = np.array([1/np.sqrt(2), 0, 0, 1/np.sqrt(2)])
VEC_TRIP_3_ = np.array([-1/np.sqrt(2), 0, 0, 1/np.sqrt(2)])
BELL_VECTORS_ = [VEC_SINGLET_, VEC_TRIP_1_, VEC_TRIP_2_, VEC_TRIP_3_]

#######################



