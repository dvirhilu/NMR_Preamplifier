#!/usr/bin/env python

import matplotlib.pyplot as plt
import numpy as np
import argparse
import CalculationUtils

parser = argparse.ArgumentParser(
        description = "Calculates the resistor values for a single stage amplifier design given a set of parameters")

parser.add_argument('-d', '--useCascode', action = 'store_true',
        help = "Flag to indicate which amplifier to use: Cascode if called, Common-Emitter otherwise")
parser.add_argument( '-v', '--Vcc', default = 3.3, type = float,
        help = "The power supply voltage of the circuit.")
parser.add_argument( '--Vbe', default = 0.76, type = float,
        help = "The base emitter voltage of the BJT")
parser.add_argument('--Vce1', default = 1, type = float,
        help = "The desired collector-emitter voltage of the BJT. V_CE for Q1 if cascode. Ignored if RE provided")
parser.add_argument('--Vce2', default = 0.5, type = float,
		help = "The desiered collector-emitter voltage for Q2 in a cascode amplifier. Ignored if RE provided or common-emitter")
parser.add_argument( '-i', '--emitterCurrent',  default = 5e-3, type = float,
        help = "Target current flow in the emitter branch.")
parser.add_argument('--RE', default = argparse.SUPPRESS, type = float,
        help = "Emitter resistor value. Typically supressed. If value provided, Vce and Rc arguments ignored.")
parser.add_argument('--RC', default = 50, type = float,
        help = "Collector resistor value. Ignored if RE provided")
parser.add_argument('-r', '--rParallel', default = 50, type = float,
        help = "The impedance magnitude you wish to match to. Used as Bode Plot reference.")
parser.add_argument('-m', '--maximum_r_parallel', action = 'store_true',
        help = "If this option is specified, ignores r_parallel and uses r_parallel=R_E." )
args = parser.parse_args()

### CONSTANTS ###
I_E = args.emitterCurrent
Vcc = args.Vcc
RC = args.RC
Vce1 = args.Vce1
Vce2 = args.Vce2
Vbe = args.Vbe

def find_R_vals_common_emitter(I_E, RE, Vbe, Vcc, R_parallel):
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

	return (R1, R2)

def find_R_vals_cascode(I_E, RE, Vbe, Vcc, Vce2, R_parallel):
	# Assuming that the effects of beta are negligible:
	# Current through all three resistors is identical so
	# V_R3/R3 = V_R2/R2 = V_R1/R1
	# let a = V_R1/V_R3 = (V1-V2) / (Vcc - V1)
	# let b = V_R2/V_R3 = V2 / (Vcc - V1)
	# Then R1 = aR3, R2 = bR3

	V1 = I_E*RE + Vce2 + Vbe
	V2 = I_E*RE + Vbe

	a = (V1 - V2) / (Vcc - V1)
	b = V2 / (Vcc - V1)

	if args.maximum_r_parallel:
		# Plugging equations above into RE = (R2 * (2R3 + R1)) / (R1 + R2 + R3)
		# Rearranging for R3
		R3 = (a + b + 1) / (2*b + a*b) * RE
	else:
		# Plugging the equations above into R_parallel = R1||R2
		# Rearranging for R3
		R3 = (a + b) / (a * b) * R_parallel
		
	R1 = a * R3
	R2 = b * R3
	
	return (R1,R2,R3)

# determine R_E based on either provided value or from R_C and V_CE
if hasattr(args, 'RE'):
    RE = args.RE
    RE_given = True
else:
	RC = args.RC
	if args.useCascode:
		Vce1 = args.Vce1
		Vce2 = args.Vce2
		RE = (Vcc - I_E*RC - Vce1 - Vce2)/I_E

	else:
		Vce = args.Vce1
		RE = (Vcc - I_E*RC - Vce1)/I_E
		
	RE_given = False

if args.maximum_r_parallel:
	R_parallel = RE
else:
	R_parallel = args.rParallel

if args.useCascode:
	(R1, R2, R3) = find_R_vals_cascode(I_E=I_E, RE=RE, Vbe=Vbe, Vcc=Vcc, Vce2=Vce2, R_parallel=R_parallel)
else:
	(R1, R2) = find_R_vals_common_emitter(I_E=I_E, RE=RE, Vbe=Vbe, Vcc=Vcc, R_parallel=R_parallel)

if R_parallel > RE:
	raise ValueError("Invalid parameters: design violates inequality R1||R2 <= RE\n" + 
						"RE = " + str(RE) + "\nR1||R2 = " + str(R_parallel))

print('\n')
print('************************************************************\n')
print('The resistor values for the circuit were calculated to be:')
print('R1 = ' + str(R1) + ' Ohms')
print('R2 = ' + str(R2) + ' Ohms')

if args.useCascode:
	print('R3 = ' + str(R3) + ' Ohms')

print('RE = ' + str(RE) + ' Ohms')
print('\nThe calculation was done given the following design parameters:')

if args.maximum_r_parallel:
	print('R1||R2 = maximum value')
else:
	print('R1||R2 = ' + str(R_parallel) + ' Ohms')

if RE_given:
	print('R_E = ' + str(RE) + ' Ohms')
else: 
	if args.useCascode:
		print('R_C = ' + str(RC) + ' Ohms')
		print('V_ce1 = ' + str(Vce1) + ' V')
		print('V_ce2 = ' + str(Vce2) + ' V')
	else:
		print('R_C = ' + str(RC) + ' Ohms')
		print('V_ce = ' + str(Vce1) + ' V')

print('V_cc = ' + str(Vcc) + ' V')
print('V_be = ' + str(Vbe) + ' V')
print('I_E = ' + str(I_E*10**3) + ' mA')
print('\n************************************************************\n')
