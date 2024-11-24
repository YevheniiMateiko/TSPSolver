import json
import numpy as np

from TSPSolvers.NonNeuralSolvers import BruteForceSolver


def generate_random_routes(num_routes: int, num_points: int):
    routes = []
    for _ in range(num_routes):
        points = np.random.rand(num_points, 2) * 400
        routes.append(points.tolist())
    return routes


def save_solutions_to_file(routes, solver, filename="training_data.json"):
    data = []
    for points in routes:
        best_route, distance = solver.solve_tsp(points)
        data.append({
            "route": best_route,
            "distance": distance
        })

    with open(filename, "w") as file:
        json.dump(data, file, indent=4)


if __name__ == "__main__":
    brute_force_solver = BruteForceSolver(max_points=8)

    num_routes = 50
    num_points = brute_force_solver.max_points
    routes = generate_random_routes(num_routes, num_points)

    save_solutions_to_file(routes, brute_force_solver)