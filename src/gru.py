"""GRU model and training helpers.

This module intentionally contains all PyTorch imports so the classical
baselines in ``src.models`` remain usable before PyTorch is installed.
"""

from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass

import numpy as np
import torch
from torch import nn
from torch.utils.data import DataLoader, Dataset


class SequenceDataset(Dataset):
    """PyTorch dataset for precomputed sequence windows."""

    def __init__(self, x: np.ndarray, y: np.ndarray) -> None:
        self.x = torch.as_tensor(x, dtype=torch.float32)
        self.y = torch.as_tensor(y, dtype=torch.float32).reshape(-1, 1)

    def __len__(self) -> int:
        return len(self.x)

    def __getitem__(self, index: int) -> tuple[torch.Tensor, torch.Tensor]:
        return self.x[index], self.y[index]


class GRURegressor(nn.Module):
    """Many-to-one GRU for predicting one future target value."""

    def __init__(
        self,
        input_size: int,
        hidden_size: int = 64,
        num_layers: int = 2,
        dropout: float = 0.2,
    ) -> None:
        super().__init__()
        gru_dropout = dropout if num_layers > 1 else 0.0
        self.gru = nn.GRU(
            input_size=input_size,
            hidden_size=hidden_size,
            num_layers=num_layers,
            dropout=gru_dropout,
            batch_first=True,
        )
        self.head = nn.Sequential(
            nn.LayerNorm(hidden_size),
            nn.Linear(hidden_size, hidden_size // 2),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(hidden_size // 2, 1),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        sequence, _ = self.gru(x)
        return self.head(sequence[:, -1, :])


@dataclass(frozen=True)
class TrainingResult:
    """Training history returned by ``train_gru``."""

    train_loss: list[float]
    validation_loss: list[float]
    best_epoch: int


def _mean_loader_loss(
    model: nn.Module,
    loader: DataLoader,
    loss_fn: nn.Module,
    device: torch.device,
) -> float:
    model.eval()
    total_loss = 0.0
    total_rows = 0
    with torch.no_grad():
        for x_batch, y_batch in loader:
            x_batch = x_batch.to(device)
            y_batch = y_batch.to(device)
            batch_loss = loss_fn(model(x_batch), y_batch)
            total_loss += float(batch_loss.item()) * len(x_batch)
            total_rows += len(x_batch)
    return total_loss / max(total_rows, 1)


def train_gru(
    model: GRURegressor,
    train_loader: DataLoader,
    validation_loader: DataLoader,
    epochs: int = 50,
    learning_rate: float = 1e-3,
    patience: int = 8,
    device: str | torch.device | None = None,
) -> TrainingResult:
    """Train a GRU with validation-based early stopping."""
    resolved_device = torch.device(
        device or ("cuda" if torch.cuda.is_available() else "cpu")
    )
    model.to(resolved_device)
    loss_fn = nn.MSELoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

    train_history: list[float] = []
    validation_history: list[float] = []
    best_validation = float("inf")
    best_epoch = 0
    best_state = deepcopy(model.state_dict())
    epochs_without_improvement = 0

    for epoch in range(1, epochs + 1):
        model.train()
        total_loss = 0.0
        total_rows = 0

        for x_batch, y_batch in train_loader:
            x_batch = x_batch.to(resolved_device)
            y_batch = y_batch.to(resolved_device)

            optimizer.zero_grad()
            loss = loss_fn(model(x_batch), y_batch)
            loss.backward()
            optimizer.step()

            total_loss += float(loss.item()) * len(x_batch)
            total_rows += len(x_batch)

        train_loss = total_loss / max(total_rows, 1)
        validation_loss = _mean_loader_loss(
            model, validation_loader, loss_fn, resolved_device
        )
        train_history.append(train_loss)
        validation_history.append(validation_loss)

        if validation_loss < best_validation:
            best_validation = validation_loss
            best_epoch = epoch
            best_state = deepcopy(model.state_dict())
            epochs_without_improvement = 0
        else:
            epochs_without_improvement += 1
            if epochs_without_improvement >= patience:
                break

    model.load_state_dict(best_state)
    return TrainingResult(train_history, validation_history, best_epoch)


def predict_gru(
    model: GRURegressor,
    loader: DataLoader,
    device: str | torch.device | None = None,
) -> np.ndarray:
    """Generate ordered predictions from a non-shuffled DataLoader."""
    resolved_device = torch.device(
        device or ("cuda" if torch.cuda.is_available() else "cpu")
    )
    model.to(resolved_device)
    model.eval()
    predictions: list[np.ndarray] = []

    with torch.no_grad():
        for x_batch, _ in loader:
            output = model(x_batch.to(resolved_device))
            predictions.append(output.cpu().numpy().reshape(-1))

    return np.concatenate(predictions)
