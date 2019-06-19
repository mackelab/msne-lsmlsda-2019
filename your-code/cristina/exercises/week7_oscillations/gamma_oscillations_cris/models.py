from brian2 import *


class SynapseModel:

    def __init__(self, name, v, g_max, rise, decay, E, delay):
        self.name = name
        self.v = v
        self.g_max = g_max * nsiemens
        self.rise = rise * ms
        self.decay = decay * ms
        self.E = E * mV
        self.delay = delay * ms

    def get_eqs(self):
        return '''
               I_{name} = g_max_{name} * g_{name} * ({v} - E_{name}) : amp
               dg_{name}/dt = act_{name}/ms - g_{name} / decay_{name} : 1
               dact_{name}/dt = -act_{name} / rise_{name} : 1
               '''.format(name=self.name, v=self.v)

    def get_eqs_on_pre(self):
        return '''
               act_{name} += 1
               '''.format(name=self.name)

    def get_params(self):
        return {
            'g_max_{name}'.format(name=self.name): self.g_max,
            'rise_{name}'.format(name=self.name): self.rise,
            'decay_{name}'.format(name=self.name): self.decay,
            'E_{name}'.format(name=self.name): self.E
        }


def get_eqs_pyr():
    return '''
            dv/dt = (-I_Leak_s -I_Na_s -I_K_s -I_sd -I_GABA) / c : volt
            dv_d/dt = (-I_Leak_d -I_Ca_d -I_AHP -I_ds -I_AMPA -I_AMPA_ext) / c : volt
        
            I_Leak_s = g_Leak * (v - E_Leak) : amp
            I_Na_s = g_Na * m_inf**3 * h * (v - E_Na) : amp
            I_K_s = g_K * n**4 * (v - E_K) : amp
            I_sd = (g_coupling / p) * (v - v_d) : amp
            I_Leak_d = g_Leak * (v_d - E_Leak) : amp
            I_Ca_d = g_Ca * r**2 * (v_d - E_Ca) : amp
            I_AHP = g_AHP * (C_Ca/(C_Ca+Kd)) * (v_d - E_K) : amp
            I_ds = g_coupling / (1.0 - p) * (v_d - v) : amp
        
            r = 1 / (1 + exp(-(v_d/mV + 20) / 9.0)) : 1
            dC_Ca/dt = -4 * (umolar/(ms*uamp)) * I_Ca_d - C_Ca/tau_Ca : mmolar
            m_inf = alpha_m / (alpha_m + beta_m) : 1
            dn/dt = 4 * (alpha_n * (1-n) - beta_n * n) : 1
            dh/dt = 4 * (alpha_h * (1-h) - beta_h * h) : 1
        
            alpha_m = -0.1 * (v/mV + 33) / (exp(-(v/mV + 33) / 10) - 1) /ms : Hz
            beta_m = 4 * exp(-(v/mV + 58) / 12) /ms : Hz
            alpha_h = 0.07 * exp(-(v/mV + 50) / 10) /ms : Hz
            beta_h = 1 / (exp(-(v/mV + 20) / 10) + 1) /ms : Hz
            alpha_n = -0.01 * (v/mV + 34) / (exp(-(v/mV + 34) / 10) - 1) /ms : Hz
            beta_n = 0.125 * exp(-(v/mV + 44) / 25) /ms : Hz                                       
            '''


def get_params_pyr():
    return {
            'c': 0.25 *nfarad,
            'g_coupling': 0.5 * usiemens,
            'g_Na': 11.25 * usiemens,
            'g_K': 4.5 * usiemens,
            'g_Ca': 0.25 * usiemens,
            'g_Leak': 0.025 * usiemens,
            'g_AHP': 1.25 * usiemens,
            'E_Na': 55. * mV,
            'E_K': -80. * mV,
            'E_Ca': 120. * mV,
            'E_Leak': -65. * mV,
            'Kd': 30. * umolar,
            'p': 0.5,
            'tau_Ca': 80 *ms
            }


def get_eqs_int():
    return '''
            dv/dt = (-I_Leak -I_Na -I_K -I_AMPA -I_GABA -I_AMPA_ext) / c : volt
    
            I_Leak = g_Leak * (v - E_Leak) : amp
            I_Na = g_Na * m_inf**3 * h * (v - E_Na) : amp
            I_K = g_K * n**4 * (v - E_K) : amp
    
            m_inf = alpha_m / (alpha_m + beta_m) : 1
            dn/dt = 5 * (alpha_n * (1-n) - beta_n * n) : 1
            dh/dt = 5 * (alpha_h * (1-h) - beta_h * h) : 1
    
            alpha_m = -0.1 * (v/mV + 35) / (exp(-(v/mV + 35) / 10) - 1) /ms : Hz
            beta_m = 4 * exp(-(v/mV + 60) / 18) /ms : Hz
            alpha_h = 0.07 * exp(-0.05 * (v/mV + 58)) /ms : Hz
            beta_h = 1 / (exp(-(v/mV + 28) / 10) + 1) /ms : Hz
            alpha_n = -0.01 * (v/mV + 34) / (exp(-0.1 * (v/mV + 34)) - 1) /ms : Hz
            beta_n = 0.125 * exp(-(v/mV + 44) / 80) /ms : Hz
            '''

def get_params_int():
    return {
            'c': 0.2 * nfarad,
            'g_Na': 14.0 * usiemens,
            'g_K': 1.8 * usiemens,
            'g_Leak': 0.02 * usiemens,
            'E_Na': 55. * mV,
            'E_K': -90. * mV,
            'E_Leak': -67. * mV
            }