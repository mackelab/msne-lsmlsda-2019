import matplotlib.pyplot as plt
from gamma_oscillations.analyze import *


def plot_mem_pot(loaded_file, save_dir=None, filename='mem_pot.png'):
    vm_pyr, vm_int, t = loaded_file.get_vm()
    plt.figure()
    plt.plot(t, vm_pyr[0], label='Pyr.')
    plt.plot(t, vm_int[0], label='Int.')
    plt.ylabel('Mem. pot. (mV)')
    plt.xlabel('Time (ms)')
    plt.legend(loc='upper right')
    plt.xlim(0, loaded_file.runtime - loaded_file.onset)
    plt.tight_layout()
    if save_dir is not None:
        plt.savefig(os.path.join(save_dir, filename))


def plot_spikes(loaded_file, save_dir=None, filename='spikes.png'):
    spiketimes_cellidxs_pyr, spiketimes_cellidxs_int, spiketimes_pyr, spiketimes_int = loaded_file.get_spiketimes()
    plt.figure()
    plt.plot(spiketimes_pyr, spiketimes_cellidxs_pyr, 'o', markersize=1, label='Pyr.')
    plt.plot(spiketimes_int, spiketimes_cellidxs_int + loaded_file.n_pyr, 'o', markersize=1, label='Int.')
    plt.ylabel('Neuron index')
    plt.xlabel('Time (ms)')
    plt.xlim(0, loaded_file.runtime - loaded_file.onset)
    plt.ylim(0, loaded_file.n_pyr + loaded_file.n_int)
    plt.legend(loc='lower right')
    plt.tight_layout()
    if save_dir is not None:
        plt.savefig(os.path.join(save_dir, filename))


def plot_firing_rate(loaded_file, save_dir=None, filename='firingrate.png'):
    spiketimes_cells_pyr, spiketimes_cells_int = loaded_file.get_spiketimes_cells()
    len_rec = loaded_file.runtime
    firingrates_pyr = compute_firingrate_cells(spiketimes_cells_pyr, len_rec)
    firingrates_int = compute_firingrate_cells(spiketimes_cells_int, len_rec)
    plt.figure()
    plt.subplot(2, 1, 1)
    plt.title('Firing rate (Pyr.)')
    plt.hist(firingrates_pyr, bins=40, align='mid')
    plt.xlabel('Firing rate (Hz)')
    plt.ylabel('Count')
    plt.subplot(2, 1, 2)
    plt.title('Firing rate (Int.)')
    plt.hist(firingrates_int, bins=40, align='mid')
    plt.xlabel('Firing rate (Hz)')
    plt.ylabel('Count')
    plt.tight_layout()
    if save_dir is not None:
        plt.savefig(os.path.join(save_dir, filename))


def plot_spectrum(loaded_file, save_dir=None, filename='spectrum.png'):
    poprate_pyr, poprate_int, poprate_t = loaded_file.get_populationrate()
    dt = poprate_t[1] - poprate_t[0]
    poprate_zm_pyr = poprate_pyr - np.mean(poprate_pyr)
    poprate_zm_int = poprate_int - np.mean(poprate_int)
    freq_vect, power_pyr = compute_spectrum_multitaper(poprate_zm_pyr, dt)
    _, power_int = compute_spectrum_multitaper(poprate_zm_int, dt)
    plt.figure()
    plt.subplot(2, 1, 1)
    plt.title('Spectrum (Pyr.)')
    plt.plot(freq_vect, power_pyr)
    plt.xlim(0, 300)
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Power')
    plt.subplot(2, 1, 2)
    plt.title('Spectrum (Int.)')
    plt.plot(freq_vect, power_int)
    plt.xlim(0, 300)
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Power')
    plt.tight_layout()
    if save_dir is not None:
        plt.savefig(os.path.join(save_dir, filename))