#!/usr/bin/env python

import matplotlib.pyplot as plt
import numpy as np
import argparse
import CalculationUtils

parser = argparse.ArgumentParser(
        description = "Calculates the input impedance of a single stage amplifier design")

# parser.add_argument( '-t', '--ampType', default = 'commonEmitter', choices = ["commonEmitter, cascode"],
#         help = "Type of amplifier used.")
parser.add_argument( '-v', '--Vcc', default = 3.3, type = float,
        help = "The power supply voltage of the circuit.")
parser.add_argument( '--Vbe', default = 0.76, type = float,
        help = "The base emitter voltage of the BJT")
parser.add_argument('--Vce', default = 1, type = float,
        help = "The desired collector-emitter voltage of the BJT. Ignored if RE provided")
parser.add_argument( '-i', '--emitterCurrent',  default = 5e-3, type = float,
        help = "Target current flow in the emitter branch.")
parser.add_argument('--RE', default = argparse.SUPPRESS, type = float,
        help = "Emitter resistor value. Typically supressed. If value provided, Vce and Rc arguments ignored.")
parser.add_argument('--RC', default = 50, type = float,
        help = "Collector resistor value. Ignored if RE provided")
parser.add_argument('-r', '--rParallel', default = 50, type = float,
        help = "The impedance magnitude you wish to match to. Used as Bode Plot reference.")
args = parser.parse_args()

### CONSTANTS ###
I_E = args.emitterCurrent
Vcc = args.Vcc
RC = args.RC
Vce = args.Vce
Vbe = args.Vbe
R_parallel = args.rParallel

# determine R_E based on either provided value or from R_C and V_CE
if hasattr(args, 'RE'):
    RE = args.RE
    RE_given = True
else:
    Vce = args.Vce
    RC = args.RC

    RE = (Vcc - I_E*RC - Vce)/I_E
    RE_given = False

# rearranged from I_E = (Vdiv - Vbe) / RE
# Vdiv = Vcc * R2 / (R1 + R2)
# rearranging this gives R2 = ( Vdiv / (Vcc - Vdiv) )*R1 = a*R1
Vdiv = I_E * RE + Vbe
a = Vdiv / (Vcc - Vdiv)

# R_parallel = R1 * R2 / (R1 + R2)
# Plugging in R2 = a*R1 -> R1 = ( (a + 1) / a ) * R_parallel = b * R_parallel
b = (a + 1) / a
R1 = b * R_parallel
R2 = a * R1

print('\n')
print('************************************************************\n')
print('The resistor values for the circuit were calculated to be:')
print('R1 = ' + str(R1) + ' Ohms')
print('R2 = ' + str(R2) + ' Ohms')
print('RE = ' + str(RE) + ' Ohms')
print('\nThe calculation was done given the following design parameters:')
print('R1||R2 = ' + str(R_parallel) + ' Ohms')

if RE_given:
	print('R_E = ' + str(RE) + ' Ohms')
else: 
	print('R_C = ' + str(RC) + ' Ohms')
	print('V_ce = ' + str(Vce) + ' V')

print('V_cc = ' + str(Vcc) + ' V')
print('V_be = ' + str(Vbe) + ' V')
print('I_E = ' + str(I_E*10**3) + ' mA')
print('\n************************************************************\n')
