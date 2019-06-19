import numpy as np
from brian2 import *


class ReadOut:

    def __init__(self, spike_monitor_pyr, poprate_monitor_pyr, state_monitor_pyr,
                       spike_monitor_int, poprate_monitor_int, state_monitor_int,
                       runtime, timestep, n_pyr, n_int, onset=0):
        self.runtime = runtime
        self.timestep = timestep
        self.n_pyr = n_pyr
        self.n_int = n_int

        self.onset = onset
        self.onset_idx = int(round(self.onset / timestep))

        self.spike_monitor_pyr = spike_monitor_pyr
        self.spike_monitor_int = spike_monitor_int
        self.poprate_monitor_pyr = poprate_monitor_pyr
        self.poprate_monitor_int = poprate_monitor_int
        self.state_monitor_pyr = state_monitor_pyr
        self.state_monitor_int = state_monitor_int

        self.spiketimes_pyr = None
        self.spiketimes_int = None
        self.spiketimes_cellidxs_pyr = None
        self.spiketimes_cellidxs_int = None

    def get_vm(self):
        vm_pyr = self.state_monitor_pyr.get_states()['v'].T / mV
        vm_int = self.state_monitor_int.get_states()['v'].T / mV
        t = self.state_monitor_pyr.get_states()['t'] / ms

        if self.onset != 0:
            vm_pyr = vm_pyr[:, self.onset_idx:]
            vm_int = vm_int[:, self.onset_idx:]
            t = t[self.onset_idx:] - self.onset
        return vm_pyr, vm_int, t

    def get_spiketimes(self):
        self.spiketimes_pyr = self.spike_monitor_pyr.t / ms
        self.spiketimes_int = self.spike_monitor_int.t / ms
        self.spiketimes_cellidxs_pyr = self.spike_monitor_pyr.i
        self.spiketimes_cellidxs_int = self.spike_monitor_int.i

        if self.onset != 0:
            idxs = self.spiketimes_pyr > self.onset
            self.spiketimes_pyr = self.spiketimes_pyr[idxs] - self.onset
            self.spiketimes_cellidxs_pyr  = self.spiketimes_cellidxs_pyr [idxs]
            idxs = self.spiketimes_int > self.onset
            self.spiketimes_int = self.spiketimes_int[idxs] - self.onset
            self.spiketimes_cellidxs_int = self.spiketimes_cellidxs_int[idxs]
        return self.spiketimes_cellidxs_pyr, self.spiketimes_cellidxs_int, self.spiketimes_pyr, self.spiketimes_int

    def get_spiketimes_cells(self):
        if self.spiketimes_pyr is None:
            self.get_spiketimes()

        spiketimes_cells_pyr = np.zeros(self.n_pyr, dtype=object)
        spiketimes_cells_int = np.zeros(self.n_int, dtype=object)

        for cellidx in range(self.n_pyr):
            spiketimes_cells_pyr[cellidx] = self.spiketimes_pyr[self.spiketimes_cellidxs_pyr == cellidx]

        for cellidx in range(self.n_int):
            spiketimes_cells_int[cellidx] = self.spiketimes_int[self.spiketimes_cellidxs_int == cellidx]
        return spiketimes_cells_pyr, spiketimes_cells_int

    def get_spiketimes_cell(self, cellidx, celltype):
        if self.spiketimes_pyr is None:
            self.get_spiketimes()

        if celltype == 'pyr':
            spiketimes_cell = self.spiketimes_pyr[self.spiketimes_cellidxs_pyr == cellidx]
        elif celltype == 'int':
            spiketimes_cell = self.spiketimes_int[self.spiketimes_cellidxs_int == cellidx]
        else:
            raise ValueError('celltype must be pyr or int!')
        assert np.all(
            spiketimes_cell <= self.runtime)  # can be because simulation time is different to recording time
        return spiketimes_cell

    def get_populationrate(self):
        poprate_pyr = self.poprate_monitor_pyr.smooth_rate(window='gaussian', width=1 * ms) / Hz
        poprate_int = self.poprate_monitor_int.smooth_rate(window='gaussian', width=1 * ms) / Hz
        poprate_t = self.poprate_monitor_pyr.t / ms

        if self.onset != 0:
            poprate_pyr = poprate_pyr[self.onset_idx:]
            poprate_int = poprate_int[self.onset_idx:]
            poprate_t = poprate_t[self.onset_idx:] - self.onset
        return poprate_pyr, poprate_int, poprate_t