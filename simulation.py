from operations import *
import matplotlib.pyplot as plt

def print_states(states):
    for state in states:
        print(state.normalization)

def recurrent_fidelity(F_initial, iter):
    # Calculate the recurrent fidelity described in eq. 7 in the paper
    F_hist = []
    F = F_initial
    F_hist.append(F)
    for i in range(iter):
        F_after = (F ** 2 + (1 / 9) * (1 - F) ** 2) / (
                F ** 2 + (2 / 3) * F * (1 - F) + (5 / 9) * (1 - F) ** 2)
        F_hist.append(F_after)
        F = F_after
    return F_hist

def plot_fidelities(F_sim, F_expected, F_sim_std=None, plot_name='plot'):
    # Plot simulated fidelity and recurrent fidelity (expected)
    x = range(len(F_sim))
    if F_sim_std:
        plt.figure()
        plt.errorbar(x, F_sim, yerr=F_sim_std, capsize=2, fmt='bo', elinewidth=0.5, markersize=3)
    else:
        plt.plot(x, F_sim, 'bo', markersize=3)
    plt.plot(x, F_expected, 'r')
    plt.xlabel('Iterations')
    plt.ylabel('Fidelity')
    plt.savefig('figure/{}.png'.format(plot_name))

def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█'):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = '\r')
    # Print New Line on Complete
    if iteration == total:
        print()

def protocol_A_simulation(samples, threshold=1):
    fidelities_hist = {
        'min': [],
        'max': [],
        'avg': []
    }     # Final fidelities of each iteration
    iter = 0
    # Simulation starts
    while len(samples) > threshold:
        fidelities = []
        for sample in samples:
            if iter == 0:
                fidelities.append(sample.fidelity())
            uni_y_rot(sample)

        #  Add initial fidelities of samples
        if iter == 0:
            fidelities_hist['min'].append(min(fidelities))
            fidelities_hist['max'].append(max(fidelities))
            fidelities_hist['avg'].append(sum(fidelities) / float(len(fidelities)))

        remaining_sample = []
        random.shuffle(samples)
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
        # print("Iteration: {}".format(iter))
        # print("Samples remaining: {}".format(len(fidelities)))
        if len(fidelities) > 0:
            # print("Minimum fidelity: {}".format(min(fidelities)))
            fidelities_hist['min'].append(min(fidelities))
            # print("Maximum fidelity: {}".format(max(fidelities)))
            fidelities_hist['max'].append(max(fidelities))
            # print("Average fidelity: {}".format(sum(fidelities)/float(len(fidelities))))
            fidelities_hist['avg'].append(sum(fidelities)/float(len(fidelities)))

    return samples, fidelities_hist
