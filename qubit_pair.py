import numpy as np

# initialize seed for reproducibility
np.random.seed()

class QubitPair:
  """A four-vector representation of a qubit pair.

  By default, it's represented in the Bell basis, but can be configured to be
  represented in the Binary basis at initialization, or through a class 
  method. Contains all operations needed for quantum distillation in the form
  of class methods.

  Operations will be performed in the most appropriate basis, converting back
  and forth if needed.

  Attributes:
    vector (np.array): complex state vector, normalized
    basis (str): either "bell" or "binary"

  """

  # atomic state vectors
  _ZERO = np.array([1.0, 0.0])
  _ONE = np.array([0.0, 1.0])

  # bell states in binary basis
  _PHI_PLUS  = 1.0/np.sqrt(2.0) * (np.kron(_ZERO, _ZERO) + np.kron(_ONE, _ONE ))
  _PHI_MINUS = 1.0/np.sqrt(2.0) * (np.kron(_ZERO, _ZERO) - np.kron(_ONE, _ONE ))
  _PSI_PLUS  = 1.0/np.sqrt(2.0) * (np.kron(_ZERO, _ONE ) + np.kron(_ONE, _ZERO))
  _PSI_MINUS = 1.0/np.sqrt(2.0) * (np.kron(_ZERO, _ONE ) - np.kron(_ONE, _ZERO))

  # rotation matrices
  _BIN_TO_BELL = np.stack([_PHI_PLUS, _PHI_MINUS, _PSI_PLUS, _PSI_MINUS])
  _BELL_TO_BIN = _BIN_TO_BELL.T

  # private constructor
  def __init__(self, weights, basis)
    """Constructor. 
    
    Really not intended for client use - they should the static factor methods instead.

    Args:
      weights (list): List of weights. Doesn't need to be normalized.
      basis (str): Either "bell" or "binary": the basis to use, and basis of weights

    Notes:
      assumes sum of weights is not zero
    """

    self.vector = np.array(weights)
    self.vector /= np.sum(self.vector)
    self.basis = basis

  # factory functions
  @classmethod
  def singlet(cls, basis="bell"):
    """Factory function for a singlet Bell state in a specific basis.
    """

    if basis == "binary":
      weights = cls._PSI_MINUS
    elif basis == "bell":
      weights = np.array([0, 0, 0, 1.0])
    else:
      raise ValueError("Invalid basis: must be 'bell' or 'binary'")
    return cls(weights, basis)

  # methods
  def add_noise(self, stddev):
    """Add Gaussian noise to a Qubit pair, with a given stddev.

    Note that the internal state vector will be renormalized.
    """

    self.vector += stddev * np.random.randn(*self.vector.shape)
    self.vector /= np.sum(self.vector)

  def to_bell(self):
    if self.basis == "bell":
      return
    if self.basis == "binary":
      self.vector = self._BIN_TO_BELL.dot(self.vector)
      self.basis = "bell"
  
  def to_binary(self):
    if self.basis == "binary":
      return
    if self.basis == "bell":
      self.vector = self._BELL_TO_BIN.dot(self.vector)
      self.basis = "binary"
  
  def fidelity(self):
    """Get the fidelity (w.r.t. singlet state) of qubit pair.
    """
    # project
    if self.basis == "bell":
      out = self.vector[3] 
    elif self.basis == "binary":
      out = self._PSI_MINUS.dot(self.vector)

    # convert amplitude to probability and return
    out *= np.conj(out)
    return out


