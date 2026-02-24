import tkinter as tk
from math import comb
from tkinter import ttk, filedialog, messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.ticker as ticker

class BezierCurveApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Bezier Curve Generation")
        self.root.geometry("1200x800")
        self.root.resizable(False, False)

        self.num_points = tk.IntVar()
        self.entries = []

        self.setup_ui()

        # 绑定关闭事件
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def setup_ui(self):
        control_frame = tk.Frame(self.root, width=300, relief=tk.SUNKEN, borderwidth=2, bg="lightblue")
        control_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=5, pady=10)
        control_frame.pack_propagate(False)

        ttk.Label(control_frame, text="Number of Points", background="lightblue", foreground="blue",
                  font=("Helvetica", 10, "bold")).pack(anchor=tk.CENTER, pady=5)
        ttk.Entry(control_frame, textvariable=self.num_points, width=10, validate="key",
                  validatecommand=(self.root.register(self.validate_real_number), '%P'), justify="center").pack(
            anchor=tk.CENTER, padx=5, pady=5)
        ttk.Button(control_frame, text="Input", command=self.create_input_fields).pack(anchor=tk.CENTER, padx=5, pady=5)
        ttk.Button(control_frame, text="Import Data", command=self.Import_data).pack(anchor=tk.CENTER, padx=5, pady=5)
        ttk.Button(control_frame, text="Export Data", command=self.Export_data).pack(anchor=tk.CENTER, padx=5, pady=5)

        self.input_frame_container = ttk.Frame(control_frame)
        self.input_frame_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Create a canvas object and a vertical scrollbar for scrolling it
        self.canvas = tk.Canvas(self.input_frame_container)
        self.scrollbar = ttk.Scrollbar(self.input_frame_container, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Pack the canvas and scrollbar
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Create a frame inside the canvas which will hold the input fields
        self.scrollable_frame = ttk.Frame(self.canvas)
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        self.plot_button = ttk.Button(control_frame, text="Plot", command=self.plot_curve)
        self.plot_button.pack(anchor=tk.CENTER, padx=5, pady=5)

        self.connect_button = ttk.Button(control_frame, text="Connect", command=self.connect_curve)
        self.connect_button.pack(anchor=tk.CENTER, padx=5, pady=5)

        plot_frame = tk.Frame(self.root, relief=tk.SUNKEN, borderwidth=5, bg="purple")
        plot_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.figure, self.ax = plt.subplots(figsize=(8, 6))
        self.canvas_plot = FigureCanvasTkAgg(self.figure, master=plot_frame)
        self.canvas_plot.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        self.ax.set_xlabel('x')
        self.ax.set_ylabel('y')
        self.ax.set_title('Bezier Curve Generation')
        # 设置网格线的间隔
        self.ax.xaxis.set_major_locator(ticker.MaxNLocator(10))
        self.ax.yaxis.set_major_locator(ticker.MaxNLocator(10))

        # 设置网格线的样式为虚线
        self.ax.grid(True, linestyle='--')

    def validate_real_number(self, value):
        if value == "":
            return True
        try:
            float(value)
            return True
        except ValueError:
            return False

    def create_input_fields(self):
        self.curves = [self.num_points.get()]
        self.create_fields()

    def create_fields(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        self.entries = []

        # Iterate through each group's number of points
        for group_index, num_points in enumerate(self.curves):
            entry = []

            # Create a label for the group
            group_label = ttk.Label(self.scrollable_frame, text=f"Group {group_index}",
                                    font=("Helvetica", 10, "bold"))
            group_label.pack(anchor=tk.W, pady=5)
            for i in range(num_points):
                frame = ttk.Frame(self.scrollable_frame)
                frame.pack(anchor=tk.W, pady=2)
                ttk.Label(frame, padding=(5, 0)).pack(side=tk.LEFT)
                y_entry = ttk.Entry(frame, width=10, validate="key",
                                    validatecommand=(self.root.register(self.validate_real_number), '%P'), justify="center")
                y_entry.pack(side=tk.RIGHT, padx=(5, 0))
                ttk.Label(frame, text="Y").pack(side=tk.RIGHT)
                x_entry = ttk.Entry(frame, width=10, validate="key",
                                    validatecommand=(self.root.register(self.validate_real_number), '%P'), justify="center")
                x_entry.pack(side=tk.RIGHT, padx=(5, 0))
                ttk.Label(frame, text="X").pack(side=tk.RIGHT)
                entry.append((x_entry, y_entry))
            self.entries.append(entry)
            # Add some vertical space between groups
            # spacer = ttk.Frame(self.scrollable_frame, height=10)
            # spacer.pack(anchor=tk.W, pady=10)


    def Import_data(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            try:
                with open(file_path, 'r') as file:
                    content = file.read().strip()
                    groups = content.split("\n\n")  # Split by empty lines to separate groups

                    # Clear any previous data
                    self.curves = []

                    for group_index, group in enumerate(groups):
                        lines = group.strip().splitlines()
                        if len(lines) < 2:
                            messagebox.showwarning("Warning",
                                                   f"At least two points are required in group {group_index + 1}.")
                            return

                        num_points_in_group = len(lines)
                        self.curves.append(num_points_in_group)  # Append number of points in this group

                    self.create_fields()

                    for group_index, group in enumerate(groups):
                        lines = group.strip().splitlines()
                        for i, line in enumerate(lines):
                            parts = line.strip().split()
                            if len(parts) != 2:
                                messagebox.showwarning("Warning",
                                                       f"Invalid format in line {i + 1} of group {group_index + 1}: {line}")
                                return
                            x_value, y_value = parts
                            self.entries[group_index][i][0].insert(0, x_value)
                            self.entries[group_index][i][1].insert(0, y_value)

                    # Now you can use self.num_points as an array containing number of points in each group
                    print("Number of points in each group:", self.curves)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load file: {e}")

    def Export_data(self):
        # 弹出文件对话框，让用户选择保存位置和文件名
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            try:
                # 打开文件准备写入
                with open(file_path, 'w') as file:
                    # 遍历每组数据
                    for group_index, num_points_in_group in enumerate(self.curves):
                        # 获取当前组的数据
                        group_data = []
                        for i in range(num_points_in_group):
                            # 提取每个点的 x 和 y 值
                            x_value = self.entries[group_index][i][0].get()
                            y_value = self.entries[group_index][i][1].get()
                            # 将 x 和 y 值格式化并添加到组数据中
                            group_data.append(f"{x_value} {y_value}")

                        # 将当前组的数据写入文件，每组数据之间用空行分隔
                        file.write("\n".join(group_data) + "\n\n")

                messagebox.showinfo("Success", "Data exported successfully.")

            except Exception as e:
                messagebox.showerror("Error", f"Failed to export data: {e}")

    def collect_points(self):
        curves_points = []
        for index, group_entries in enumerate(self.entries):
            points = []
            for x_entry, y_entry in group_entries:
                x = x_entry.get()
                y = y_entry.get()
                if not x or not y:
                    messagebox.showerror("Error", "Please enter all the points.")
                    return
                points.append(np.array([float(x), float(y)]))

            if len(points) <= 1:
                messagebox.showerror("Error", "Please enter some points.")
                return

            curves_points.append(points)
        return curves_points

    def plot_curve(self, curves_points=None):
        if curves_points is None:
            curves_points = self.collect_points()

        self.ax.clear()
        t_values = np.linspace(0, 1, 100)
        offset = [(-10, 10), (10, -10)]
        plot_color = ['blue', 'green', 'purple']
        for index, points in enumerate(curves_points):
            curves = [[] for _ in range(len(points) - 1)]

            # 使用 Bernstein 函数计算贝塞尔曲线点
            for t in t_values:
                for n in range(2, len(points)+1):
                    curves[n-2].append([sum([Bernstein_basis(n-1, i, t) * points[i+k] for i in range(0, n)])
                                       for k in range(0, len(points)-n+1)])

            # # 使用 de Casteljau 函数计算贝塞尔曲线点
            # for t in t_values:
            #     curves[0].append([np.array((1 - t) * points[i] + t * points[i + 1]) for i in range(len(points) - 1)])
            #     for i in range(1, len(curves)):
            #         curves[i].append(
            #             [np.array((1 - t) * curves[i - 1][-1][j] + t * curves[i - 1][-1][j + 1])
            #              for j in range(len(curves[i - 1][-1]) - 1)]
            #         )

            for i, point in enumerate(points):
                self.ax.scatter(*point, color='red', s=20)
                self.ax.annotate(f'{chr(80 + index)}{i}', (point[0], point[1]),
                                 textcoords="offset points",
                                 xytext=offset[index % len(offset)], ha='center')

            for i in range(len(curves)):
                for k in range(len(curves[i][0])):
                    c = np.array(curves[i])[:, k]
                    self.ax.plot(c[:, 0], c[:, 1], linestyle='--', linewidth=.7)

            for k in range(len(curves[0][0])):
                c = np.array(curves[0])[:, k]
                self.ax.plot(c[:, 0], c[:, 1], linewidth=.7, color='black')

            c = np.array(curves[-1])[:, 0]
            self.ax.plot(c[:, 0], c[:, 1], linewidth=2, color=plot_color[index%len(plot_color)])

        self.ax.set_xlabel('x')
        self.ax.set_ylabel('y')
        self.ax.set_title('Bezier Curve Generation')
        # 设置网格线的间隔
        self.ax.xaxis.set_major_locator(ticker.MaxNLocator(10))
        self.ax.yaxis.set_major_locator(ticker.MaxNLocator(10))

        # 设置网格线的样式为虚线
        self.ax.grid(True, linestyle='--')

        self.canvas_plot.draw()

        # 绘图完成后保存为PNG文件，设置dpi以提高分辨率
        save_file_path = "./res.png"
        self.figure.savefig(save_file_path, dpi=300, bbox_inches='tight')
        messagebox.showinfo("Info", f"Plot saved as {save_file_path}")

    def connect_curve(self):
        curves_points = self.collect_points()
        # 完成多段Bezier曲线的拼接，确保一阶导数连续性
        for i in range(len(curves_points) - 1):
            # 当前段的最后一个点
            curves_points[i][-1] = curves_points[i + 1][0]

            p3 = curves_points[i][-1]
            # 下一段的第一个点
            q0 = curves_points[i + 1][0]
            # 当前段的倒数第二个点
            p2 = curves_points[i][-2]
            # 下一段的第二个点
            q1 = curves_points[i + 1][1]

            # 确保两段曲线在拼接点处的切线方向相同
            p3_p2_direction = p3 - p2
            new_q1 = q0 + p3_p2_direction
            curves_points[i + 1][1] = new_q1

        self.plot_curve(curves_points)

    def on_closing(self):
        plt.close('all')
        self.root.destroy()

def Bernstein_basis(n, i, t):
    return comb(n, i) * (t ** i) * ((1 - t) ** (n - i))

if __name__ == "__main__":
    root = tk.Tk()
    app = BezierCurveApp(root)
    root.mainloop()
