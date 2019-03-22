import random

def werner_norm(F, bell_state):
    # Generate normalization for Werner state
    F_ = (1-F)/3
    norm = [F_, F_, F_, F_]
    norm[bell_state] = F
    return norm

def uni_y_rot(state):
    """ Perform unitary y rotation.
    """
    state.normalization[1], state.normalization[3] = state.normalization[3], state.normalization[1]
    state.normalization[0], state.normalization[2] = state.normalization[2], state.normalization[0]

def bxor(source, target):
    # Probabilistic implementation of BXOR operation
    F = source.normalization[2] * target.normalization[2]
    rand = random.random()
    if rand < F:
        return source