import numpy as np
import matplotlib.pyplot as plt
from matplotlib import ticker
from matplotlib.animation import FuncAnimation
from scipy.special import comb

def bernstein_basis(n, i, t):
    return comb(n, i) * (t ** i) * ((1 - t) ** (n - i))

def bezier_curve(control_points, t):
    n = len(control_points) - 1
    curve_point = np.zeros(2)
    for i in range(n + 1):
        basis = bernstein_basis(n, i, t)
        curve_point += basis * control_points[i]
    return curve_point

def animate_bezier_curve(control_points):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))  # 创建一个包含两个子图的图表
    t_values = np.linspace(0, 1, 100)

    # 设置子图1：动画曲线
    ax1.set_xlabel('x')
    ax1.set_ylabel('y')
    ax1.set_aspect('equal')  # 设置为 equal，保持纵横比为 1:1
    ax1.set_title('Bezier Curve Create Animation')
    ax1.plot(control_points[:, 0], control_points[:, 1],
             color='gray', marker='o', linestyle='-', markersize=3, linewidth=1)
    for i, point in enumerate(control_points):
        ax1.annotate(f'P{i} ({point[0]}, {point[1]})', (point[0], point[1]), textcoords="offset points",
                     xytext=(35, 0), ha='center', fontsize=8, color='purple')
    curve_line, = ax1.plot([], [], label='Bezier Curve', color='blue')
    aux_lines = [ax1.plot([], [], color='purple', linestyle='--', linewidth=.7)[0] for _ in range(len(control_points) - 1)]
    moving_points_plots = [ax1.plot([], [], 'o', color='black', markersize=3)[0] for _ in range(len(control_points))]
    # 设置网格线的间隔
    ax1.xaxis.set_major_locator(ticker.MaxNLocator(10))
    ax1.yaxis.set_major_locator(ticker.MaxNLocator(10))
    ax1.grid(True, linestyle='--')
    ax1.legend()

    # 添加显示t值的文本框
    t_text1 = ax1.text(0.45, 0.1, '', transform=ax1.transAxes, fontsize=10, verticalalignment='top', color='blue')
    result1 = ax1.text(0.3, 0.75, '', transform=ax1.transAxes, fontsize=13, verticalalignment='top', color='blue')

    # 设置子图2：伯恩斯坦基函数
    ax2.set_xlabel('t')
    ax2.set_ylabel('Basis Function Value')
    ax2.set_title('Bernstein Basis Functions')
    for i in range(len(control_points)):
        t = np.linspace(0, 1, 100)
        ax2.plot(t, bernstein_basis(len(control_points) - 1, i, t), label=f'B_{i}^{len(control_points)-1}(t)')
    line_t = ax2.axvline(x=t_values[0], color='gray', linestyle='--', linewidth=1)  # 在子图2中添加竖线


    # 设置网格线的间隔
    ax2.xaxis.set_major_locator(ticker.MaxNLocator(15))
    ax2.yaxis.set_major_locator(ticker.MaxNLocator(10))
    ax2.grid(True, linestyle='--')
    ax2.legend()

    # 添加显示t值的文本框
    t_text2 = ax2.text(0.85, 0.5, '', transform=ax2.transAxes, fontsize=10, verticalalignment='top')
    result2 = ax2.text(0.25, 0.65, '', transform=ax2.transAxes, fontsize=13, verticalalignment='top')
    b_labels = [ax2.text(0.02, .9 - i / len(control_points) * .9, '', transform=ax2.transAxes,
                         fontsize=10, verticalalignment='top') for i in range(len(control_points))]

    def update(frame, control_points, curve_line, aux_lines, t_values, moving_points_plots, line_t):
        t = t_values[frame]
        points = [control_points]

        # Compute De Casteljau's algorithm steps
        while len(points[-1]) > 1:
            next_points = []
            for i in range(len(points[-1]) - 1):
                next_point = (1 - t) * points[-1][i] + t * points[-1][i + 1]
                next_points.append(next_point)
            points.append(next_points)

        # Update curve
        curve_point = bezier_curve(control_points, t)
        curve_line.set_data(np.append(curve_line.get_xdata(), curve_point[0]),
                            np.append(curve_line.get_ydata(), curve_point[1]))

        # Update auxiliary lines and moving points
        for i, line in enumerate(aux_lines):
            if i > 0 and i < len(points) - 1:
                line.set_data([p[0] for p in points[i]], [p[1] for p in points[i]])
                moving_points_plots[i].set_data([p[0] for p in points[i]], [p[1] for p in points[i]])
            else:
                line.set_data([], [])
                moving_points_plots[i].set_data([], [])

        # Update moving points position and annotation
        moving_points_plots[-1].set_data([curve_point[0]], [curve_point[1]])
        moving_points_plots[-1].set_color('blue')
        moving_points_plots[-1].set_markersize(5)

        # Update line_t position
        line_t.set_xdata([t_values[frame], t_values[frame]])

        # Update t value text
        t_text1.set_text(f't = {t:.2f}')
        t_text2.set_text(f't = {t:.2f}')

        for i, label in enumerate(b_labels):
            label.set_text(f'B_{i}^{len(control_points)-1}(t)={bernstein_basis(len(control_points)-1, i, t):.2f}')

        value = sum([bernstein_basis(len(control_points)-1, i, t) * control_points[i] for i in range(len(control_points))])

        result1.set_text(f'Point=({curve_point[0]:.2f},{curve_point[1]:.2f})')

        formula = r'$B_n(t) = \sum_{i=0}^{n} B_{i,n} P_i$'
        result2.set_text(f'{formula}=({value[0]:.2f},{value[1]:.2f})')

        return [curve_line, *aux_lines, *moving_points_plots, line_t, t_text1, t_text2, *b_labels, result1, result2]

    def init_animation():
        # 清空曲线数据
        curve_line.set_data([], [])
        # 返回一个包含需要更新的艺术家对象的可迭代对象
        return curve_line,

    ani = FuncAnimation(fig, update, frames=range(len(t_values)),
                        fargs=(control_points, curve_line, aux_lines, t_values, moving_points_plots, line_t),
                        init_func=init_animation,
                        blit=True, repeat=True)

    plt.tight_layout()
    plt.show()

# 控制点
control_points = np.array([[0, 0], [1, 2], [3, 3], [4, 1], [5, 5]])

# 动画显示Bezier曲线和伯恩斯坦基函数
animate_bezier_curve(control_points)
