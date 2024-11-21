import numpy as np

m_dot_ox = 20 # kg/s
# I_sp = 250 # s
R_i = 0.3 # m
R_f = 9 # cm
P_o = 1.5e6 # Pa
rho_f = 920 # kg / m^3
L = 500 # cm
g_o = 9.81

# # Create array to hold values of data with time.
# R_t = [R_i]
time = [0]
dt = 0.1

# Holds arrays of all variables distribituion as a function of time.
# Each array is a function of distance along the nozzle.
# Data structure has the following shape (NxM).
# Where N = number of time steps and M = number of location downstream of the nozzle.

# Create array holding inital Radius values for the fuel grain.
R_t = []
temp = []
for i in range(20):
    temp.append(R_i)
    # print(temp)
R_t.append(temp)


r_dot_t = []

# Loop through time unit the inner raidus of the fuel grain reaches the outer radius. 
i = 0
while R_t[-1, 0] < R_f:

    L_x = np.linspace(L/40, L + L/40, 20)
    R_x = []
    for j, x in enumerate(L_x):
        # print(x)

        # Oxidzier diffusion rate.
        # print(j)
        # print(R_t[-1])
        G_ox = m_dot_ox / (np.pi * R_t[-1][j-1]) # kg / (m^2*s)
        
        # # Fuel radial rate of change.
        # r_dot = 1.6086*G_ox**0.681
        r_dot = (0.036/rho_f)*((G_ox**0.8)/(x**0.2))
        # r_dot_vals.append(r_dot)
        # Calculate mass flow rate of the fuel (burned off from the fuel grain)
        m_dot_f = rho_f * (2*np.pi*R_t[-1][j-1]*L)*r_dot

        # Calculate total mass flow rate
        m_dot = m_dot_f + m_dot_ox

        # Calculate thrust 
        # T = m_dot*I_sp*g_o

        # Append data to the corresponding arrays.
        R_x.append(R_t[-1] + r_dot*dt)
        time.append(time[-1] + dt)

        i = i+1
        # print('R =', R_t[-1][0])
        # print(type(R_t[-1][0]))
        # print(type(R_f))
    R_t.append(R_x.copy())

print(R_t)