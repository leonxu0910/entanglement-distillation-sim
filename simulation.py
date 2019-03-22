from channel_simulation import generate_sim_samples
from operations import *

num_sample = 500000
threshold = 1

def print_states(states):
    for state in states:
        print(state.normalization)

samples = generate_sim_samples(num_sample)  # Generate simulation samples
fidelities = []     # Final fidelities of each iteration
iter = 0

# Simulation starts
while len(samples) > threshold:
    for sample in samples:
        uni_y_rot(sample)

    remaining_sample = []
    for source, target in zip(samples[0::2], samples[1::2]):
        keep = bxor(source, target)
        if keep:
            remaining_sample.append(keep)

    fidelities = []
    samples = remaining_sample[:]
    for sample in samples:
        uni_y_rot(sample)
        fidelities.append(sample.fidelity())

    iter += 1
    print("Iteration: {}".format(iter))
    print("Samples remaining: {}".format(len(fidelities)))
    if len(fidelities) > 0:
        print("Minimum fidelity: {}".format(min(fidelities)))
        print("Maximum fidelity: {}".format(max(fidelities)))
        print("Average fidelity: {}".format(sum(fidelities)/float(len(fidelities))))

print_states(samples)

