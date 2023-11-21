import numpy as np
from PyAstronomy import pyasl
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.animation import PillowWriter
from mpl_toolkits.mplot3d import Axes3D

from datetime import date
import csv


writer = PillowWriter(fps=60)

asteroid_name = "Moon Orbit "

file_name = 'Planetary-Satellite-Data.csv'


plt.style.use('dark_background')
fig = plt.figure(figsize=(8, 8))
ax = fig.add_subplot(111, projection='3d')


ax.set_facecolor('black')

ax.xaxis.set_pane_color((0.0, 0.0, 0.0, 1.0))
ax.yaxis.set_pane_color((0.0, 0.0, 0.0, 1.0))
ax.zaxis.set_pane_color((0.0, 0.0, 0.0, 1.0))

ax.xaxis._axinfo["grid"]['color'] =  (1,1,1,0)
ax.yaxis._axinfo["grid"]['color'] =  (1,1,1,0)
ax.zaxis._axinfo["grid"]['color'] =  (1,1,1,0)


planet_dots = {}
planet_positions = {}
orbital_periods = {}

ax.scatter([0], [0], [0], color="yellow", s=100, label="Sun")

colors_planets = { "mercury": "#8c8c8c", "venus": "#ffcc66", "earth": "#66ccff", "mars": "#ff6666", "jupiter": "#ffcc00", "saturn": "#ff9900", "uranus": "#66ffff", "neptune": "#3366ff" }

with open(file_name, mode='r') as file:
    csv_reader = csv.DictReader(file, delimiter=';')
    

    for row in csv_reader:
        # print(f"Plotting {row} orbit")

        unit = row['Unit (AU)']
        semi_major_axis = row['Semi-major Axis']
        perihelion = row['Perihelion']
        eccentricity = row['Eccentricity']
        inclination = row['Inclination']
        longitude_of_ascending_node = row['Longitude of ascending node']
        argument_of_perihelion = row['Argument of perihelion/periapsis/perifocus']

        planet_orbit = pyasl.KeplerEllipse(a=float(semi_major_axis), per=float(perihelion), e=float(eccentricity), Omega=float(longitude_of_ascending_node), i=float(inclination), w=float(argument_of_perihelion))
        t_planet = np.linspace(0, 4 * 12, 3000)
        pos_planet = planet_orbit.xyzPos(t_planet)
        #random color
        r = lambda: np.random.randint(0,255)
        color = '#%02X%02X%02X' % (r(),r(),r())

        print(unit.lower())

        if unit.lower() in colors_planets:
            print("Found planet color")
            color = colors_planets[unit.lower()]

        planet_positions[unit] = pos_planet  # Storing positions for each planet

        # Creating scatter plot for each planet and storing it
        planet_dot = ax.scatter([pos_planet[0][1]], [pos_planet[0][0]], [0], color=color, label=f"{unit}")

        ax.plot(pos_planet[::,1], pos_planet[::,0], 'k-', color=color, alpha=0.5, linewidth=0.5)

        planet_dots[unit] = planet_dot

        a = float(semi_major_axis)
        orbital_period = np.sqrt(a**3)
        orbital_periods[unit] = orbital_period


file_name_satellites = 'Satellites-2-Table 1.csv'

