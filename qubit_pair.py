import numpy as np
import random

np.random.seed()
random.seed()

def _normalize(state):
  norm = sum(value for value in state.values())
  for k in state:
    state[k] /= norm

def _scale(state, factor):
  for k in state:
    state[k] *= factor
    
class QubitPair(dict):

  def __repr__(self):
    return "QubitPair({})".format(str(dict(self)))

  @classmethod
  def singlet(cls, fidelity = 1.0):
    state = cls({key: random.random() for key in ["phi+", "phi-", "psi+"]})
    _normalize(state)
    _scale(state, 1.0 - fidelity)
    state["psi-"] = fidelity
    return state

  @classmethod
  def pure_triplet(cls):
    return {"phi+": 1.0, "phi-": 0.0, "psi+": 0.0, "psi-": 0.0}

  


