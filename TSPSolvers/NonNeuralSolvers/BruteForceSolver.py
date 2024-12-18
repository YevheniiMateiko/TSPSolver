from itertools import permutations

from numpy import ndarray
from scipy.spatial.distance import cdist

from TSPSolvers.NonNeuralSolvers import NonNeuralSolver


class BruteForceSolver(NonNeuralSolver):
    def __init__(self,
                 max_points: int = 8):
        self.max_points = max_points

    def __name__(self):
        return f"BruteForceSolver({self.max_points})"

    @staticmethod
    def __calculate_route_distance(route: list[(float, float)],
                                   dist_matrix: ndarray):
        distance = 0
        for i in range(len(route) - 1):
            distance += dist_matrix[route[i], route[i + 1]]

        distance += dist_matrix[route[-1], route[0]]
        return distance

    def solve_tsp(self, points):
        dist_matrix = cdist(points, points)

        min_distance = float('inf')
        best_route = None

        for perm in permutations(range(len(points))):
            route = list(perm)

            distance = self.__calculate_route_distance(route, dist_matrix)

            if distance < min_distance:
                min_distance = distance
                best_route = route

        return [points[i] for i in best_route], min_distance
