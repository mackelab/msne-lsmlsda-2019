from brian2 import *
import matplotlib.pyplot as plt
from gamma_oscillations.simulate_network import simulate_network
from gamma_oscillations.read_out import ReadOut
from gamma_oscillations.plots import *


if __name__ == '__main__':
    factors = np.arange(1., 10.+1.5, 1.5)
    n_pyr = 1
    n_int = 100
    p_conn_pyr2int = 0.
    p_conn_pyr2pyr = 0.
    p_conn_int2int = 0.1
    p_conn_int2pyr = 0.
    runtime = 1100  # ms
    timestep = 0.05  # ms
    onset = 100  # ms
    poisson_rate_pyr = 0  # kHz
    poisson_rate_int_base = 1  # kHz
    g_max_base = 2.1

    params_pyr2int = {'name': 'AMPA', 'v': 'v', 'g_max': 2.1, 'rise': 0.5, 'decay': 2., 'E': 0., 'delay': 1.5}
    params_pyr2pyr = {'name': 'AMPA', 'v': 'v_d', 'g_max': 6., 'rise': 0.5, 'decay': 2., 'E': 0., 'delay': 1.5}
    params_int2pyr = {'name': 'GABA', 'v': 'v', 'g_max': 50., 'rise': 0.5, 'decay': 5., 'E': -75., 'delay': 0.5}
    params_int2int = {'name': 'GABA', 'v': 'v', 'g_max': 0.5, 'rise': 0.5, 'decay': 5., 'E': -75., 'delay': 0.5}
    params_poisson2pyr = {'name': 'AMPA_ext', 'v': 'v', 'g_max': 6., 'rise': 0.5, 'decay': 2., 'E': 0., 'delay': 1.5}
    params_poisson2int = {'name': 'AMPA_ext', 'v': 'v', 'g_max': g_max_base, 'rise': 0.5, 'decay': 2., 'E': 0.,
                          'delay': 1.5}

    mean_firingrates = np.zeros(len(factors))
    frequencies = np.zeros(len(factors))
    coherences = np.zeros(len(factors))

    for idx, factor in enumerate(factors):
        poisson_rate_int = poisson_rate_int_base * factor
        params_poisson2int['g_max'] = g_max_base / float(factor)

        (spike_monitor_pyr, poprate_monitor_pyr, state_monitor_pyr,
            spike_monitor_int, poprate_monitor_int, state_monitor_int) = simulate_network(runtime, timestep, n_pyr, n_int,
                                                                                          params_pyr2int, params_pyr2pyr,
                                                                                          params_int2pyr, params_int2int,
                                                                                          params_poisson2pyr,
                                                                                          params_poisson2int,
                                                                                          p_conn_pyr2int, p_conn_pyr2pyr,
                                                                                          p_conn_int2int, p_conn_int2pyr,
                                                                                          poisson_rate_pyr, poisson_rate_int)

        readout = ReadOut(spike_monitor_pyr, poprate_monitor_pyr, state_monitor_pyr,
                          spike_monitor_int, poprate_monitor_int, state_monitor_int,
                          runtime, timestep, n_pyr, n_int, onset)

        # compute variables
        _, spiketimes_cells_int = readout.get_spiketimes_cells()
        firingrates_int = compute_firingrate_cells(spiketimes_cells_int, runtime)
        mean_firingrates[idx] = np.mean(firingrates_int)

        _, poprate_int, poprate_t = readout.get_populationrate()
        freq_vect, power_int = compute_spectrum_multitaper(poprate_int - np.mean(poprate_int), poprate_t[1] - poprate_t[0])
        frequencies[idx] = freq_vect[np.argmax(power_int)]

        _, spiketimes_cells = readout.get_spiketimes_cells()
        dt_coherence = 1.  # ms
        spiketrains_cells = np.zeros((len(spiketimes_cells), int(round(runtime / dt_coherence)) + 1))
        for i in range(len(spiketimes_cells)):
            spiketrains_cells[i] = spiketrain_from_spiketimes(spiketimes_cells[i], runtime, dt_coherence)
        coherences[idx] = coherence_index_pop(spiketrains_cells)

        # plot_spikes(readout)
        # plot_spectrum(readout)
        # plt.show()


    plt.figure()
    plt.subplot(3, 1, 1)
    plt.plot(factors, mean_firingrates, marker='o', linestyle='-', color='k')
    plt.ylabel('Mean firing rate')
    plt.xlabel('Increase ext. drive')
    plt.xlabel('Increase noise ->')
    plt.ylim(0, 200)
    plt.xlim(10, 1)
    plt.subplot(3, 1, 2)
    plt.plot(factors, frequencies, marker='o', linestyle='-', color='k')
    plt.ylabel('Frequency')
    plt.xlabel('Increase ext. drive')
    plt.xlabel('Increase noise ->')
    plt.ylim(0, 200)
    plt.xlim(10, 1)
    plt.subplot(3, 1, 3)
    plt.plot(factors, coherences, marker='o', linestyle='-', color='k')
    plt.ylabel('Coherence')
    plt.xlabel('Increase ext. drive')
    plt.xlabel('Increase noise ->')
    plt.ylim(0, 1)
    plt.xlim(10, 1)
    plt.tight_layout()
    plt.show()