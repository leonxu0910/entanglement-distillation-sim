from simulation import *
from channel_simulation import generate_sim_samples
import numpy as np

def run_prot_A_sim(num_trails, num_sample_per_trial, max_sample_remain, set_iter=10, plot_name='plot'):
    '''
    Run simulation on protocol A with trails
    :param num_trails: number of simulations to run
    :param num_sample_per_trial: sample size
    :param max_sample_remain: maximum number of samples to keep for each trail (ending condition)
    :param set_iter: Because iteration in each trail may vary, take the majority to prevent varying array size
    :param plot_name: name of the output fidelity plot
    :return:
    '''
    trail_avg = np.array([])
    # printProgressBar(0, num_trails, prefix='Trails:', suffix='Complete', length=50)
    for i in range(num_trails):
        samples = generate_sim_samples(num_sample_per_trial)
        purified, f_hist = protocol_A_simulation(samples, threshold=max_sample_remain)
        # printProgressBar(i + 1, num_trails, prefix='Trails:', suffix='Complete', length=50)
        print(len(f_hist['avg']))
        if i == 0:
            trail_avg = np.array(f_hist['avg'])
        if i == 1:
            trail_avg = np.stack((trail_avg, np.array(f_hist['avg'])))
        if not len(f_hist) == set_iter:
            continue
        else:
            trail_avg = np.concatenate((trail_avg, np.array([f_hist['avg']])), axis=0)

    trails_avg = list(np.mean(trail_avg, axis=0))
    trails_std = list(np.std(trail_avg, axis=0))
    F_recur = recurrent_fidelity(trails_avg[0], len(trails_avg) - 1)
    plot_fidelities(trails_avg, F_recur, F_sim_std=trails_std, plot_name=plot_name)
    return trails_avg, trails_std


if __name__ == "__main__":
    # Simulate protocol A
    num_trails = 100
    num_sample = 500000
    max_sample_remain = 1
    avg, std = run_prot_A_sim(num_trails, num_sample, max_sample_remain, set_iter=12, plot_name='fidelity_iter')
    print("Average fidelity: {}".format(avg))
    print("Std on fidelity: {}".format(std))
