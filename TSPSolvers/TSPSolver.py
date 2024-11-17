from abc import ABC, abstractmethod

class TSPSolver(ABC):
    """
    Abstract class
    Superclass for all types of TSP solvers (NeuralSolver, NonNeuralSolver)

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
