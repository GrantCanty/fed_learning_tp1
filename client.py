import numpy as np
import flwr

from flwr.common import (
    GetPropertiesIns, GetPropertiesRes,
    GetParametersIns, GetParametersRes,
    FitIns, FitRes,
    EvaluateIns, EvaluateRes,
    Code, Status,
    ndarrays_to_parameters, parameters_to_ndarrays
)

from typing import List
import torch

class CustomClient(flwr.client.Client):
    def __init__(self, model: torch.nn.Module, train_loader,
                 test_loader, device: torch.device) -> None:
        self.model = model
        self.train_loader = train_loader
        self.test_loader = test_loader
        self.device = device

    def get_properties(self, instruction: GetPropertiesIns) -> GetPropertiesRes:
        return GetPropertiesRes(
            status=Status(code=Code.OK, message="Success"),
            properties={"framework": "pytorch", "dataset": "FashionMNIST"}
        )

    def get_parameters(self, instruction: GetParametersIns) -> GetParametersRes:
        weights: List[np.ndarray] = self.model.get_model_parameters()
        return GetParametersRes(
            status=Status(code=Code.OK, message="Success"),
            parameters=ndarrays_to_parameters(weights)
        )

    def fit(self, instruction: FitIns) -> FitRes:
        # Set model parameters from server
        params = parameters_to_ndarrays(instruction.parameters)
        self.model.set_model_parameters(params)

        # Training
        criterion = torch.nn.CrossEntropyLoss()
        optimizer = torch.optim.Adam(self.model.parameters(), lr=0.001)
        self.model.to(self.device)
        train_loss, train_accuracy = self.model.train_epoch(
            self.train_loader, criterion, optimizer, self.device
        )

        # Return updated parameters
        updated_weights = self.model.get_model_parameters()
        return FitRes(
            status=Status(code=Code.OK, message="Trained successfully"),
            parameters=ndarrays_to_parameters(updated_weights),
            num_examples=len(self.train_loader.dataset),
            metrics={"train_loss": train_loss, "train_accuracy": train_accuracy}
        )

    def evaluate(self, instruction: EvaluateIns) -> EvaluateRes:
        # Set model parameters from server
        params = parameters_to_ndarrays(instruction.parameters)
        self.model.set_model_parameters(params)

        # Evaluation
        criterion = torch.nn.CrossEntropyLoss()
        self.model.to(self.device)
        test_loss, test_accuracy = self.model.test_epoch(
            self.test_loader, criterion, self.device
        )

        return EvaluateRes(
            status=Status(code=Code.OK, message="Evaluated successfully"),
            loss=test_loss,
            num_examples=len(self.test_loader.dataset),
            metrics={"accuracy": test_accuracy}
        )

    def to_client(self) -> "CustomClient":
        return self