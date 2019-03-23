import numpy as np
import random

np.random.seed()
random.seed()

def _opposite_symbol(symbol):
  if symbol == "phi":
    out = "psi"
  elif symbol == "psi":
    out = "phi"
  else:
    raise ValueError("Invalid symbol")
  return out

def _opposite_sign(sign):
  if sign == "+":
    out = "-"
  elif sign == "-":
    out = "+"
  else:
    raise ValueError("Invalid sign")
  return out

class QubitPair(dict):

  def __repr__(self):
    return "QubitPair({})".format(str(dict(self)))

  def _normalize(self):
    norm = sum(value for value in self.values())
    for k in self:
      self[k] /= norm

  def _scale(self, factor):
    for k in self:
      self[k] *= factor

  def _swap(self, key1, key2):
    self[key1], self[key2] = self[key2], self[key1]

  @classmethod
  def singlet(cls, fidelity = 1.0):
    state = cls({key: random.random() for key in ["phi+", "phi-", "psi+"]})
    state._normalize()
    state._scale(1.0 - fidelity)
    state["psi-"] = fidelity
    return state

  @classmethod
  def pure_triplet(cls):
    return cls({"phi+": 1.0, "phi-": 0.0, "psi+": 0.0, "psi-": 0.0})

  def unirotate(self, axis):
    if axis == "x":
      self._swap("phi+", "psi+")
      self._swap("phi-", "psi-")
    elif axis == "y":
      self._swap("phi+", "psi-")
      self._swap("phi-", "psi+")
    elif axis == "z":
      self._swap("phi+", "phi-")
      self._swap("psi+", "psi-")
    else:
      raise ValueError("Axis must be 'x', 'y' or 'z'")

  def birotate(self, axis):
    if axis == "x":
      self._swap("phi+", "psi+")
    elif axis == "y":
      self._swap("phi-", "psi+")
    elif axis == "z":
      self._swap("phi+", "phi-")
    else:
      raise ValueError("Axis must be 'x', 'y' or 'z'")

  # Liang: check this out!!!! It's just the normalization condition.
  def bxor(self, other):
    temp = {(ks, ko): vs * vo for ks, vs in self.items() \
                              for ko, vo in other.items()}
    self._scale(0.0)
    other._scale(0.0)
    for (source, target) in temp:
      new_source = [source[:-1], source[-1]]
      new_target = [target[:-1], target[-1]]

      if new_source[0] == "psi":
        new_target[0] = _opposite_symbol(new_target[0])
      if new_target[1] == "-":
        new_source[1] = _opposite_sign(new_source[1])

      new_source = "".join(new_source)
      new_target = "".join(new_target)

      self[new_source] += temp[source, target]
      other[new_target] += temp[source, target]

    self._normalize()
    other._normalize()


    
