from UI.MainWindow.MainView import MainView
from UI.colors import generate_colors, rgba_to_hex


class MainController:
    def __init__(self, root, solvers, width = 600, height = 400):
        self.view = MainView(root, width, height)

        self.solvers = solvers
        self.points = []
        self.colors = generate_colors(len(self.solvers))

        self.view.solve_button.config(command=self.solve_tsp)

        self.view.graph_canvas.mpl_connect("button_press_event", self.add_or_remove_point)

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
        self.update_graph([])

    def get_closest_point_index(self, x, y):
        if x is None or y is None or not self.points:
            return None
        distances = [(i, (px - x) ** 2 + (py - y) ** 2) for i, (px, py) in enumerate(self.points)]
        return min(distances, key=lambda item: item[1])[0]

    def solve_tsp(self):
        if len(self.points) < 2:
            return

        routes = []
        legends = []
        for solver, color in zip(self.solvers, self.colors):
            if hasattr(solver, 'max_points') and len(self.points) > solver.max_points:
                continue
            else:
                try:
                    route, length = solver.solve_tsp(self.points)
                    routes.append(route)
                    legends.append((f"{solver.__name__()} \t({length:.2f})", rgba_to_hex(color)))
                except Exception as e:
                    print(f"Solver failed: {e}")

        self.update_graph(routes)
        self.view.update_legend(legends)

    def update_graph(self, routes):
        self.view.draw_graph(self.points, routes, self.colors)
