import numpy as np
import matplotlib.pyplot as plt

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

# 创建节点矢量和生成曲线函数
def generate_and_plot_spline(control_points, degree, num_points):
    open_uniform_nodes = create_open_uniform_nodes(len(control_points), degree)
    periodic_nodes = create_periodic_nodes(len(control_points), degree)

    open_curve_points = b_spline_curve(control_points, open_uniform_nodes, degree, num_points)
    periodic_curve_points = b_spline_curve(control_points, periodic_nodes, degree, num_points)

    return open_curve_points, periodic_curve_points

def plot_bspline():
    # 生成并绘制曲线
    fig, axes = plt.subplots(2, 2, figsize=(10, 6))
    fig.subplots_adjust(left=0.2, hspace=1, wspace=3)  # 调整左侧边距和子图之间的间距

    # 二次均匀开放B样条曲线
    degree = 2
    open_curve_points, periodic_curve_points = generate_and_plot_spline(control_points, degree, num_points)
    axes[0, 0].plot(open_curve_points[:, 0], open_curve_points[:, 1], label="Open Uniform B-spline")
    axes[0, 0].scatter(control_points[:, 0], control_points[:, 1], color='red', label="Control Points")
    axes[0, 0].plot(control_points[:, 0], control_points[:, 1], color='gray', linestyle='--', label="Control Polygon")
    axes[0, 0].set_xlabel("X-axis")
    axes[0, 0].set_ylabel("Y-axis")
    axes[0, 0].set_title(f"Open Uniform B-spline Curve (Degree {degree})")
    axes[0, 0].legend(fontsize='small')
    axes[0, 0].grid(True)

    # 二次均匀周期B样条曲线
    axes[0, 1].plot(periodic_curve_points[:, 0], periodic_curve_points[:, 1], label="Periodic B-spline")
    axes[0, 1].scatter(control_points[:, 0], control_points[:, 1], color='red', label="Control Points")
    axes[0, 1].plot(control_points[:, 0], control_points[:, 1], color='gray', linestyle='--', label="Control Polygon")
    axes[0, 1].set_xlabel("X-axis")
    axes[0, 1].set_ylabel("Y-axis")
    axes[0, 1].set_title(f"Periodic B-spline Curve (Degree {degree})")
    axes[0, 1].legend(fontsize='small')
    axes[0, 1].grid(True)

    # 三次均匀开放B样条曲线
    degree = 3
    open_curve_points, periodic_curve_points = generate_and_plot_spline(control_points, degree, num_points)
    axes[1, 0].plot(open_curve_points[:, 0], open_curve_points[:, 1], label="Open Uniform B-spline")
    axes[1, 0].scatter(control_points[:, 0], control_points[:, 1], color='red', label="Control Points")
    axes[1, 0].plot(control_points[:, 0], control_points[:, 1], color='gray', linestyle='--', label="Control Polygon")
    axes[1, 0].set_xlabel("X-axis")
    axes[1, 0].set_ylabel("Y-axis")
    axes[1, 0].set_title(f"Open Uniform B-spline Curve (Degree {degree})")
    axes[1, 0].legend(fontsize='small')
    axes[1, 0].grid(True)

    # 三次均匀周期B样条曲线
    axes[1, 1].plot(periodic_curve_points[:, 0], periodic_curve_points[:, 1], label="Periodic B-spline")
    axes[1, 1].scatter(control_points[:, 0], control_points[:, 1], color='red', label="Control Points")
    axes[1, 1].plot(control_points[:, 0], control_points[:, 1], color='gray', linestyle='--', label="Control Polygon")
    axes[1, 1].set_xlabel("X-axis")
    axes[1, 1].set_ylabel("Y-axis")
    axes[1, 1].set_title(f"Periodic B-spline Curve (Degree {degree})")
    axes[1, 1].legend(fontsize='small')
    axes[1, 1].grid(True)

    # 显示绘图
    plt.tight_layout()
    plt.show()

# 示例使用
control_points = np.array([
    [0, 0], [1, 2], [3, 5], [4, 4], [5, 0], [6, -3], [7, 0]
])

num_points = 100

plot_bspline()
