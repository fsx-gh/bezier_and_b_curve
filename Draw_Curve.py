import pygame
import sys
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import numpy as np

# 初始化Pygame
pygame.init()

# 设置Pygame绘图区域大小
drawing_width = 800
drawing_height = 600

# 创建Tkinter窗口
root = tk.Tk()
root.title("bezier曲线绘制")

# 设置Tkinter窗口大小
root.geometry(f'{drawing_width + 150}x{drawing_height}')

# 添加一个Frame用于包含Canvas和边框
drawing_frame = tk.Frame(root, width=drawing_width, height=drawing_height, bg='black', bd=2, relief=tk.SUNKEN)
drawing_frame.pack(side=tk.LEFT, padx=10, pady=10)

# 添加一个Canvas用于嵌入Pygame绘图区域
canvas = tk.Canvas(drawing_frame, width=drawing_width, height=drawing_height)
canvas.pack()

# 创建一个Frame用于放置控制按钮
control_frame = tk.Frame(root, width=200, height=drawing_height)
control_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)

# 添加一个Frame用于居中按钮，放置在control_frame的顶部
button_frame = tk.Frame(control_frame)
button_frame.pack(anchor=tk.N, pady=20)

# 添加节点函数
def add_mode():
    global mode
    mode = 'add'

# 删除节点函数
def remove_mode():
    global mode
    mode = 'remove'

# 移动节点函数
def move_mode():
    global mode
    mode = 'move'

# 选择贝塞尔曲线函数
def bezier_mode():
    global curve_mode
    curve_mode = 'bezier'
    root.title("bezier曲线绘制")
    messagebox.showinfo("Curve Mode", "已选择绘制贝塞尔曲线")

# 选择B样条曲线函数
def bspline_mode():
    global curve_mode
    curve_mode = 'bspline'
    root.title("bspline曲线绘制")
    messagebox.showinfo("Curve Mode", "已选择绘制B样条曲线")

# 添加控制按钮
add_button = ttk.Button(button_frame, text="添加节点", command=add_mode)
add_button.pack(pady=10)

remove_button = ttk.Button(button_frame, text="删除节点", command=remove_mode)
remove_button.pack(pady=10)

move_button = ttk.Button(button_frame, text="移动节点", command=move_mode)
move_button.pack(pady=10)

bezier_button = ttk.Button(button_frame, text="选择贝塞尔曲线", command=bezier_mode)
bezier_button.pack(pady=10)

bspline_button = ttk.Button(button_frame, text="选择B样条曲线", command=bspline_mode)
bspline_button.pack(pady=10)

# 设置颜色
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
gray = (200, 200, 200)
blue = (0, 0, 255)

# 存储顶点的列表
vertices = []
mode = 'add'  # 默认模式为添加节点
moving_vertex_index = None
curve_mode = 'bezier'  # 默认绘制贝塞尔曲线

# 创建Pygame绘图表面
screen = pygame.Surface((drawing_width, drawing_height))

def pygame_to_tk_image(surface):
    # 将Pygame表面转换为PIL图像
    pygame_image = pygame.surfarray.array3d(surface)
    pil_image = Image.fromarray(pygame_image.transpose((1, 0, 2)))
    return ImageTk.PhotoImage(image=pil_image)

def handle_mouse_click(event):
    global moving_vertex_index
    # 获取相对Canvas的鼠标点击位置
    mouse_x, mouse_y = event.x, event.y
    if mouse_x < drawing_width:  # 确保点击在左侧绘图区域
        if mode == 'add':
            # 添加节点
            vertices.append((mouse_x, mouse_y))
        elif mode == 'remove':
            # 删除节点
            if vertices:
                # 查找离鼠标点击位置最近的顶点并删除
                closest_vertex_index = None
                closest_distance = float('inf')
                for i, vertex in enumerate(vertices):
                    distance = ((vertex[0] - mouse_x) ** 2 + (vertex[1] - mouse_y) ** 2) ** 0.5
                    if distance < closest_distance:
                        closest_distance = distance
                        closest_vertex_index = i
                if closest_vertex_index is not None and closest_distance < 10:  # 距离阈值，避免误删
                    vertices.pop(closest_vertex_index)
        elif mode == 'move':
            # 选中要移动的节点
            moving_vertex_index = None
            closest_distance = float('inf')
            for i, vertex in enumerate(vertices):
                distance = ((vertex[0] - mouse_x) ** 2 + (vertex[1] - mouse_y) ** 2) ** 0.5
                if distance < closest_distance:
                    closest_distance = distance
                    moving_vertex_index = i
            if closest_distance >= 10:  # 距离阈值，避免误选
                moving_vertex_index = None

def handle_mouse_motion(event):
    global moving_vertex_index
    if moving_vertex_index is not None and mode == 'move':
        mouse_x, mouse_y = event.x, event.y
        if mouse_x < drawing_width:  # 确保移动在左侧绘图区域
            vertices[moving_vertex_index] = (mouse_x, mouse_y)

canvas.bind("<Button-1>", handle_mouse_click)
canvas.bind("<B1-Motion>", handle_mouse_motion)

