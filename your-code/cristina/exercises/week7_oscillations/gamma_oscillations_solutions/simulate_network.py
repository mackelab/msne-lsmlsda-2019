from brian2 import *
from gamma_oscillations.models import *
from gamma_oscillations import *


def simulate_network(runtime, timestep, n_pyr, n_int,
                     params_pyr2int, params_pyr2pyr, params_int2pyr, params_int2int,
                     params_poisson2pyr, params_poisson2int,
                     p_conn_pyr2int, p_conn_pyr2pyr, p_conn_int2int, p_conn_int2pyr,
                     poisson_rate_pyr, poisson_rate_int):
    runtime *= ms
    timestep *= ms
    network_objects = []  # objects that are needed to create the network

    syn_pyr2int_model = SynapseModel(**params_pyr2int)
    syn_pyr2pyr_model = SynapseModel(**params_pyr2pyr)
    syn_int2int_model = SynapseModel(**params_int2int)
    syn_int2pyr_model = SynapseModel(**params_int2pyr)
    syn_poisson2pyr_model = SynapseModel(**params_poisson2pyr)
    syn_poisson2int_model = SynapseModel(**params_poisson2int)

    ints, pyrs = create_neurons(n_int, n_pyr, syn_int2int_model, syn_int2pyr_model, syn_pyr2int_model,
                                syn_pyr2pyr_model, syn_poisson2pyr_model, syn_poisson2int_model)
    network_objects.extend([pyrs, ints])

    syn_int2int, syn_int2pyr, syn_pyr2int, syn_pyr2pyr = create_connections(ints, pyrs, p_conn_pyr2int, p_conn_pyr2pyr,
                                                                            p_conn_int2int, p_conn_int2pyr,
                                                                            syn_int2int_model, syn_int2pyr_model,
                                                                            syn_pyr2int_model, syn_pyr2pyr_model)
    network_objects.extend([syn_pyr2int, syn_pyr2pyr, syn_int2int, syn_int2pyr])

    poisson2int, poisson2pyr, syn_poisson2int, syn_poisson2pyr = create_poisson_input(ints, pyrs, n_int, n_pyr,
                                                                                      poisson_rate_pyr,
                                                                                      poisson_rate_int,
                                                                                      syn_poisson2int_model,
                                                                                      syn_poisson2pyr_model)
    network_objects.extend([syn_poisson2pyr, syn_poisson2int, poisson2pyr, poisson2int])

    (spike_monitor_pyr, poprate_monitor_pyr, state_monitor_pyr,
        spike_monitor_int, poprate_monitor_int, state_monitor_int) = create_monitors(timestep, ints, pyrs)
    network_objects.extend([spike_monitor_pyr, poprate_monitor_pyr, state_monitor_pyr,
                            spike_monitor_int, poprate_monitor_int, state_monitor_int])

    # run
    net = Network(*network_objects)
    net.run(runtime + timestep)

    return (spike_monitor_pyr, poprate_monitor_pyr, state_monitor_pyr,
            spike_monitor_int, poprate_monitor_int, state_monitor_int)


def create_neurons(n_int, n_pyr, syn_int2int_model, syn_int2pyr_model, syn_pyr2int_model, syn_pyr2pyr_model,
                   syn_poisson2pyr_model, syn_poisson2int_model):
    pyrs = NeuronGroup(n_pyr,
                       get_eqs_pyr() + syn_pyr2pyr_model.get_eqs() + syn_int2pyr_model.get_eqs()
                       + syn_poisson2pyr_model.get_eqs(),
                       namespace=merge_dicts([get_params_pyr(), syn_pyr2pyr_model.get_params(),
                                              syn_int2pyr_model.get_params(), syn_poisson2pyr_model.get_params()]),
                       method='exponential_euler',
                       threshold='v>0*mV', refractory=1.5 * ms)
    ints = NeuronGroup(n_int,
                       get_eqs_int() + syn_pyr2int_model.get_eqs() + syn_int2int_model.get_eqs() +
                       syn_poisson2int_model.get_eqs(),
                       namespace=merge_dicts([get_params_int(), syn_pyr2int_model.get_params(),
                                              syn_int2int_model.get_params(), syn_poisson2int_model.get_params()]),
                       method='exponential_euler',
                       threshold='v>0*mV', refractory=1.5 * ms)
    return ints, pyrs


def create_connections(ints, pyrs, p_conn_pyr2int, p_conn_pyr2pyr, p_conn_int2int, p_conn_int2pyr,
                       syn_int2int_model, syn_int2pyr_model, syn_pyr2int_model, syn_pyr2pyr_model):
    syn_pyr2int = Synapses(pyrs, ints, on_pre=syn_pyr2int_model.get_eqs_on_pre(), delay=syn_pyr2int_model.delay)
    syn_pyr2pyr = Synapses(pyrs, pyrs, on_pre=syn_pyr2pyr_model.get_eqs_on_pre(), delay=syn_pyr2pyr_model.delay)
    syn_int2int = Synapses(ints, ints, on_pre=syn_int2int_model.get_eqs_on_pre(), delay=syn_int2int_model.delay)
    syn_int2pyr = Synapses(ints, pyrs, on_pre=syn_int2pyr_model.get_eqs_on_pre(), delay=syn_int2pyr_model.delay)
    syn_pyr2int.connect(p=p_conn_pyr2int)
    syn_pyr2pyr.connect(p=p_conn_pyr2pyr)
    syn_int2int.connect(p=p_conn_int2int)
    syn_int2pyr.connect(p=p_conn_int2pyr)
    return syn_int2int, syn_int2pyr, syn_pyr2int, syn_pyr2pyr


def create_poisson_input(ints, pyrs, n_int, n_pyr, poisson_rate_pyr, poisson_rate_int, syn_poisson2int_model, syn_poisson2pyr_model):
    poisson2pyr = PoissonGroup(n_pyr, rates=poisson_rate_pyr*kHz)
    poisson2int = PoissonGroup(n_int, rates=poisson_rate_int*kHz)
    syn_poisson2pyr = Synapses(poisson2pyr, pyrs, on_pre=syn_poisson2pyr_model.get_eqs_on_pre(),
                               delay=syn_poisson2pyr_model.delay)
    syn_poisson2int = Synapses(poisson2int, ints, on_pre=syn_poisson2int_model.get_eqs_on_pre(),
                               delay=syn_poisson2int_model.delay)
    syn_poisson2pyr.connect(j='i')
    syn_poisson2int.connect(j='i')
    return poisson2int, poisson2pyr, syn_poisson2int, syn_poisson2pyr


def create_monitors(dt, ints, pyrs):
    spike_monitor_pyr = SpikeMonitor(pyrs)
    poprate_monitor_pyr = PopulationRateMonitor(pyrs)
    spike_monitor_int = SpikeMonitor(ints)
    poprate_monitor_int = PopulationRateMonitor(ints)
    state_monitor_pyr = StateMonitor(pyrs, ['v', 'I_AMPA', 'I_GABA'], record=True, dt=dt)
    state_monitor_int = StateMonitor(ints, ['v', 'I_AMPA', 'I_GABA'], record=True, dt=dt)
    return (spike_monitor_pyr, poprate_monitor_pyr, state_monitor_pyr,
            spike_monitor_int, poprate_monitor_int, state_monitor_int)