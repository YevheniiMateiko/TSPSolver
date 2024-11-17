from scipy.spatial.distance import cdist

from TSPSolvers.NonNeuralSolvers import NonNeuralSolver


class NearestNeighborSolver(NonNeuralSolver):
    def __init__(self):
        pass

    def __name__(self):
        return "NearestNeighborSolver"

    def solve_tsp(self, points):
        dist_matrix = cdist(points, points)

        n = len(points)
        visited = set()
        route = [0]
        visited.add(0)
        total_distance = 0

        for _ in range(1, n):
            last = route[-1]
            distances = dist_matrix[last]

            nearest = min(
                (i for i in range(n) if i not in visited),
                key=lambda i: distances[i]
            )

            route.append(nearest)
            visited.add(nearest)
            total_distance += distances[nearest]

        total_distance += dist_matrix[route[-1], route[0]]
        route.append(0)

        return [points[i] for i in route], total_distance
