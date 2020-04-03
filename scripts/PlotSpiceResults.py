#!/usr/bin/env python

import numpy as np
import csv
import matplotlib.pyplot as plt

f = open('bodePlot.csv')
csv_f = csv.reader(f)
f = []
g = []
phi = []
for row in csv_f:
    try:
        f.append(float(row[0])/1e6)
        g.append(float(row[1]))
        deg = float(row[2])
        if deg < 0 :
            phi.append(deg)
        else:
            phi.append(deg-360)
    except:
        raise ValueError("rip")

# f2 = open('timeDomain.csv')
# csv_f2 = csv.reader(f2)
# t = []
# v = []
# for row in csv_f2:
#     try:
#         t.append(float(row[0])*1e9)
#         v.append(float(row[1])*1e6)
#     except:
#         raise ValueError("rip")


fig, ax1 = plt.subplots()

color = 'tab:red'
ax1.set_xlabel('Frequency (MHz)')
ax1.set_ylabel('Gain Magnitude (dB)', color=color)
# ax1.set_ylabel('Gain Magnitude (dB)')
ax1.semilogx(f, g, color = color)
ax1.plot(np.ones(100)*125, np.linspace(min(g),19.328,100), '--' , label = '125MHz', color = 'black')
ax1.plot(np.ones(100)*500, np.linspace(min(g),19.328,100), '--', label = '500MHz', color = 'green')
ax1.plot(np.linspace(min(f), max(f), 100), np.ones(100)*19.328, '--', label = 'Calculated Gain', color = 'orange')
ax1.tick_params(axis='y', labelcolor = color)
ax1.title.set_text("Simulated Amplifier Open Circuit Gain")
ax1.legend()

ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

color = 'tab:blue'
ax2.set_ylabel('Gain Phase (degrees)', color=color)  # we already handled the x-label with ax1
ax2.semilogx(f, phi, color=color)
ax2.tick_params(axis='y', labelcolor=color)

fig.tight_layout()  # otherwise the right y-label is slightly clipped

# plt.figure()
# plt.xlabel('Time (ns)')
# plt.ylabel('Output Voltage ' + r'$(\mu V)$')
# plt.plot(t, v)
# plt.title("Time Domain Output Voltage Signal")
plt.show()
