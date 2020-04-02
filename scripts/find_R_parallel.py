#!/usr/bin/env python

import numpy as np
import argparse
import CalculationUtils

parser = argparse.ArgumentParser(
        description = "Calculates the input impedance of a single stage amplifier design")

# parser.add_argument('-t', '--ampType', default = 'commonEmitter', choices = ["commonEmitter, cascode"],
#         help = "Type of amplifier used.")
parser.add_argument('-v', '--Vcc', default = 3.3, type = float,
        help = "The power supply voltage of the circuit.")
parser.add_argument('--Vbe', default = 0.76, type = float,
        help = "The base emitter voltage of the BJT")
parser.add_argument('-i', '--emitterCurrent',  default = 5e-3, type = float,
        help = "Target current flow in the emitter branch.")
parser.add_argument('-b', '--beta', default = 330, type = float,
        help = "Current amplification factor of the transistor")
parser.add_argument('--Cpi', default = 0.595e-12, type = float,
        help = "C_pi of the chosen transistor in the Hybrid Pi Model")
parser.add_argument('--Cmu', default = 0.147e-12, type = float,
        help = "C_mu of the chosen transistor in the Hybrid Pi Model")
parser.add_argument('--RC', default = 50, type = float,
        help = "Collector resistor value")
parser.add_argument('-z', '--targetImpedanceMagnitude', default = 50, type = float,
        help = "The magnitude of the desired input impedance")
args = parser.parse_args()

# Design Parameters
v_t = 27e-3
z_target = args.targetImpedanceMagnitude
V_BE = args.Vbe
V_CC = args.Vcc
I_E = args.emitterCurrent
c_pi = args.Cpi
c_mu = args.Cmu
f = (500e6+125e6)/2
omega = 2*np.pi*f
beta = args.beta
RC = args.RC
r_pi = beta * v_t / I_E
z_pi = -1j/(omega*c_pi)

# Calculate Miller impedance 
gain = RC * I_E/v_t
c_miller = c_mu * (1 + gain)

z_miller = -1j/(omega*c_miller)

# Calculate contributions from divider network and bjt
z_bjt = CalculationUtils.parallel(z_pi, r_pi)

z_ext = CalculationUtils.parallel(z_target, -z_bjt, -z_miller)

R_parallel_no_cap = CalculationUtils.magnitude(z_ext)

R_parallel_with_cap = z_ext.real
C_series = 1/(omega*z_ext.imag)

print('\n')
print('************************************************************\n')
print('The following is a first guess to achieve Z_in = ' + str(z_target) + ':')
print('\nWith no series capacitor:')
print('R1||R2 = ' + str(R_parallel_no_cap) + ' Ohms')
print('\nWith a series capacitor:')
print('R1||R2 = ' + str(R_parallel_with_cap) + ' Ohms')
print('C_series = ' + str(C_series*10**(12)) + ' pF')
print('\n************************************************************')
print('\n')
print('NOTE: This was a calculation for f = 312.5MHz')
print('NOTE: The calculation yielded Z_ext = ' + str(z_ext))
print()