import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
# Molecular Weight as a Function from the Plotted Graph.
def get_MW(OF):
    k = [52.301, -127.7, 150.56, -89.006, 22.23, -4.631, 0.3094]
    MW = 0
    for i in range(6):
        MW = MW + k[i]*OF**i
    return MW

# Constants from your provided code
m_dot_ox_i = 20  # kg/s
R_i = 0.15  # m
R_f = 0.5  # m
P_o = 1.5e6  # Pa
rho_f = 920  # kg/m^3
L = 5  # m
g_o = 9.81  # m/s^2
dt = 1  # Time step in seconds

# Initialize arrays
num_points = 20  # Number of spatial points
L_x = np.linspace(L/40, L*(1 + L/40), num_points)  # Spatial distribution
R_t = np.full((1, num_points), R_i)  # Initial radii (2D array with 1 row)
time = [0]  # Time array

MW_t = np.full((1, num_points), 0)  # Initial radii (2D array with 1 row)

# Simulation loop
i = 0
while R_t[-1, 0] < R_f: # Compare only the last element in the last row
    R_x = np.zeros(num_points)
    MW_x = np.zeros(num_points)
    m_dot_ox = m_dot_ox_i
    m_dot_f = 0
    for j, x in enumerate(L_x):
        # Add fuel mass to up stream slice.
        m_dot_ox = m_dot_ox + m_dot_f

        # Oxidizer diffusion rate (vectorized)
        G_ox = m_dot_ox / (np.pi * R_t[-1, j]**2)

        # Radial rate of change
        r_dot = (0.036 / rho_f) * ((G_ox ** 0.8) / (x) ** 0.2)

        # Stop calculating radial rates of change if they exceed the final radius.
        if R_t[i][j] > R_f:
            R_x[j] = R_f
        else:
            R_x[j] = R_t[i, j] + r_dot * dt  # Update radii
        
        # Calculate mass to feed up stream
        m_dot_f = rho_f*np.pi*R_x[j]**2*r_dot

        OF = m_dot_ox / m_dot_f

        MW_x[j] = get_MW(OF)

    # Append new radii distribution
    R_t = np.vstack([R_t, R_x])
    time.append(time[-1] + dt)
    i += 1

# Animation setup
fig, ax = plt.subplots()
line, = ax.plot([], [], lw=2)
ax.set_ylim(R_i, R_f)
ax.set_xlim(0, L)
ax.set_xlabel("Position (m)")
ax.set_ylabel("Radius (m)")
ax.set_title("Radii Evolution Over Time")

def init():
    line.set_data([], [])
    return line,

def update(frame):
    line.set_data(L_x, R_t[frame])
    current_time = time[frame]  # Get the time corresponding to the frame
    ax.set_title(f"Radii Evolution Over Time (t = {current_time:.2f} s)")
    return line,

anim = FuncAnimation(fig, update, frames=len(R_t), init_func=init, blit=True)

# Save the animation as an MP4 file
anim.save('radii_evolution.mp4', fps=30, extra_args=['-vcodec', 'libx264'])

print("Animation saved as radii_evolution.mp4")


# Plot fuel grain radii.
index_vals = [50, 100, 150, 200, i]
plt.clf()

for i in index_vals:
    plt.plot(L_x, R_t[i], label = 'time = ' + str(time[i]))
plt.xlabel("Position (m)")
plt.ylabel("Radius (m)")
plt.title("Radii Evolution Over Time")
plt.legend(loc="upper right")
plt.savefig('raddii_time_steps.png')
