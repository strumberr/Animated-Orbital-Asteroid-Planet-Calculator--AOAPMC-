import numpy as np
from PyAstronomy import pyasl
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.animation import PillowWriter
import matplotlib

import json

import os
import pathlib
from datetime import date
import datetime
import os
import glob





asteroid_name = "testingAsteroid"

writer = PillowWriter(fps=30)

#semi-major axis
a = 2.279410092590412
#periapsis
per = 2.066719172674827
#eccentricity
e = 9.330963331564170
#longitude of ascending node
omega = 4.949015080264508
#inclination
i = 1.847884265058486
#argument of periapsis/perifocus
w = 2.866508600402408
print(a)
print(per)
print(e)
print(omega)
print(i)
print(w)

orbit = pyasl.KeplerEllipse(a=float(a), per=float(per), e=float(e), Omega=float(omega), i=float(i), w=float(w))

t = np.linspace(0, 4, 350)
pos = orbit.xyzPos(t)

plt.style.use('dark_background')
fig, ax = plt.subplots()
l = plt.plot(pos[::,1], pos[::,0], 'k-')

#----------------------------

#define y-unit to x-unit ratio
ratio = 1.0
fig, ax = plt.subplots()

#get x and y limits
x_left, x_right = ax.get_xlim()
y_low, y_high = ax.get_ylim()

#set aspect ratio
ax.set_aspect(abs((x_right-x_left)/(y_low-y_high))*ratio)
ax.set_facecolor('xkcd:black')

a2 = 1.00000011
e2 = 0.01671022
omega2 = 18.272
i2 = 0.00005
w2 = 85.901

per2 = a2 * (1-e2)


orbit2 = pyasl.KeplerEllipse(a=float(a2), per=float(per2), e=float(e2), Omega=float(omega2), i=float(i2), w=float(w2))
t2 = np.linspace(0, 4, 200)

pos2 = orbit2.xyzPos(t2)


plt.plot(pos2[::, 1], pos2[::, 0], 'k-', label="Earth Trajectory", color="yellow", linewidth=1)
plt.plot(pos2[0, 1], pos2[0, 0], 'r*', label="Earth Periapsis", color="blue", linewidth=1)

plt.plot(0, 0, 'bo', markersize=9, label="Sun", color="yellow", linewidth=1)
plt.plot(pos[::, 1], pos[::, 0], 'k-', label="Celestial Object Trajectory", color="orange", linestyle="dotted", linewidth=1)
#plot the moon trajectory relative to the earth trajectory

plt.plot(pos[0, 1], pos[0, 0], 'r*', label="Celestial Object Periapsis", color="gray", linewidth=1)


plt.grid(linewidth = 0.2)

print("-----------------------Checkpoint1--------------------------")

#----------------------------


red_dot, = plt.plot(pos[0][1], pos[0][0], 'bo', color="gray")

red_dot2, = plt.plot(pos2[0][1], pos2[0][0], 'bo', color="blue")


ln, = plt.plot([], [], 'bo-', animated=True, color="#fe28a2", linewidth = 0.6)

ln2, = plt.plot([], [], 'bo-', animated=True, color="#00b2ee", linewidth = 0.6)

ln3, = plt.plot([], [], 'bo-', animated=True, color="#bcbcbc", linewidth = 0.6)


def animate(i):
    
    red_dot.set_data(pos[i][1], pos[i][0])
    red_dot2.set_data(pos2[i][1], pos2[i][0])

    ln.set_data([pos[i][1], pos2[i][1]], [pos[i][0], pos2[i][0]])

    ln2.set_data([0, pos2[i][1]], [0, pos2[i][0]])

    ln3.set_data([0, pos[i][1]], [0, pos[i][0]])

    return ln, ln2, red_dot, red_dot2,


# create animation using the animate() function
myAnimation = animation.FuncAnimation(fig, animate, 

                    frames=np.arange(0, len(t), 1), interval=40,

                    blit=True, repeat=True)


plt.tick_params(
    axis='both', 
    which='both', 
    bottom=True, 
    top=False, 
    labelbottom=True,  
    left=True,
    labelleft=True)

plt.legend(loc="lower right", fontsize='xx-small')

plt.title(f'{asteroid_name} Orbital Simulation')



print("-----------------------Checkpoint2--------------------------")
try:
    myAnimation.save(f'animated_{asteroid_name}.gif', writer=writer)
except:
    pass
print("-----------------------Checkpoint3--------------------------")