def draw_grid_and_axes(screen):
    # 绘制网格线和坐标轴
    for x in range(100, drawing_width, 70):  # 范围调整为覆盖大约70个单位
        pygame.draw.line(screen, gray, (x, 0), (x, drawing_height), 1)
    for y in range(drawing_height-100, 0, -70):  # 范围调整为覆盖大约70个单位
        pygame.draw.line(screen, gray, (0, y), (drawing_width, y), 1)

    # 原点坐标
    origin_x = 70
    origin_y = drawing_height - 70

    pygame.draw.line(screen, black, (origin_x, 0), (origin_x, drawing_height), 2)  # 纵坐标
    pygame.draw.line(screen, black, (0, origin_y), (drawing_width, origin_y), 2)  # 横坐标

def draw_labels(screen):
    font = pygame.font.SysFont('Arial', 15)
    origin_x = 70
    origin_y = drawing_height - 70
    # 绘制 x 轴和 y 轴坐标
    for x in range(100, drawing_width, 70):  # 范围调整为覆盖大约70个单位
        label = font.render(str((x-origin_x) // 70), True, black)  # 调整除法以匹配新的范围
        screen.blit(label, (x, origin_y + 5))
    for y in range(drawing_height-100, 0, -70):  # 范围调整为覆盖大约70个单位
        label = font.render(str((origin_y-y) // 70), True, black)  # 调整除法以匹配新的范围
        screen.blit(label, (origin_x + 5, y))

def draw_vertices(screen, vertices):
    font = pygame.font.SysFont('Arial', 15)
    origin_x = 70
    origin_y = drawing_height - 70
    for i, vertex in enumerate(vertices):
        pygame.draw.circle(screen, blue, vertex, 3)  # 蓝色 (0, 0, 255) 和半径 3
        # 将屏幕坐标转换为实际坐标
        x_coord = ((vertex[0] - origin_x) / 70)
        y_coord = ((origin_y - vertex[1]) / 70)
        # 绘制顶点标识和坐标
        label = font.render(f'p{i} ({x_coord:.2f},{y_coord:.2f})', True, black)
        screen.blit(label, (vertex[0] + 5, vertex[1] - 15))


def bezier_curve(vertices, num_points=100):
    # 计算贝塞尔曲线上的点
    n = len(vertices) - 1
    curve = []
    for t in np.linspace(0, 1, num_points):
        x = sum(
            [binomial_coeff(n, i) * (1 - t) ** (n - i) * t ** i * vertices[i][0] for i in range(n + 1)]
        )
        y = sum(
            [binomial_coeff(n, i) * (1 - t) ** (n - i) * t ** i * vertices[i][1] for i in range(n + 1)]
        )
        curve.append((int(x), int(y)))
    return curve

def binomial_coeff(n, k):
    # 计算二项式系数 C(n, k)
    return np.math.factorial(n) // (np.math.factorial(k) * np.math.factorial(n - k))

def bspline_curve(vertices, num_points=100):
    # 计算B样条曲线上的点
    k = 3  # 阶数 (k阶B样条，通常为3)
    n = len(vertices)
    if n < k + 1:
        return []  # 如果顶点数少于k+1，无法形成B样条
    t = np.linspace(0, 1, num_points)
    T = [0] * k + list(np.linspace(0, 1, n - k + 1)) + [1] * k
    curve = []
    for u in t:
        x, y = 0, 0
        for i in range(n):
            b = bspline_basis(i, k, u, T)
            x += vertices[i][0] * b
            y += vertices[i][1] * b
        curve.append((int(x), int(y)))
    return curve

def bspline_basis(i, k, u, T):
    if k == 0:
        if T[i] <= u < T[i + 1] or (u == T[-1] and T[i] <= u <= T[i + 1]):
            return 1
        return 0
    denominator1 = T[i + k] - T[i]
    denominator2 = T[i + k + 1] - T[i + 1]
    coef1 = (u - T[i]) / denominator1 if denominator1 != 0 else 0
    coef2 = (T[i + k + 1] - u) / denominator2 if denominator2 != 0 else 0
    return coef1 * bspline_basis(i, k - 1, u, T) + coef2 * bspline_basis(i + 1, k - 1, u, T)

def draw_bezier_curve(screen, vertices):
    # 绘制贝塞尔曲线
    curve_points = bezier_curve(vertices)
    pygame.draw.lines(screen, red, False, curve_points, 2)

def draw_bspline_curve(screen, vertices):
    # 绘制B样条曲线
    curve_points = bspline_curve(vertices)
    if curve_points:  # 确保有足够的顶点绘制B样条曲线
        pygame.draw.lines(screen, red, False, curve_points, 2)

def draw_polygon(screen, vertices):
    if len(vertices) > 1:
        pygame.draw.lines(screen, gray, False, vertices, 2)

# 主循环
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 填充背景颜色
    screen.fill(white)

    # 绘制网格线和坐标轴
    draw_grid_and_axes(screen)
    draw_labels(screen)

    # 绘制控制多边形
    draw_polygon(screen, vertices)

    # 绘制所有顶点及其坐标
    draw_vertices(screen, vertices)

    # 根据选择绘制相应的曲线
    if curve_mode == 'bezier':
        draw_bezier_curve(screen, vertices)
    elif curve_mode == 'bspline':
        draw_bspline_curve(screen, vertices)

    # 将Pygame绘图表面渲染到Tkinter Canvas
    tk_image = pygame_to_tk_image(screen)
    canvas.create_image((0, 0), anchor=tk.NW, image=tk_image)

    # 更新Tkinter窗口
    root.update_idletasks()
    root.update()

# 退出Pygame
pygame.quit()
sys.exit()
