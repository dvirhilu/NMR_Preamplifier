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
        raise ValueError("CSV file not formatted correctly RIP")

fig, ax1 = plt.subplots(figsize=(8,5))

color = 'tab:red'
ax1.set_xlabel('Frequency (MHz)')
ax1.set_ylabel('Gain Magnitude (dB)', color=color)
ax1.semilogx(f, g, color = color)
ax1.tick_params(axis='y', labelcolor = color)
ax1.title.set_text("Simulated Amplifier Open Circuit Gain")

ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

color = 'tab:blue'
ax2.set_ylabel('Gain Phase (degrees)', color=color)  # we already handled the x-label with ax1
ax2.semilogx(f, phi, color=color)
ax2.tick_params(axis='y', labelcolor=color)

fig.tight_layout()  # otherwise the right y-label is slightly clipped

# plt.savefig('LTspice_CE_sim.png', dpi=600)
plt.show()
