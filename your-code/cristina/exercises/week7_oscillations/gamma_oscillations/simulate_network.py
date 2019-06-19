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
    '''
    Creates a population of interneurons and pyramidal cells.

    :param n_int: Number of interneurons.
    :type n_int: int
    :param n_pyr: Number of pyramidal cells.
    :type n_pyr: int
    :param syn_int2int_model: Manages equations and parameters of connections from interneurons to interneurons.
    :type syn_int2int_model: SynapseModel
    :param syn_int2pyr_model: Manages equations and parameters of connections from interneurons to pyramidal cells.
    :type syn_int2pyr_model: SynapseModel
    :param syn_pyr2int_model: Manages equations and parameters of connections from pyramidal cells to interneurons.
    :type syn_pyr2int_model: SynapseModel
    :param syn_pyr2pyr_model: Manages equations and parameters of connections from pyramidal cells to pyramidal cells.
    :type syn_pyr2pyr_model: SynapseModel
    :param syn_poisson2pyr_model: Manages equations and parameters of connections from external pyramidal cells to
                                  pyramidal cells.
    :type syn_poisson2pyr_model: SynapseModel
    :param syn_poisson2int_model: Manages equations and parameters of connections from external pyramidal cells to
                                  pyramidal cells.
    :type syn_poisson2int_model: SynapseModel
    :return: Interneuron and pyramidal cell population.
    :rtype: NeuronGroup, NeuronGroup
    '''
    pass


def create_connections(ints, pyrs, p_conn_pyr2int, p_conn_pyr2pyr, p_conn_int2int, p_conn_int2pyr,
                       syn_int2int_model, syn_int2pyr_model, syn_pyr2int_model, syn_pyr2pyr_model):
    '''
    Creates Synapses and connects interneuron and pyramidal cell populations.

    :param ints: Population of interneurons.
    :type ints: NeuronGroup
    :param pyrs: Population of pyramidal cells.
    :type pyrs: NeuronGroup
    :param p_conn_pyr2int: Probability ([0, 1]) of connecting any pair of cells from the pyramidal cell to the
                           interneuron population.
    :type p_conn_pyr2int: float
    :param p_conn_pyr2pyr: Probability ([0, 1]) of connecting any pair of cells from from the pyramidal cell to the
                           pyramidal cell population.
    :type p_conn_pyr2pyr: float
    :param p_conn_int2int: Probability ([0, 1]) of connecting any pair of cells from the interneuron to the
                           interneuron population.
    :type p_conn_int2int: float
    :param p_conn_int2pyr: Probability ([0, 1]) of connecting any pair of cells from the interneuron to the
                           pyramidal cell population.
    :type p_conn_int2pyr: float
    :param syn_int2int_model: Manages equations and parameters of connections from interneurons to interneurons.
    :type syn_int2int_model: SynapseModel
    :param syn_int2pyr_model: Manages equations and parameters of connections from interneurons to pyramidal cells.
    :type syn_int2pyr_model: SynapseModel
    :param syn_pyr2int_model: Manages equations and parameters of connections from pyramidal cells to interneurons.
    :type syn_pyr2int_model: SynapseModel
    :param syn_pyr2pyr_model: Manages equations and parameters of connections from pyramidal cells to pyramidal cells.
    :type syn_pyr2pyr_model: SynapseModel
    :return: Synapses from interneurons to interneurons, from interneurons to pyramidal cells, from pyramidal cells to
             interneurons and from pyramidal cells to pyramidal cells.
    :rtype Synapses, Synapses, Synapses, Synapses
    '''
    pass


def create_poisson_input(ints, pyrs, n_int, n_pyr, poisson_rate_pyr, poisson_rate_int, syn_poisson2int_model, syn_poisson2pyr_model):
    '''
    Creates Poisson generated input to the pyramidal cell and interneuron population, respectively. Each cell
    is connected to exactly one Poisson-driven synapse.

    :param ints: Population of interneurons.
    :type ints: NeuronGroup
    :param pyrs: Population of pyramidal cells.
    :type pyrs: NeuronGroup
    :param n_int: Number of interneurons.
    :type n_int: int
    :param n_pyr: Number of pyramidal cells.
    :type n_pyr: int
    :param poisson_rate_pyr: Firing rate (kHz) of external cells that connect to pyramidal cells.
    :type poisson_rate_pyr: float
    :param poisson_rate_int: Firing rate (kHz) of external cells that connect to interneurons.
    :type poisson_rate_int: float
    :param syn_poisson2int_model: Manages equations and parameters of connections from a Poisson-driven synapse to
                                  interneurons.
    :type syn_poisson2int_model: SynapseModel
    :param syn_poisson2pyr_model: Manages equations and parameters of connections from a Poisson-driven synapse to
                                  pyramidal cells.
    :type syn_poisson2pyr_model: SynapseModel
    :return: The generators for Poisson-spiking and the synapses for the interneuron and pyramidal cell population,
             respectively.
    :rtype: PoissonGroup, PoissonGroup, Synapses, Synapses
    '''
    pass


def create_monitors(dt, ints, pyrs):
    spike_monitor_pyr = SpikeMonitor(pyrs)
    poprate_monitor_pyr = PopulationRateMonitor(pyrs)
    spike_monitor_int = SpikeMonitor(ints)
    poprate_monitor_int = PopulationRateMonitor(ints)
    state_monitor_pyr = StateMonitor(pyrs, ['v', 'I_AMPA', 'I_GABA'], record=True, dt=dt)
    state_monitor_int = StateMonitor(ints, ['v', 'I_AMPA', 'I_GABA'], record=True, dt=dt)
    return (spike_monitor_pyr, poprate_monitor_pyr, state_monitor_pyr,
            spike_monitor_int, poprate_monitor_int, state_monitor_int)
