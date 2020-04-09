#!/usr/bin/env python

import matplotlib.pyplot as plt
import numpy as np
import argparse, CalculationUtils

parser = argparse.ArgumentParser(
        description = "Plots amplifier sensitivity to changes in BJT properties")

parser.add_argument('-d', '--useCascode', action = 'store_true',
        help = "Flag to indicate which amplifier to use: Cascode if called, Common-Emitter otherwise")
parser.add_argument('-v', '--Vcc', default = 3.3, type = float,
        help = "The power supply voltage of the circuit.")
parser.add_argument('-i', '--i_target',  default = 5e-3, type = float,
        help = "Target current flow in the emitter branch.")
parser.add_argument('--R1', default = 60.4, type = float, 
        help = "Top resistor in the divider network for common-emitter, middle resistor for cascode")
parser.add_argument('--R2', default = 357, type = float, 
        help = "Bottom resistor in the divider at the input")
parser.add_argument('--R3', default = 13, type = float, 
        help = "Top resistor in the divider at the input of a cascode")
parser.add_argument('--RE', default = 412, type = float,
        help = "Emitter resistor value")
args = parser.parse_args()

### Design Parameters ###
I_E = args.i_target
Vcc = args.Vcc
R1 = args.R1
R2 = args.R2
R3 = args.R3
RE = args.RE

def get_I_E_cascode(Vbe, beta, Vcc, R1, R2, R3, RE):
        Vdiv = Vcc * R2 / (R1 + R2 + R3)
        Rbott = R2 * (2*R3 + R1) / (R1 + R2 + R3)

        return (Vdiv - Vbe) / (Rbott / beta + RE) 

def get_I_E_CE(Vbe, beta, Vcc, R1, R2, RE):
        Vdiv = Vcc * R2 / (R1 + R2)
        Rbott = CalculationUtils.parallel(R1, R2)

        return (Vdiv - Vbe) / (Rbott / beta + RE) 

### Plot Vbe Sensitivity ###
Vbe = np.linspace(0.5, 1.25, 1000, endpoint= True)
beta = np.linspace(100, 500, 5, endpoint = True)

plt.figure(figsize=(7,6))
for beta_val in beta:
	if args.useCascode:
		I = get_I_E_cascode(Vbe=Vbe, beta=beta_val, Vcc=Vcc, R1=R1, R2=R2, R3=R3, RE=RE)
	else:
		I = get_I_E_CE(Vbe=Vbe, beta=beta_val, Vcc=Vcc, R1=R1, R2=R2, RE=RE)
	
	plt.plot(Vbe, I, label = r'$\beta=$' + str(int(beta_val)))

plt.xlabel("Base-Emitter Voltage (V)")
plt.ylabel("Collector Current (mA)")
plt.title("Collector Current Sensitivity to Base-Emitter Voltage")
plt.legend(loc='lower left')

### Plot Beta Sensitivity ###
Vbe = np.linspace(0.5, 1, 6, endpoint= True)
beta = np.linspace(1, 500, 1000, endpoint = True)

plt.figure(figsize=(7,6))
for Vbe_val in Vbe:
	if args.useCascode:
		I = get_I_E_cascode(Vbe=Vbe_val, beta=beta, Vcc=Vcc, R1=R1, R2=R2, R3=R3, RE=RE)
	else:
		I = get_I_E_CE(Vbe=Vbe_val, beta=beta, Vcc=Vcc, R1=R1, R2=R2, RE=RE)
	
	plt.semilogx(beta, I, label = r'$V_{be}=$' + str(round(Vbe_val,1)))

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
		if args.useCascode:
			I = get_I_E_cascode(Vbe=Vbe[i], beta=beta[j], Vcc=Vcc, R1=R1, R2=R2, R3=R3, RE=RE)
		else:
			I = get_I_E_CE(Vbe=Vbe[i], beta=beta[j], Vcc=Vcc, R1=R1, R2=R2, RE=RE)
		
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
