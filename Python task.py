# -*- coding: utf-8 -*-
"""
@author: Thomas Declercq
"""
import math
import matplotlib.pyplot as plt
#import scipy.integrate as integrate


# Constants and coefficients

µ = 0.05 # Dynamic friction coefficient, rubber wheels, wet road, aquaplaning
g = 9.81 # m/s² Gravitional acceleration

# Variables

m = float(input("Enter the mass (in kg): "))                        # mass in kg
v_initial = float(input("Enter the initial velocity (in m/s): "))   # initial velocity in m/s
degr = float(input("Enter inclination (in °): "))                   # degree of inclination
t_initial = 0

# Ensure that the road type variable has specific value
while True:
    road_type = input("Enter the road type (concrete, ice, water, gravel, or sand): ")
    if road_type in ["concrete", "ice", "water", "gravel", "sand"]:
        break
    print("Invalid road type. Please enter concrete, ice, water, gravel, or sand.")

# Print a list of valid road condition values depending on the road type
if road_type in ["concrete", "ice"]:
    print("Valid road condition values: dry, wet")
elif road_type in ["water"]:
    print("Valid road condition value: aquaplaning")
elif road_type in ["gravel", "sand"]:
    print("Valid road condition value: dry")

# Ensure that the road condition variable has a valid value depending on the road type
while True:
    road_condition = input("Enter the road condition: ")
    if road_type in ["concrete", "ice"] and road_condition in ["wet", "dry"]:
        break
    elif road_type in ["water"] and road_condition in ["aquaplaning"]:
        break
    elif road_type in ["gravel", "sand"] and road_condition == "dry":
        break
    print("Invalid road condition for selected road type. Please enter a valid road condition.")    


# Define an array of friction coefficients for different road types and conditions
u_array = [[0.5, 0.35], [0.15, 0.08], [0, 0, 0.05], [0.35], [0.3]]
road_type_array = ["concrete", "ice", "water", "gravel", "sand"]
road_condition_array = ["dry", "wet", "aquaplaning"]

u = u_array[road_type_array.index(road_type)][road_condition_array.index(road_condition)] #selection of the actual friction coefficient

#physics
F_N = m*g*math.cos(math.radians(degr))
F_R = u*F_N                                     #branking force
F_I = m*g*math.sin(math.radians(degr))          #force due to inclination
F_B = F_R + m*g*math.sin(math.radians(degr))    #braking force due to frictional force and inclination
a = F_B/m
#v = a*t
#s = s_0 + v*t + 1/2*a*t^2

#conservation of energy
#W_kin=(m*v^2)/2
#W_fric=integrate.quad(F_R, 0, s)

#rule of thumb
v_km=v_initial*3.6
s_normal=(v_km/10)**2
s_danger=(v_km/10)**2/2
s_reaction=(v_km/10)*3


#plot

n_steps = 100000   # Set the number of time steps
dt = 0.01          # Set the time step size

# Initialize lists to store the time, velocity, and displacement at each time step
time = [t_initial]
velocity = [v_initial]
displacement = [0]

# Calculate the velocity and displacement at each time step

for i in range(n_steps):    #During reaction time
    t = t_initial + i*dt
    s = v_initial*t
    time.append(t)
    velocity.append(v_initial)
    displacement.append(s)
    if s >= s_reaction:
        t_initial = t
        s_initial = s
        break
    
for i in range(n_steps):    #During actual braking
    t = t_initial + i*dt
    v = v_initial - a*(t-t_initial)
    
    #stop loop when velocity is smaller or equal to 0
    if v <= 0:
        t_initial = t
        v_initial = v
        s_initial = s
        break
    
    s = s_initial + v*(t-t_initial) + 0.5*a*(t-t_initial)**2
    time.append(t)
    velocity.append(v)
    displacement.append(s)

 
     
# Create a figure with two subplots
fig, ax = plt.subplots(nrows=1, ncols=2)

# Plot the speed over time in the first subplot
ax[0].plot(time, velocity)
ax[0].set_xlabel("Time (s)")
ax[0].set_ylabel("Speed (m/s)")
ax[0].set_title("Speed over Time")

# Plot the speed over distance in the second subplot
ax[1].plot(time, displacement)
ax[1].set_xlabel("Time (s)")
ax[1].set_ylabel("Displacement (m)")
ax[1].set_title("Distance over Time")

# Show the figure and results
plt.show()
print()
print("The needed braking distance was", round(s,2),"m")
print("The needed time to stop was", round(t,2),"s")

# Comparison against rule of thumb
print()
print("The normal braking distance according to the rule of thumb is", round(s_normal,2),"m")
print("The danger braking distance according to the rule of thumb is", round(s_danger,2),"m")
print("The reaction braking distance according to the rule of thumb is", round(s_reaction,2),"m")