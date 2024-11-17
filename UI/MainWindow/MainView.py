import tkinter as tk

import networkx as nx
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt


class MainView:
    def __init__(self, root, width, height):
        self.root = root
        self.width = width
        self.height = height
        self.figure, self.ax = plt.subplots(figsize=(8, 6))
        self.ax.set_xlim((0, self.width))
        self.ax.set_ylim((0, self.height))

        self.graph_canvas = FigureCanvasTkAgg(self.figure, master=self.root)
        self.graph_canvas.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        control_frame = tk.Frame(self.root, width=300)
        control_frame.pack(side=tk.RIGHT, fill=tk.Y)

        self.point_listbox = tk.Listbox(control_frame, height=20, width=35)
        self.point_listbox.pack(pady=10)

        self.solve_button = tk.Button(control_frame, text="Solve TSP")
        self.solve_button.pack(pady=5)

        self.legend_canvas = tk.Canvas(control_frame, width=250, height=400)
        self.legend_canvas.pack(pady=5)

    def draw_graph(self, points, routes, colors):
        self.ax.clear()
        self.ax.set_xlim((0, self.width))
        self.ax.set_ylim((0, self.height))

        for x, y in points:
            self.ax.scatter(x, y, c="blue", s=50)

        for i, route in enumerate(routes):
            offset = i * 30

            G = nx.Graph()
            for j, (x, y) in enumerate(route):
                G.add_node(j, pos=(x + offset, y - offset))
                if j > 0:
                    G.add_edge(j - 1, j)
            G.add_edge(len(route) - 1, 0)

            pos = nx.get_node_attributes(G, 'pos')
            nx.draw(G, pos, ax=self.ax, with_labels=True, node_color=colors[i],
                    edge_color=colors[i], node_size=300, font_size=10)

        self.graph_canvas.draw()

    def update_legend(self, legends):
        self.legend_canvas.delete("all")

        for i, (name, color) in enumerate(legends):
            self.legend_canvas.create_rectangle(10, 10 + 30 * i, 30, 30 + 30 * i, fill=color)
            self.legend_canvas.create_text(40, 20 + 30 * i, text=name, anchor=tk.W)
