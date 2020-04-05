#!/usr/bin/env python

import matplotlib.pyplot as plt
import numpy as np
import argparse
import CalculationUtils

parser = argparse.ArgumentParser(
        description = "Calculates the input impedance of a single stage amplifier design")

parser.add_argument('-d', '--useCascode', action = 'store_true',
        help = "Flag to indicate which amplifier to use: Cascode if called, Common-Emitter otherwise")
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
parser.add_argument('--Cseries', default = np.inf, type = float,
	help = "Ability to insert a capacitor in series at the input and see its effects on the impedance")
parser.add_argument('-r', '--rParallel', default = 50, type = float,
        help = "The parallel combination of the input resistors")
parser.add_argument('--RC', default = 50, type = float,
        help = "Collector resistor value")
parser.add_argument('-z', '--targetImpedanceMagnitude', default = 50, type = float,
        help = "The impedance magnitude you wish to match to. Used as Bode Plot reference.")
args = parser.parse_args()

#### Design Parameters ###
v_t = 27e-3
z_target = args.targetImpedanceMagnitude
V_BE = args.Vbe
V_CC = args.Vcc
I_E = args.emitterCurrent
c_pi = args.Cpi
c_mu = args.Cmu
c_series = args.Cseries
f = np.linspace(125e6,500e6, 1000)
omega = 2*np.pi*f
beta = args.beta
RC = args.RC
r_e = v_t / I_E
r_pi = beta * r_e
z_pi = -1j/(omega*c_pi)
z_mu = -1j/(omega*c_mu)
R_in_eq = args.rParallel

# Calculate gain for Miller Capacitance depending on amplifier type
if args.useCascode:
	miller_gain = CalculationUtils.parallel(r_e, z_mu, z_pi) / CalculationUtils.parallel(r_e, z_mu)
	amp_type = "Cascode"
else:
	miller_gain = RC * I_E/v_t
	amp_type = "Common-Emitter"

# Calculate Miller impedance 
c_miller = c_mu * (1 + miller_gain)
z_miller = -1j/(omega*c_miller)

# find non-feedback contribution from BJT
z_bjt = CalculationUtils.parallel(z_pi, r_pi)

z_in = CalculationUtils.parallel(R_in_eq, z_bjt, z_miller)

z_in_mag = CalculationUtils.magnitude(z_in)
z_in_phase = CalculationUtils.phase(z_in)

print("Calculating for amplifier type: " + str(amp_type))

plt.figure()
plt.plot(f*1e-6, z_in_mag)
plt.xlabel("Frequency (Hz)")
plt.ylabel("Input Impedance Magnitude (" + r'$\Omega$' + ")")
plt.title("Amplifier Input Impedance Magnitude")

plt.figure()
plt.semilogx(f*1e-6, 20*np.log10(z_in_mag/z_target) )
plt.xlabel("Frequency (Hz)")
plt.ylabel("Input Impedance Magnitude (dB)")
plt.title("Impedance Bode Plot (Reference of " + str(round(z_target, 1)) + r'$\Omega$' + ")" )

plt.figure()
plt.plot(f*1e-6, z_in_phase*180/(2*np.pi))
plt.xlabel("Frequency (Hz)")
plt.ylabel("Input Impedance Phase (Degrees)")
plt.title("Amplifier Input Impedance Phase")

plt.figure()
plt.plot([c.real for c in z_in], [c.imag for c in z_in])
plt.xlabel("Re(" + r'$Z_{in}$' + ")")
plt.ylabel("Im(" + r'$Z_{in}$' + ")")
plt.xlim(-100, 100)
plt.ylim(-100, 100)
plt.title("Input Impedance in the Complex Plane")
plt.grid()

plt.show()