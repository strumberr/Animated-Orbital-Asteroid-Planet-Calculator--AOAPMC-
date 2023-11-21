import numpy as np
from PyAstronomy import pyasl
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.animation import PillowWriter
from mpl_toolkits.mplot3d import Axes3D
import matplotlib

import json

import os
import pathlib
from datetime import date
import datetime
import os
import glob


writer = PillowWriter(fps=60)

asteroid_name = "Moon Orbit "

# Semi-major axis
a = 2.36
# Periapsis
per = 2.15
# Eccentricity 
e = 0.0894
# Longitude of ascending node 
omega = 103.71
# Inclination 
i = 7.1422
# Argument of periapsis/perifocus 
w = 151.66

# Moon orbit parameters
a_moon = 0.256955529
per_moon = 5.997
e_moon = 0.0554     # Eccentricity
i_moon = 5.16       # Inclination in degrees
omega_moon = 125.08 # Longitude of ascending node in degrees
w_moon = 318.15     # Argument of periapsis in degrees

# Create moon orbit
moon_orbit = pyasl.KeplerEllipse(a=float(a_moon), e=float(e_moon), per=float(per_moon), i=float(i_moon), Omega=float(omega_moon), w=float(w_moon))
t_moon = np.linspace(0, 4 * 48, 600)
pos_moon = moon_orbit.xyzPos(t_moon)


# t_moon_full = np.linspace(0, 4 * 12, 200 * 12)  # 12 times the points for 12 orbits
# t_moon = t_moon_full % 4  # Use modulo to repeat the moon's orbit
# pos_moon = moon_orbit.xyzPos(t_moon)

plt.style.use('dark_background')
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')


ax.set_facecolor('black')

ax.xaxis.set_pane_color((0.0, 0.0, 0.0, 1.0))
ax.yaxis.set_pane_color((0.0, 0.0, 0.0, 1.0))
ax.zaxis.set_pane_color((0.0, 0.0, 0.0, 1.0))

ax.xaxis._axinfo["grid"]['color'] =  (1,1,1,0)
ax.yaxis._axinfo["grid"]['color'] =  (1,1,1,0)
ax.zaxis._axinfo["grid"]['color'] =  (1,1,1,0)



# Earth orbit parameters
a2 = 1.00000011
e2 = 0.01671022
omega2 = 18.272
i2 = 0.00005
w2 = 85.901
per2 = a2 * (1 - e2)

# Create Earth orbit
orbit2 = pyasl.KeplerEllipse(a=float(a2), per=float(per2), e=float(e2), Omega=float(omega2), i=float(i2), w=float(w2))
t2 = np.linspace(0, 4, 600)
pos2 = orbit2.xyzPos(t2)


ax.scatter([0], [0], [0], color="yellow", s=100, label="Sun")  # Plotting the Sun as a point in 3D


pos_moon_relative = np.array([pos_moon[j] + pos2[j] for j in range(len(t_moon))])
ax.plot(pos_moon_relative[:, 1], pos_moon_relative[:, 0], 0, label="Moon Trajectory", color="white", linestyle="dotted", linewidth=1)


ax.plot(pos2[:, 1], pos2[:, 0], 0, label="Earth Trajectory", color="yellow", linestyle="dotted", linewidth=1)

# Scatter plot for Earth and Moon in 3D
red_dot2 = ax.scatter([pos2[0][1]], [pos2[0][0]], [0], color="blue", label="Earth")  # Earth
red_dot3 = ax.scatter([pos_moon_relative[0][1]], [pos_moon_relative[0][0]], [0], color="white", linestyle="dotted", label="Moon")  # Moon


def animate(i):
    # Update Earth and Moon positions
    red_dot2._offsets3d = (np.array([pos2[i][1]]), np.array([pos2[i][0]]), np.array([0]))  # Earth
    red_dot3._offsets3d = (np.array([pos_moon_relative[i][1]]), np.array([pos_moon_relative[i][0]]), np.array([0]))  # Moon
    fig.canvas.draw()
    return red_dot2, red_dot3


myAnimation = animation.FuncAnimation(fig, animate, interval=40, frames=np.arange(0, 600), blit=True, repeat=True)


ax.set_xlabel('X Axis')
ax.set_ylabel('Y Axis')
ax.set_zlabel('Z Axis')
plt.legend(loc="lower right", fontsize='xx-small')
plt.title(f'{asteroid_name} Orbital Simulation')


# myAnimation.save(f'{asteroid_name}-orbit.gif', writer=writer)


plt.show()