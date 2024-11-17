import tkinter as tk

from torch_geometric.nn import nearest

from TSPSolvers.NeuralSolvers import DynamicGAT, SingleGAT
from TSPSolvers.NonNeuralSolvers import BruteForceSolver, NearestNeighborSolver
from UI.MainWindow import MainController

if __name__ == "__main__":
    dynamic_gat_solver_2_16_8_4k = DynamicGAT(in_channels = 2, hidden_channels = 16, out_channels = 8, alpha = 1)
    dynamic_gat_solver_2_16_8_64k = DynamicGAT(in_channels=2, hidden_channels=16, out_channels=8, alpha=64)
    dynamic_gat_solver_2_48_16_4k = DynamicGAT(in_channels=2, hidden_channels=48, out_channels=16, alpha=1)
    dynamic_gat_solver_2_48_16_64k = DynamicGAT(in_channels=2, hidden_channels=48, out_channels=16, alpha=64)
    single_gat_solver_0 = SingleGAT(in_channels = 2, out_channels = 8, alpha = 1)
    single_gat_solver_64 = SingleGAT(in_channels=2, out_channels=8, alpha=64)
    nearest_neighbor_solver = NearestNeighborSolver()
    brute_force_solver = BruteForceSolver(max_points=9)

    solvers = (
        dynamic_gat_solver_2_16_8_4k,
        dynamic_gat_solver_2_16_8_64k,
        dynamic_gat_solver_2_48_16_4k,
        dynamic_gat_solver_2_48_16_64k,
        single_gat_solver_0,
        single_gat_solver_64,
        nearest_neighbor_solver,
        brute_force_solver
    )

    root = tk.Tk()
    app = MainController(root=root, solvers=solvers)
    root.mainloop()
