from UI.MainWindow.MainView import MainView
from UI.colors import generate_colors, rgba_to_hex


class MainController:
    def __init__(self, root, solvers, width=600, height=400):
        self.view = MainView(root, width, height)

        self.solvers = solvers
        self.points = []
        self.colors = generate_colors(len(self.solvers))
        self.current_graph_index = 0
        self.routes = []

        self.view.solve_button.config(command=self.solve_tsp)
        self.view.graph_canvas.mpl_connect("button_press_event", self.add_or_remove_point)
        self.view.prev_button.config(command=self.show_previous_graph)
        self.view.next_button.config(command=self.show_next_graph)

    def add_or_remove_point(self, event):
        if event.button == 1:
            x, y = event.xdata, event.ydata
            if x is not None and y is not None:
                self.points.append((x, y))
                self.view.point_listbox.insert("end", f"({x:.2f}, {y:.2f})")
        elif event.button == 3:
            if self.points:
                closest_idx = self.get_closest_point_index(event.xdata, event.ydata)
                if closest_idx is not None:
                    self.points.pop(closest_idx)
                    self.view.point_listbox.delete(closest_idx)

        self.routes = []
        self.current_graph_index = 0
        self.update_graph()

    def get_closest_point_index(self, x, y):
        if x is None or y is None or not self.points:
            return None
        distances = [(i, (px - x) ** 2 + (py - y) ** 2) for i, (px, py) in enumerate(self.points)]
        return min(distances, key=lambda item: item[1])[0]

    def solve_tsp(self):
        if len(self.points) < 2:
            return

        self.routes = []
        legends = []
        for solver, color in zip(self.solvers, self.colors):
            if hasattr(solver, 'max_points') and len(self.points) > solver.max_points:
                continue
            else:
                try:
                    route, length = solver.solve_tsp(self.points)
                    self.routes.append(route)
                    legends.append((f"{solver.__name__()} \t({length:.2f})", rgba_to_hex(color)))
                except Exception as e:
                    print(f"Solver failed: {e}")

        self.current_graph_index = 0
        self.update_graph()
        self.view.update_legend(legends)

    def update_graph(self):
        if not self.routes:
            self.view.draw_graph(self.points, [], self.colors)
        else:
            self.view.draw_graph(self.points, self.routes, self.colors, self.current_graph_index)

    def show_previous_graph(self):
        if self.routes:
            self.current_graph_index = (self.current_graph_index - 1) % len(self.routes)
            self.update_graph()

    def show_next_graph(self):
        if self.routes:
            self.current_graph_index = (self.current_graph_index + 1) % len(self.routes)
            self.update_graph()