#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
from astropy import constants as const
import pandas as pd

def P(sigma, M_A):
    e = 0               # Assuming non-eccentric orbits
    sini = 2/np.pi      # Assuming mean inclination
    M_B = M_A           # Assuming same mass for both stars
    K = sigma/0.707     # Assuming a Gaussian distribution
    P = 1/np.sqrt(1+e)**3 * ((const.M_sun.value*M_A)*sini)**3 / (const.M_sun.value*(M_A+M_B))**2 * (2*np.pi*const.G.value/K**3)
    return np.round(P/86400,2)
