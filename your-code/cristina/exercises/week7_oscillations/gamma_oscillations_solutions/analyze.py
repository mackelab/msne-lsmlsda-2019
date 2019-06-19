from spectrum import pmtm
from spectrum.tools import nextpow2
from brian2 import *
import itertools


def spiketrain_from_spiketimes(spiketimes, runtime, dt):
    time_bins = np.arange(0, runtime+dt+dt, dt)  # one longer because of bins
    spiketrain, _ = np.histogram(spiketimes, time_bins)
    return spiketrain


def compute_synchfreq(freq_vect, power):
    return freq_vect[np.argmax(power)]


def compute_firingrate(spiketimes_cell, len_rec):
    return len(spiketimes_cell) / (len_rec/1000.)


def compute_firingrate_cells(spiketimes_cells, len_rec):
    firingrates = np.zeros(len(spiketimes_cells))
    for cellidx in range(len(spiketimes_cells)):
        firingrates[cellidx] = compute_firingrate(spiketimes_cells[cellidx], len_rec)
    return firingrates


def compute_spectrum_multitaper(x, dt, max_freq=300, NFFT=None):
    fs = 1. / (dt / 1000.)
    fmax = fs / 2.
    len_x = len(x)
    if NFFT is None:
        NFFT = 2 ** nextpow2(len_x)  # fft more efficient if power of 2
    freq_vec = np.linspace(0, fmax, NFFT / 2)
    a = pmtm(x, NFFT=NFFT, NW=2.5, method='eigen', show=False)
    power_pyr = np.mean(abs(a[0]) ** 2 * a[1], axis=0)[:int(NFFT / 2)] / len_x

    if max_freq is not None:
        freq_vec = freq_vec[np.where(freq_vec <= max_freq)]
        power_pyr = power_pyr[np.where(freq_vec <= max_freq)]
    return freq_vec, power_pyr


def compute_spectrogram_multitaper(x, dt, step_size=1, window_size=2**13, NW=2.5, freq_max=None, freq_min=None):
    fs = 1. / (dt / 1000.)
    fmax = fs / 2.
    len_x = len(x)
    NFFT = 2**nextpow2(len_x)  # fft more efficient if power of 2

    if NFFT is None:
        NFFT = window_size * 2

    assert len_x > window_size
    n_segs = int(np.floor(len_x / float(step_size))) + 1
    freq_vec = np.linspace(0, fmax, NFFT / 2)
    time_vec = np.arange(n_segs) * dt * step_size  # midpoint of respective window
    window_size_half = int(np.floor(window_size/2.))
    x = np.pad(x, window_size_half, mode='reflect')

    spectrogram = np.zeros((len(freq_vec), n_segs))
    for i in range(n_segs):
        x_window = x[i*step_size:i*step_size + window_size]  # symmetric
        x_window -= np.mean(x_window)
        a = pmtm(x_window, NFFT=NFFT, NW=NW, method='eigen', show=False)
        power_window = np.mean(abs(a[0]) ** 2 * a[1], axis=0)[:int(NFFT / 2)] / window_size
        spectrogram[:, i] = power_window

    if freq_max is not None:
        spectrogram = spectrogram[np.where(freq_vec <= freq_max)[0], :]
        freq_vec = freq_vec[np.where(freq_vec <= freq_max)]

    if freq_min is not None:
        spectrogram = spectrogram[np.where(freq_vec > freq_min)[0], :]
        freq_vec = freq_vec[np.where(freq_vec > freq_min)]

    return spectrogram, freq_vec, time_vec


def coherence_index(spiketrain1, spiketrain2):
    return np.sum(spiketrain1 * spiketrain2) / np.sqrt(np.sum(spiketrain1)*np.sum(spiketrain2))


def coherence_index_pop(spiketrains):
    coherence_indices = []
    for i, j in itertools.combinations(range(len(spiketrains)), r=2):
        coherence_indices.append(coherence_index(spiketrains[i], spiketrains[j]))
    return np.mean(coherence_indices)