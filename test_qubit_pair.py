from qubit_pair import *

def simple_test():
  state = QubitPair.singlet()
  print(state)

def bxor_test():
  for fidelity in [0.0, 0.5, 0.9, 0.95, 1.0]:
    print("Fidelity: {}\n".format(fidelity))
    state1 = QubitPair.singlet(fidelity)
    state2 = QubitPair.pure_triplet()
    print("Before:\n{}\n{}\n".format(state1, state2))
    state1.bxor(state2)
    print("After:\n{}\n{}\n".format(state1, state2))

if __name__ == "__main__":
  print("Simple test:")
  simple_test()
  print()

  print("BXOR test:")
  bxor_test()
  print()