# Open and read the CSV file
with open(file_name_satellites, mode='r') as file:
    csv_reader = csv.DictReader(file, delimiter=';')
    
    # Iterate over each row in the CSV file
    for row in csv_reader:
        # Extract the required fields
        parent_planet = row['Planet'].lower()
        name_satellite = row['Satellite'].lower()
        semi_major_axis = (float(row['a'])) / 149597870.7
        eccentricity = float(row['e'])
        inclination = float(row['i'])
        longitude_of_ascending_node = float(row['pnode'])
        argument_of_perihelion = float(row['ω'])
        
        if eccentricity == 1:
            print("Eccentricity is 0")
            eccentricity = 1.0000000000000001e-10

        perihelion = float(semi_major_axis) * (1 - float(eccentricity))
        

        # Do something with these variables
        # For example, print them
        # print(f"Parent Planet: {parent_planet}, Satellite: {name_satellite}, Semi-major Axis: {semi_major_axis} AU, Eccentricity: {eccentricity}, Inclination: {inclination}°, Longitude of Ascending Node: {longitude_of_ascending_node}°, Argument of Perihelion: {argument_of_perihelion}°, Perihelion: {perihelion} km")

        # if parent_planet in colors_planets:
        #     print("Found parent planet")

        #     satellite_orbit = pyasl.KeplerEllipse(a=float(semi_major_axis), per=float(perihelion), e=float(eccentricity), Omega=float(longitude_of_ascending_node), i=float(inclination), w=float(argument_of_perihelion))
        #     t_satellite = np.linspace(0, 4 * 12, 3000)
        #     pos_satellite = satellite_orbit.xyzPos(t_satellite)
        #     #plot orbit using the relative location of the parent planet
        #     ax.plot(pos_satellite[::,1], pos_satellite[::,0], 'k-', color=colors_planets[parent_planet], alpha=0.5, linewidth=0.5)



asteroid_dots = {}
asteroid_positions = {}
asteroid_orbital_periods = {}

all_asteroids = 'all_asteroids.csv'

# Open and read the CSV file
with open(all_asteroids, mode='r') as file:
    csv_reader = csv.DictReader(file, delimiter=';')
    
    # Iterate over each row in the CSV file
    for row in csv_reader:

        # Extract the required fields
        asteroid = row['Name'].lower()
        number = float(row['Num'])

        if number >= 100:
            break

        semi_major_axis = float(row['a'])
        eccentricity = float(row['e'])
        inclination = float(row['i'])
        longitude_of_ascending_node = float(row['Node'])
        argument_of_perihelion = float(row['w'])
        
        if eccentricity == 1:
            print("Eccentricity is 0")
            eccentricity = 1.0000000000000001e-10

        perihelion = float(semi_major_axis) * (1 - float(eccentricity))
        
        print(f"Asteroid: {asteroid}, Semi-major Axis: {semi_major_axis} AU, Eccentricity: {eccentricity}, Inclination: {inclination}°, Longitude of Ascending Node: {longitude_of_ascending_node}°, Argument of Perihelion: {argument_of_perihelion}°, Perihelion: {perihelion} km")

        asteroid_orbit = pyasl.KeplerEllipse(a=float(semi_major_axis), per=float(perihelion), e=float(eccentricity), Omega=float(longitude_of_ascending_node), i=float(inclination), w=float(argument_of_perihelion))
        t_asteroid = np.linspace(0, 4 * 1, 3000)
        pos_asteroid = asteroid_orbit.xyzPos(t_asteroid)

        #plot orbit using the relative location of the sun
        ax.plot(pos_asteroid[::,1], pos_asteroid[::,0], 'k-', color="white", alpha=0.5, linewidth=0.5)

 




        
min_period = min(orbital_periods.values())
relative_speeds = {}

for unit, period in orbital_periods.items():
    
    relative_speed = min_period / period

    relative_speeds[unit] = relative_speed


vicinity_radius = 0.5


def animate(i):

    for unit, planet_dot in planet_dots.items():

        pos_index = int(i * relative_speeds[unit]) % len(planet_positions[unit])
        pos_planet = planet_positions[unit][pos_index]


        planet_dot._offsets3d = (np.array([pos_planet[1]]), np.array([pos_planet[0]]), np.array([0]))

    fig.canvas.draw()

    return list(planet_dots.values())


#keep the aspect ratio of the plot to 1:1
ax.set_aspect('equal')

myAnimation = animation.FuncAnimation(fig, animate, interval=20, frames=np.arange(0, 3000), blit=True, repeat=True)

ax.set_xlabel('X Axis')
ax.set_ylabel('Y Axis')
ax.set_zlabel('Z Axis')
plt.legend(loc="lower right", fontsize='xx-small')
plt.title(f'{asteroid_name} Orbital Simulation')

# myAnimation.save(f'{asteroid_name}-orbit.gif', writer=writer)

plt.show()