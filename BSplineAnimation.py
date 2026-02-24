import numpy as np
import matplotlib.pyplot as plt
from matplotlib import ticker
from matplotlib.animation import FuncAnimation

def basis_function(i, k, u, nodes):
    if k == 0:
        return 1.0 if nodes[i] <= u < nodes[i + 1] else 0.0
    term1 = 0.0 if nodes[i + k] == nodes[i] else (u - nodes[i]) / (nodes[i + k] - nodes[i])
    term2 = 0.0 if nodes[i + k + 1] == nodes[i + 1] else (nodes[i + k + 1] - u) / (nodes[i + k + 1] - nodes[i + 1])
    return term1 * basis_function(i, k - 1, u, nodes) + term2 * basis_function(i + 1, k - 1, u, nodes)

def b_spline_curve(control_points, nodes, degree, num_points):
    curve_points = []
    for u in np.linspace(nodes[degree], nodes[-degree - 1], num_points):
        point = np.zeros(2)  # 假设是二维点
        for i, control_point in enumerate(control_points):
            basis = basis_function(i, degree, u, nodes)
            point += control_point * basis
        curve_points.append(point)
    return np.array(curve_points)

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

def animate_bspline_curve(ax1, ax2, control_points, degree, num_points, node_type='periodic'):
    ax1.set_xlim(np.min(control_points[:, 0]) - 1, np.max(control_points[:, 0]) + 1)
    ax1.set_ylim(np.min(control_points[:, 1]) - 1, np.max(control_points[:, 1]) + 1)
    ax1.set_xlabel('X-axis')
    ax1.set_ylabel('Y-axis')
    ax1.set_title(f'B-spline Curve (Degree {degree}) - {node_type.capitalize()} Nodes')

    # 绘制控制点和控制多边形
    for i, point in enumerate(control_points):
        ax1.annotate(f'P{i} ({point[0]}, {point[1]})', (point[0], point[1]), textcoords="offset points",
                     xytext=(35, 0), ha='center', fontsize=8, color='purple')
    ax1.scatter(control_points[:, 0], control_points[:, 1], color='red', label="Control Points")
    ax1.plot(control_points[:, 0], control_points[:, 1], color='gray', linestyle='--', label="Control Polygon")
    ax1.xaxis.set_major_locator(ticker.MaxNLocator(15))
    ax1.yaxis.set_major_locator(ticker.MaxNLocator(10))
    ax1.legend()
    ax1.grid(True)

    # 创建节点向量
    if node_type == 'periodic':
        nodes = create_periodic_nodes(len(control_points), degree)
    else:
        nodes = create_open_uniform_nodes(len(control_points), degree)

    # 初始化曲线
    line, = ax1.plot([], [], label="B-spline Curve", color='blue')

    moving_point = ax1.plot([], [], 'o', color='black', markersize=3)[0]
    cur_point = ax1.text(0.1, 0.1, '---', transform=ax1.transAxes, fontsize=10, verticalalignment='top')

    # 右侧子图：条件基函数视图和当前变量值标签
    ax2.set_title('B-spline Basis Functions')
    ax2.set_xlabel('u')
    ax2.set_ylabel('Basis Function Value')
    ax2.xaxis.set_major_locator(ticker.MaxNLocator(15))
    ax2.yaxis.set_major_locator(ticker.MaxNLocator(10))
    ax2.legend()
    ax2.grid(True)

    # 绘制基函数初始值
    k = degree
    t_values = np.linspace(nodes[0], nodes[-1], 100)
    basis_lines = [ax2.plot(t_values,
                            [basis_function(i, k, t, nodes) for t in t_values],
                            label=f'B{i},{k}')[0] for i in range(len(control_points))]

    b_labels = [ax2.text(0.02, .9 - i / len(control_points) * .9, '', transform=ax2.transAxes,
                         fontsize=10, verticalalignment='top') for i in range(len(control_points))]

    # 添加显示当前变量值的文本框
    text_u = ax2.text(0.45, 0.9, '', transform=ax2.transAxes, fontsize=12, verticalalignment='top')
    line_u = ax2.axvline(x=0, color='gray', linestyle='--', linewidth=1)  # 在子图2中添加竖线
    result = ax2.text(0.25, 0.2, '', transform=ax2.transAxes, fontsize=10, verticalalignment='top')

    def update(frame):
        u = np.linspace(nodes[degree], nodes[-degree - 1], num_points)[frame]
        curve_points = b_spline_curve(control_points, nodes, degree, num_points)
        line.set_data(curve_points[:frame, 0], curve_points[:frame, 1])

        # 更新右侧基函数视图
        for i, basis_line in enumerate(basis_lines):
            basis_line.set_ydata([basis_function(i, k, t, nodes) for t in t_values])

        # 更新当前变量值的文本框
        text_u.set_text(f'u = {u:.2f}')
        line_u.set_xdata([u, u])

        for i, label in enumerate(b_labels):
            label.set_text(f'B{i},{k}(u)={basis_function(i, k, u, nodes):.2f}')

        formula = r'$P(u) = \sum_{i=0}^{n} B_{i,k} P_i$'
        field = r'$, \quad u \in [u_{k-1}, u_{n+1}]$'
        value = sum([basis_function(i, k, u, nodes) * control_points[i] for i in range(len(control_points))])
        result.set_text(f'{formula} = ({value[0]:.2f}, {value[1]:.2f}){field}')
        cur_point.set_text(f'Point=({value[0]:.2f}, {value[1]:.2f})')

        moving_point.set_data([value[0]], [value[1]])
        moving_point.set_color('blue')
        moving_point.set_markersize(5)

        return line, *basis_lines, *b_labels, text_u, line_u, result, cur_point, moving_point

    return FuncAnimation(fig, update, frames=num_points, blit=True, repeat=False)

# 示例使用
control_points = np.array([
    [0, 0], [1, 2], [3, 5], [4, 4], [5, 0], [6, -3], [7, 0], [8, 2], [9, 1], [10, 0]
])
degree = 3
num_points = 100

fig, axes = plt.subplots(2, 2, figsize=(12, 10), gridspec_kw={'height_ratios': [1, 1]})

# 上下排列两个动画
ani_periodic = animate_bspline_curve(axes[0, 0], axes[0, 1], control_points, degree, num_points, node_type='periodic')
ani_open_uniform = animate_bspline_curve(axes[1, 0], axes[1, 1], control_points, degree, num_points, node_type='open_uniform')

plt.tight_layout()
plt.show()
