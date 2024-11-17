from abc import abstractmethod

from TSPSolvers.TSPSolver import TSPSolver


class NonNeuralSolver(TSPSolver):
    """
    Abstract class
    Superclass for all non-neural TSP solvers

    Contains 2 methods that should contain all subclasses:
    - __name__()
    - solve_tsp(points)
    """

    @abstractmethod
    def __name__(self):
        pass

    @abstractmethod
    def solve_tsp(self, points):
        pass