#!/usr/bin/env python

import matplotlib.pyplot as plt
import numpy as np
import argparse, CalculationUtils

parser = argparse.ArgumentParser(
        description = "Calculates the input impedance of a single stage amplifier design")

# parser.add_argument('-t', '--ampType', default = 'commonEmitter', choices = ["commonEmitter, cascode"],
#         help = "Type of amplifier used.")
parser.add_argument('-v', '--Vcc', default = 3.3, type = float,
        help = "The power supply voltage of the circuit.")
parser.add_argument('--Vce', default = 1, type = float,
        help = "The desired collector-emitter voltage of the BJT. Ignored if RE provided")
parser.add_argument('-i', '--i_target',  default = 5e-3, type = float,
        help = "Target current flow in the emitter branch.")
parser.add_argument('--R1', default = 60.4, type = float, 
        help = "Top resistor in the divider at the input")
parser.add_argument('--R2', default = 357, type = float, 
        help = "Middle resistor in the divider at the input")
# parser.add_argument('--R3', default = 100, type = float, 
#         help = "Bottom resistor in the divider at the input")
parser.add_argument('--RE', default = argparse.SUPPRESS, type = float,
        help = "Emitter resistor value. Typically supressed. If value provided, Vce and Rc arguments ignored.")
parser.add_argument('--RC', default = 50, type = float,
        help = "Collector resistor value. Ignored if RE provided")
parser.add_argument('-d', '--incorporateTestData', action = 'store_true',
        help = "Call this option to incorporate data points from conducted tests into plots")
args = parser.parse_args()

### Design Parameters ###
I_E = args.i_target
Vcc = args.Vcc
R1 = args.R1
R2 = args.R2
R_parallel = CalculationUtils.parallel(R1, R2)
Vdiv = Vcc * R2 / (R1 + R2)

# determine R_E based on either provided value or from R_C and V_CE
if hasattr(args, 'RE'):
    RE = args.RE
else:
    Vce = args.Vce
    RC = args.RC

    RE = (Vcc - I_E*RC - Vce)/I_E

Vbe_test = np.array([0.771, 0.76, 0.758])
beta_test = np.array([325, 405, 409])
Vdiv_test = Vcc*R2 / (R1+R2)
I_test = (Vdiv_test - Vbe_test) / (R_parallel/beta_test + RE) * 10**3

### Plot Vbe Sensitivity ###
Vbe = np.linspace(0.5, 1.25, 1000, endpoint= True)
beta = np.linspace(100, 500, 5, endpoint = True)

plt.figure(figsize=(7,6))
for beta_val in beta:
    I = (Vdiv - Vbe) / (R_parallel/beta_val + RE) * 10**3
    plt.plot(Vbe, I, label = r'$\beta=$' + str(int(beta_val)))

if args.incorporateTestData: 
    plt.scatter(Vbe_test[0], I_test[0], label = 'Simulation')
    plt.scatter(Vbe_test[1], I_test[1], label = 'Outside Magnet')
    plt.scatter(Vbe_test[2], I_test[2], label = 'Inside Magnet')

plt.xlabel("Base-Emitter Voltage (V)")
plt.ylabel("Collector Current (mA)")
plt.title("Collector Current Sensitivity to Base-Emitter Voltage")
plt.legend(loc='lower left')

### Plot Beta Sensitivity ###
Vbe = np.linspace(0.5, 1, 6, endpoint= True)
beta = np.linspace(1, 500, 1000, endpoint = True)

plt.figure(figsize=(7,6))
for Vbe_val in Vbe:
    I = (Vdiv - Vbe_val) / (R_parallel/beta + RE) * 10**3
    plt.semilogx(beta, I, label = r'$V_{be}=$' + str(round(Vbe_val,1)))

if args.incorporateTestData: 
    plt.scatter(beta_test[0], I_test[0], label = 'Simulation')
    plt.scatter(beta_test[1], I_test[1], label = 'Outside Magnet')
    plt.scatter(beta_test[2], I_test[2], label = 'Inside Magnet')

plt.xlabel("BJT Current Amplification Factor (" + r'$\beta$' + ")")
plt.ylabel("Collector Current (mA)")
plt.title("Collector Current Sensitivity to BJT Current Amplification")
plt.legend(loc='lower right')

### Plot Percent Difference From Target Current Due to BJT Characteristics ###
Vbe = np.linspace(0.5, 1.25, 100, endpoint= True)
beta = np.logspace(0, 2.7, 100, endpoint = True)

I_per_error = np.empty([len(Vbe), len(beta)])
for i in range(len(Vbe)):
    for j in range((len(beta))):
        I = (Vdiv - Vbe[i]) / (R_parallel/beta[j] + RE)
        I_per_error[i][j] = (I - I_E) / I_E * 100

plt.figure(figsize=(7,6))
c = plt.pcolor(Vbe, beta, I_per_error.T)
plt.yscale('log')
plt.xlabel("Base-Emitter Voltage (V)")
plt.ylabel("BJT Current Amplification Factor (" + r'$\beta$' + ")")
plt.title("% Error in Collector Current Due to BJT Characteristics")
cbar = plt.colorbar(c)
cbar.set_label("% Error in Collector Current")

plt.show()
