#!/usr/bin/env python

import matplotlib.pyplot as plt
import numpy as np
import argparse
import CalculationUtils

parser = argparse.ArgumentParser(
        description = "Calculates the gain of a single stage amplifier design")

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
parser.add_argument('--RC', default = 50, type = float,
        help = "Collector resistor value")
args = parser.parse_args()

#### Design Parameters ###
v_t = 27e-3
V_BE = args.Vbe
V_CC = args.Vcc
I_E = args.emitterCurrent
c_pi = args.Cpi
c_mu = args.Cmu
f = np.linspace(125e6,500e6, 1000)
omega = 2*np.pi*f
beta = args.beta
RC = args.RC
g_m = I_E / v_t
r_e = 1 / g_m
z_pi = -1j/(omega*c_pi)
z_mu = -1j/(omega*c_mu)

g_1 = g_m - 1 / z_mu
z_3 = CalculationUtils.parallel(RC, z_mu)

if args.useCascode:
    z_2 = CalculationUtils.parallel(z_mu, z_pi, beta*r_e)
    g_2 = g_m + 1/z_2
    gain = z_3 * g_1 * g_m / g_2
    amp_type = "Cascode"
    print(z_3[0], z_2[0], g_1[0], g_m)
else:
    gain = z_3 * g_1
    amp_type = "Common-Emitter"

gain_mag = CalculationUtils.magnitude(gain)
gain_phase = CalculationUtils.phase(gain)
print(gain_mag[0])

plt.figure()
plt.semilogx(f*1e-6, 20*np.log10(gain_mag) )
plt.xlabel("Frequency (Hz)")
plt.ylabel("Gain Magnitude (dB)")
plt.title("Gain Bode Plot" )

plt.figure()
plt.plot(f*1e-6, gain_phase*180/(2*np.pi))
plt.xlabel("Frequency (Hz)")
plt.ylabel("Gain Phase (Degrees)")
plt.title("Gain Phase Plot")

# plt.figure()
# plt.plot([c.real for c in gain], [c.imag for c in gain])
# plt.xlabel("Re(" + r'$Z_{in}$' + ")")
# plt.ylabel("Im(" + r'$Z_{in}$' + ")")
# plt.xlim(-100, 100)
# plt.ylim(-100, 100)
# plt.title("Gain in the Complex Plane")
# plt.grid()

plt.show()