from simulation import *
from channel_simulation import generate_sim_samples
import numpy as np

def run_prot_A_sim(num_trials, num_sample_per_trial, max_sample_remain, set_iter=10, plot_name='plot'):
    '''
    Run simulation on protocol A with trials
    :param num_trials: number of simulations to run
    :param num_sample_per_trial: sample size
    :param max_sample_remain: maximum number of samples to keep for each trial (ending condition)
    :param set_iter: Because iteration in each trial may vary, take the majority to prevent varying array size
    :param plot_name: name of the output fidelity plot
    :return:
    '''
    trial_avg = np.array([[]])
    printProgressBar(0, num_trials, prefix='trials:', suffix='Complete', length=50)
    for i in range(num_trials):
        samples = generate_sim_samples(num_sample_per_trial)
        purified, f_hist = protocol_A_simulation(samples, threshold=max_sample_remain)
        # printProgressBar(i + 1, num_trials, prefix='trials:', suffix='Complete', length=50)
        # print("trial: ", i)
        # print(len(f_hist['avg']))
        if len(f_hist['avg']) != set_iter:
            continue
        if trial_avg.size == 0:
            trial_avg = np.array([f_hist['avg']])
        else:
            trial_avg = np.concatenate((trial_avg, np.array([f_hist['avg']])), axis=0)

    trials_avg = list(np.mean(trial_avg, axis=0))
    trials_std = list(np.std(trial_avg, axis=0))
    F_recur = recurrent_fidelity(trials_avg[0], len(trials_avg) - 1)
    plot_fidelities(trials_avg, F_recur, F_sim_std=trials_std, plot_name=plot_name)
    return trials_avg, trials_std


if __name__ == "__main__":
    # Simulate protocol A
    num_trials = 100
    num_sample = 500000
    max_sample_remain = 10
    avg, std = run_prot_A_sim(num_trials, num_sample, max_sample_remain, set_iter=12, plot_name='fidelity_iter')
    print("Average fidelity: {}".format(avg))
    print("Std on fidelity: {}".format(std))
