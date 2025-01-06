#all the states on the bloch sphere
import numpy as np
import matplotlib.pyplot as plt
from qiskit.visualization import plot_bloch_vector
vector1 = [0, 0, 0]#I had to set this vector to 0 because I could not customize the vector from qiskit. 
vector2 = [1, 0, 0]#This vector is plotted with matplotlib where I have way more freedom and can customize more.
vector3 = [-1, 0, 0]
vector4 = [0, 1, 0]
vector5 = [0, -1, 0]
vector6 = [0, 0, 1]
vector7 = [0, 0, -1]
fig = plt.figure(figsize=(8, 8))
ax = fig.add_subplot(111, projection='3d')
plot_bloch_vector(vector1, ax=ax)
ax.quiver(0, 0, 0, *vector2, color='r', arrow_length_ratio=0.1, linewidth=3)
ax.quiver(0, 0, 0, *vector3, color='g', arrow_length_ratio=0.1, linewidth=3)
ax.quiver(0, 0, 0, *vector4, color='b', arrow_length_ratio=0.1, linewidth=3)
ax.quiver(0, 0, 0, *vector5, color='y', arrow_length_ratio=0.1, linewidth=3)
ax.quiver(0, 0, 0, *vector6, color='c', arrow_length_ratio=0.1, linewidth=3)
ax.quiver(0, 0, 0, *vector7, color='m', arrow_length_ratio=0.1, linewidth=3)
ax.text(-3, 1.3, -0.2, r'$|+⟩= \frac{\sqrt{2}}{2}(|0⟩+|1⟩)$', color='y', fontsize = 14)
ax.text(-3, 1.3, -0.4, r'$|-⟩= \frac{\sqrt{2}}{2}(|0⟩-|1⟩)$', color='b',fontsize = 14)
ax.text(-3, 1.3, -.6, r'$|+i⟩= \frac{\sqrt{2}}{2}(|0⟩+i|1⟩)$', color='r',fontsize = 14)
ax.text(-3, 1.3, -.8, r'$|-i⟩= \frac{\sqrt{2}}{2}(|0⟩-i|1⟩)$', color='g',fontsize = 14)
ax.text(-3, 1.3, -1, '|0⟩ state', color='c',fontsize = 14)
ax.text(-3, 1.3, -1.2, '|1⟩ state', color='m',fontsize = 14)
ax.text(-1.2, 0, 0, '-Y', fontsize=9)
ax.text(0, 1.2, 0, '-X', fontsize=9)
plt.show()



