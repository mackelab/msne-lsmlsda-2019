import numpy as np
from scipy.special import factorial, gammaln
from scipy.optimize import minimize as scipy_minimize

def make_filter(lags, mu1=3., mu2=8., s1=1., s2=5., eta=.2):
    """Returns a filter constructed by a mixture of 2 Gaussians (N(range(lags) | mu1, s1) - eta * N(range(lags) | mu2, s2)).
    Parameters:
    lags : int. value. Length of filter to be constructed.
    mu1 : float value. Mean of first Gaussian.
    mu2 : float value. Mean of second Gaussian.
    s1 : float value. Std of first Gaussian.
    s2 : float value. Std of second Gaussian.
    eta : float value. Weight parameter for second Gaussian
    
    Returns:
    _filter : vector of float values of size 'lags'.
    """
    x = np.arange(lags)
    gauss1 = np.exp(- (x - mu1) ** 2 / (2 * s1**2))
    gauss2 = eta * np.exp(- (x - mu2) ** 2 / (2 * s2**2))
    _filter = gauss1 -  gauss2;
    _filter = _filter / np.linalg.norm(_filter)
    return _filter


def hankel(lags, _input):
    """Returns a Hankel matrix of size _input.size x lags
    Parameters:
    lags : int value. Number of input timebins in the past on which the response depends.
    _input : vector of float values. Input sequence to be converted in to a Hankel matrix.
    
    Returns:
    hank : matrix of float values of size '_input.size x lags'
    """
    
    _input_flat = _input.flatten()
    hank = np.zeros((len(_input_flat), lags))
    hank[:, 0] = _input_flat
    for lag in range(1, lags):
        hank[lag:, lag] = _input_flat[:-lag]
    return hank

    
def convolution(_filter, _input):
    """Returns the convolution product of the inputs.
    Parameters:
    _filter : vector of float values containing the convolutional filter.
    _input : int value. The input to be convolved with the filter.
    
    Returns:
    Vector of float values, of same shape as '_input'.
    """
    hank = hankel(len(_filter), _input)
    return np.dot(hank, _filter).reshape(_input.shape)

        
def cost(params, stimulus, response, dt):
    """Returns log likelihood of a linear-nonlinear Poisson model.
    Parameters:
    params : vector of floats containing parameters of model. Last element of vector should be the baseline offset.
    stimulus : vector / matrix of floats containing the input stimulus.
    response : vector / matrix of floats containing the responses of the neuron to the stimulus. Should be of same shape as the stimulus.
    dt : float value containing size of timebins in s.
    
    Returns:
    log_likelihood : float value.
    """
    _filter = params[:-1]
    baseline = params[-1]
    
    stimulus = stimulus.flatten()
    response = response.flatten()
    
    X = hankel(len(_filter), stimulus)
    z = X.dot(_filter) + baseline
    r = dt * np.exp(z)
    
    # One way to calculate log likelihood
#     likelihood = np.prod(r**response * np.exp(-r) / factorial(response))
#     log_likelihood = np.log(likelihood)
    
    # Another way to calculate log likelihood
    log_likelihood = np.sum((response * (z + no.log(dt))) - r - gammaln(response + 1))
    
    return log_likelihood
    
    
def nll(params, stimulus, response, dt):
    """Returns negative log likelihood of a linear-nonlinear Poisson model.
    Parameters:
    params : vector of floats containing parameters of model. Last element of vector should be the baseline offset.
    stimulus : vector / matrix of floats containing the input stimulus.
    response : vector / matrix of floats containing the responses of the neuron to the stimulus. Should be of same shape as the stimulus.
    dt : float value containing size of timebins in s.
    
    Returns:
    nll : float value.
    """
    return -cost(params, stimulus, response, dt)


def minimize(stimulus, response, stim_lags, dt):
    """Returns the ML estimate of the parameters of a linear-nonlinear Poisson model.
    Parameters:
    stimulus : vector / matrix of floats containing the input stimulus.
    response : vector / matrix of floats containing the responses of the neuron to the stimulus. Should be of same shape as the stimulus.
    dt : float value containing size of timebins in s.
    
    Returns:
    _filter : vector of floats. ML estimate of the convolutional filter.
    baseline : float value. ML estimate of the baseline offset. 
    """
    init = np.zeros(stim_lags + 1)
    params = scipy_minimize(nll, init, args=(stimulus, response, dt), jac=False).x
    return params[:-1], params[-1]
