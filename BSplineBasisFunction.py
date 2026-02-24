import numpy as np
import matplotlib.pyplot as plt
from matplotlib import ticker

def basis_function(i, k, u, nodes):
    if k == 0:
        return 1.0 if nodes[i] <= u < nodes[i + 1] else 0.0
    term1 = 0.0 if nodes[i + k] == nodes[i] else (u - nodes[i]) / (nodes[i + k] - nodes[i])
    term2 = 0.0 if nodes[i + k + 1] == nodes[i + 1] else (nodes[i + k + 1] - u) / (nodes[i + k + 1] - nodes[i + 1])
    return term1 * basis_function(i, k - 1, u, nodes) + term2 * basis_function(i + 1, k - 1, u, nodes)

def create_periodic_nodes(num_control_points, degree):
    nodes = np.zeros(num_control_points + degree + 1)
    for j in range(num_control_points + degree + 1):
        nodes[j] = j - degree
    return nodes

def create_open_uniform_nodes(num_control_points, degree):
    nodes = np.zeros(num_control_points + degree + 1)
    nodes[:degree + 1] = 0
    nodes[-degree - 1:] = num_control_points - degree
    nodes[degree + 1:-degree - 1] = np.arange(1, num_control_points - degree)
    return nodes

def plot_basis_functions(ax, control_points, degree, node_type='periodic'):
    ax.set_title(f'B-spline Basis Functions (Degree {degree}, {node_type.capitalize()} Nodes)')
    ax.set_xlabel('u')
    ax.set_ylabel('Basis Function Value')
    ax.xaxis.set_major_locator(ticker.MaxNLocator(15))
    ax.yaxis.set_major_locator(ticker.MaxNLocator(10))
    ax.grid(True)

    # Create node vector
    if node_type == 'periodic':
        nodes = create_periodic_nodes(len(control_points), degree)
    else:
        nodes = create_open_uniform_nodes(len(control_points), degree)

    # Plot basis functions
    k = degree
    t_values = np.linspace(nodes[0], nodes[-1], 100)
    for i in range(len(control_points)):
        ax.plot(t_values, [basis_function(i, k, t, nodes) for t in t_values], label=f'B{i},{k}')

    ax.legend(fontsize='small')

# Example usage
control_points = np.array([
    [0, 0], [1, 2], [3, 5], [4, 4], [5, 0], [6, -3], [7, 0]
])

fig, axes = plt.subplots(2, 2, figsize=(10, 6))
fig.subplots_adjust(left=0.2, hspace=1, wspace=3)  # 调整左侧边距和子图之间的间距

# Plot 2nd degree periodic basis functions
plot_basis_functions(axes[0, 0], control_points, degree=2, node_type='periodic')

# Plot 2nd degree open uniform basis functions
plot_basis_functions(axes[0, 1], control_points, degree=2, node_type='open_uniform')

# Plot 3rd degree periodic basis functions
plot_basis_functions(axes[1, 0], control_points, degree=3, node_type='periodic')

# Plot 3rd degree open uniform basis functions
plot_basis_functions(axes[1, 1], control_points, degree=3, node_type='open_uniform')

plt.tight_layout()
plt.show()
