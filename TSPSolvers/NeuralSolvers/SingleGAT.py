import torch
import torch.nn as nn
from torch import optim
from torch_geometric.nn import GATConv
import numpy as np
from scipy.spatial import distance_matrix

from TSPSolvers.NeuralSolvers import NeuralSolver


class SingleGAT(nn.Module, NeuralSolver):
    def __init__(self,
                 in_channels: int,
                 out_channels: int,
                 heads: int = 4,
                 alpha: float = 0.5):
        super(SingleGAT, self).__init__()

        self.in_channels = in_channels
        self.out_channels = out_channels
        self.alpha = alpha

        self.gat = GATConv(in_channels, out_channels, heads=heads, concat=False)
        self.fc = nn.Linear(out_channels, 1)

    def __name__(self):
        return f"SingleGAT({self.in_channels}x{self.out_channels}, {self.alpha})"

    def __forward(self, x, edge_index):
        x = self.gat(x, edge_index)
        x = torch.relu(x)

        return x

    def solve_tsp(self,
                  points: list[(float, float)]):
        x = torch.tensor(points, dtype=torch.float)
        n = len(points)

        dist_matrix = distance_matrix(points, points)
        edges = np.array(np.nonzero(dist_matrix)).T
        edge_index = torch.tensor(edges, dtype=torch.long).t().contiguous()

        embeddings = self.__forward(x, edge_index)
        scores = self.fc(embeddings).squeeze().detach().numpy()

        route = [0]
        visited = set(route)
        total_distance = 0

        for _ in range(1, n):
            last = route[-1]
            combined_scores = dist_matrix[last] + self.alpha * 1000.0 * scores
            nearest = np.argmin([combined_scores[i] if i not in visited else np.inf for i in range(n)])
            route.append(nearest)
            visited.add(nearest)
            total_distance += dist_matrix[last, nearest]

        total_distance += dist_matrix[route[-1], route[0]]

        return [points[i] for i in route], total_distance

    def train_model(self, train_data, epochs=100, lr=0.001):
        optimizer = optim.Adam(self.parameters(), lr=lr)
        loss_fn = nn.MSELoss()

        for epoch in range(epochs):
            total_loss = 0
            for points, target_distance in train_data:
                self.train()

                x = torch.tensor(points, dtype=torch.float)

                dist_matrix = distance_matrix(points, points)
                edges = np.array(np.nonzero(dist_matrix)).T
                edge_index = torch.tensor(edges, dtype=torch.long).t().contiguous()

                optimizer.zero_grad()

                embeddings = self.__forward(x, edge_index)
                predicted_scores = self.fc(embeddings).squeeze()

                _, predicted_distance = self.solve_tsp(points)
                loss = loss_fn(predicted_scores.sum(),  # Використання безпосередньо обчисленого значення
                               torch.tensor(target_distance, dtype=torch.float, requires_grad=False))

                loss.backward()
                optimizer.step()

                total_loss += loss.item()
            print(f"Epoch {epoch + 1}, Loss: {total_loss:.4f}")