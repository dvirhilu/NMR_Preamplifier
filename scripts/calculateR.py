#!/usr/bin/env python

import matplotlib.pyplot as plt
import numpy as np
import argparse
import CalculationUtils

parser = argparse.ArgumentParser(
        description = "Calculates the input impedance of a single stage amplifier design")

parser.add_argument( '-t', '--ampType', default = 'commonEmitter', choices = ["commonEmitter, cascode"],
        help = "Type of amplifier used.")
parser.add_argument( '-v', '--Vcc', default = 3.3, type = float,
        help = "The power supply voltage of the circuit.")
parser.add_argument( '--Vbe', default = 0.76, type = float,
        help = "The base emitter voltage of the BJT")
parser.add_argument( '-i', '--emitterCurrent',  default = 5e-3, type = float,
        help = "Target current flow in the emitter branch.")
parser.add_argument( '-c', '--C_pi', default = 0.595e-12, type = float,
        help = "C_pi of the chosen transistor in the Hybrid Pi Model")
parser.add_argument( '-b', '--beta', default = 330, type = float,
        help = "Current amplification factor of the transistor")
parser.add_argument('--R1', default = 127, type = float, 
        help = "Top resistor in the divider at the input")
parser.add_argument('--R2', default = 750, type = float, 
        help = "Middle resistor in the divider at the input")
parser.add_argument('--R3', default = 100, type = float, 
        help = "Bottom resistor in the divider at the input")
parser.add_argument('--RE', default = 412, type = float, 
        help = "Emitter resistor value")
parser.add_argument('-z', '--targetImpedanceMagnitude', default = 50, type = float,
        help = "The impedance magnitude you wish to match to. Used as Bode Plot reference.")
args = parser.parse_args()

### CONSTANTS ###
I_E = args.emitterCurrent
V_cc = args.Vcc
R_C = 100
V_CE = 0.85
V_BE = args.Vbe
beta = args.beta

### Calculate Circuit Parameters ###
V_C = V_cc - I_E*R_C
R_E = (V_C-V_CE)/I_E
desired_parallel_combination = 50
V_1 = I_E*R_E + V_BE


a = V_1/(V_cc - V_1)
R_b1 = (a+1)/a * desired_parallel_combination
R_b2 = a*R_b1
R_B_TH = R_b1*R_b2/(R_b1+R_b2)
print("for V_BE = " + str(V_BE) + ", The following parameters were attained: ")
print("R_E = " + str(R_E) + ", R_b1 = " + str(R_b1) + ", R_b2 = " + 
        str(R_b2) + ", R_bTH = " + str(R_B_TH))

I = (V_1 - V_BE) / (R_B_TH/beta + R_E) * 1000

# plt.figure()
# plt.plot(beta, I, label = "V_BE=" + str(V_BE) + "V")
# plt.xlabel("BJT Current Gain")
# plt.ylabel("Collector Current (mA)")
# plt.title("Collector Current Sensitivity to Transistor Characteristics")
# plt.legend()
# plt.show()
