import numpy as np

# Define constants
m_dot_ox = 20  # kg/s
R_i = 0.03  # m (initial radius)
R_f = 0.09  # m (converted from 9 cm)
P_o = 1.5e6  # Pa
rho_f = 920  # kg/m^3
L = 5.0  # m (converted from 500 cm)
g_o = 9.81  # m/s^2
dt = 0.1  # Time step in seconds

# Initialize arrays
num_points = 20  # Number of spatial points
L_x = np.linspace(0, L, num_points)  # Spatial distribution
R_t = np.full((1, num_points), R_i)  # Initial radii (2D array with 1 row)
time = [0]  # Time array

# Simulation loop
while R_t[-1, 0] < R_f:  # Compare only the first element in the last row
    L_x = np.linspace(L/40, L + L/40, 20)
    R_x = np.zeros(20)
    for j, x in enumerate(L_x):
        G_ox = m_dot_ox / (np.pi * R_t[-1, j])  # Oxidizer diffusion rate (vectorized)
        r_dot = (0.036 / rho_f) * ((G_ox ** 0.8) / (x + L/40) ** 0.2)  # Radial rate of change
        print(R_t[-1][j])
        print(type(R_t[-1][j]))
        R_x[j] = R_t[-1, j] + r_dot * dt  # Update radii (vectorized)
        R_t = np.vstack([R_t, R_x])  # Append new radii (add new row)
        time.append(time[-1] + dt)  # Update time

# Results
print("Final Radii Distribution (m):", R_t[-1])
print("Number of Time Steps:", len(time))
print("Final Time (s):", time[-1])
print(R_t)
