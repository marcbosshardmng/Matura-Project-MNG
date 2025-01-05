#phase on the bloch sphere
import matplotlib.pyplot as plt
from qiskit.visualization import plot_bloch_vector
vector1 = [0, 0, 0]
vector4 = [0, 1, 0]
vector5 = [0, -1, 0]
fig = plt.figure(figsize=(8, 8))
ax = fig.add_subplot(111, projection='3d')
plot_bloch_vector(vector1, ax=ax)
ax.quiver(0, 0, 0, *vector4, color='g', arrow_length_ratio=0.1, linewidth=3)
ax.quiver(0, 0, 0, *vector5, color='r', arrow_length_ratio=0.1, linewidth=3)
ax.text(-3, 1.3, -0.2, r'$|+⟩= \frac{\sqrt{2}}{2}(|0⟩+|1⟩)$', color='r', fontsize = 14)
ax.text(-3, 1.3, -0.4, r'$|-⟩= \frac{\sqrt{2}}{2}(|0⟩-|1⟩)$', color='g',fontsize = 14)
ax.text(-1.2, 0, 0, '-Y', fontsize=9)
ax.text(0, 1.2, 0, '-X', fontsize=9)
plt.show()
