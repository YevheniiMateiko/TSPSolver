import json
import tkinter as tk

from TSPSolvers.NeuralSolvers import DynamicGAT, SingleGAT
from TSPSolvers.NonNeuralSolvers import BruteForceSolver, NearestNeighborSolver
from UI.MainWindow import MainController

def load_training_data(filename="training_data.json"):
    with open(filename, "r") as file:
        data = json.load(file)
    train_data = []
    for entry in data:
        train_data.append((entry["route"], entry["distance"]))
    return train_data

if __name__ == "__main__":
    training_data = load_training_data("training_data.json")

    dynamic_gat_solver_trained = DynamicGAT(in_channels = 2, hidden_channels = 16, out_channels = 8, alpha = 64)
    dynamic_gat_solver_trained.train_model(training_data)

    dynamic_gat_solver_untrained = DynamicGAT(in_channels = 2, hidden_channels = 16, out_channels = 8, alpha = 64)

    single_gat_solver_trained = SingleGAT(in_channels = 2, out_channels = 8, alpha = 64)
    single_gat_solver_trained.train_model(training_data)

    single_gat_solver_untrained = SingleGAT(in_channels = 2, out_channels = 8, alpha = 64)

    nearest_neighbor_solver = NearestNeighborSolver()
    brute_force_solver = BruteForceSolver(max_points=9)

    solvers = (
        dynamic_gat_solver_trained,
        dynamic_gat_solver_untrained,
        single_gat_solver_trained,
        single_gat_solver_untrained,
        nearest_neighbor_solver,
        brute_force_solver
    )

    root = tk.Tk()
    app = MainController(root=root, solvers=solvers)
    root.mainloop()
