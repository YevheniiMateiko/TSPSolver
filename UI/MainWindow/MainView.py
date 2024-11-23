import tkinter as tk
import networkx as nx
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt


class MainView:
    def __init__(self,
                 root,
                 width: int,
                 height: int):
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

        button_frame = tk.Frame(control_frame)
        button_frame.pack(pady=10)

        self.prev_button = tk.Button(button_frame, text="←", width=5)
        self.prev_button.pack(side=tk.LEFT, padx=(5, 10))

        self.solve_button = tk.Button(button_frame, text="Solve TSP", width=10)
        self.solve_button.pack(side=tk.LEFT, padx=(10, 10))

        self.next_button = tk.Button(button_frame, text="→", width=5)
        self.next_button.pack(side=tk.LEFT, padx=(10, 5))

        self.legend_canvas = tk.Canvas(control_frame, width=250, height=400)
        self.legend_canvas.pack(pady=5)

    def draw_graph(self, points, routes, colors, current_index=0):
        self.ax.clear()
        self.ax.set_xlim((0, self.width))
        self.ax.set_ylim((0, self.height))

        for x, y in points:
            self.ax.scatter(x, y, c="blue", s=50)

        if 0 <= current_index < len(routes):
            route = routes[current_index]
            color = colors[current_index]

            graph = nx.Graph()
            for j, (x, y) in enumerate(route):
                graph.add_node(j, pos=(x, y))
                if j > 0:
                    graph.add_edge(j - 1, j)
            graph.add_edge(len(route) - 1, 0)

            pos = nx.get_node_attributes(graph, 'pos')
            nx.draw(graph, pos, ax=self.ax, with_labels=True, node_color=color,
                    edge_color=color, node_size=300, font_size=10)

        self.graph_canvas.draw()

    def update_legend(self, legends):
        self.legend_canvas.delete("all")

        for i, (name, color) in enumerate(legends):
            self.legend_canvas.create_rectangle(10, 10 + 30 * i, 30, 30 + 30 * i, fill=color)
            self.legend_canvas.create_text(40, 20 + 30 * i, text=name, anchor=tk.W)