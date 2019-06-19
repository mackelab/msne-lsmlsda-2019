from brian2 import *
import matplotlib.pyplot as plt
from gamma_oscillations.simulate_network import simulate_network
from gamma_oscillations.read_out import ReadOut
from gamma_oscillations.plots import *


if __name__ == '__main__':
    n_pyr = 500  # 500
    n_int = 100
    p_conn_pyr2int = 0.1
    p_conn_pyr2pyr = 0.1
    p_conn_int2int = 0.1
    p_conn_int2pyr = 0.1
    poisson_rate_pyr = 5 #6  # kHz
    poisson_rate_int = 1  # kHz
    runtime = 1100  # ms
    timestep = 0.05  # ms
    onset = 100  # ms

    params_pyr2int = {'name': 'AMPA', 'v': 'v', 'g_max': 2.1, 'rise': 0.5, 'decay': 2., 'E': 0., 'delay': 1.5}
    params_pyr2pyr = {'name': 'AMPA', 'v': 'v_d', 'g_max': 6., 'rise': 0.5, 'decay': 2., 'E': 0., 'delay': 1.5}
    params_int2pyr = {'name': 'GABA', 'v': 'v', 'g_max': 50., 'rise': 0.5, 'decay': 5., 'E': -75., 'delay': 0.5}
    params_int2int = {'name': 'GABA', 'v': 'v', 'g_max': 0.5, 'rise': 0.5, 'decay': 5., 'E': -75., 'delay': 0.5}
    params_poisson2pyr = {'name': 'AMPA_ext', 'v': 'v', 'g_max': 6., 'rise': 0.5, 'decay': 2., 'E': 0., 'delay': 1.5}
    params_poisson2int = {'name': 'AMPA_ext', 'v': 'v', 'g_max': 2.1, 'rise': 0.5, 'decay': 2., 'E': 0., 'delay': 1.5}

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


    plot_mem_pot(readout)
    plot_spikes(readout)
    plot_firing_rate(readout)
    plot_spectrum(readout)
    plt.show()