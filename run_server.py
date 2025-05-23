from pathlib import Path
import json
import flwr as fl
from flwr.server import ServerConfig, Server
from flwr.server.history import History
import fed_avg  # Your custom FedAvg strategy
import custom_client_manager  # Your custom client manager


def main():
    # 1. Define server address
    server_address = "0.0.0.0:8080"  # Listen on all interfaces on port 8080

    # 2. Define federated learning hyperparameters
    num_rounds = 5  # As specified in the assignment
    min_available_clients = 2  # Minimum number of clients required
    
    print(f"Starting Flower server on {server_address}")
    print(f"Number of rounds: {num_rounds}")
    print(f"Waiting for at least {min_available_clients} clients to connect...")

    # 3. Instantiate ClientManager 
    client_manager = custom_client_manager.CustomClientManager()
    
    # 4. Configure the strategy with proper minimums
    strategy = fed_avg.FedAvgStrategy(
        min_fit_clients=min_available_clients,
        min_evaluate_clients=min_available_clients,
        min_available_clients=min_available_clients
    )
    
    # 5. Configure server
    config = ServerConfig(num_rounds=num_rounds)

    # 6. Start the Flower server
    try:
        # Start server and wait for completion
        history = fl.server.start_server(
            server_address=server_address,
            config=config,
            strategy=strategy,
            client_manager=client_manager
        )

        print("Training completed! Saving results...")

        # 7. Extract history info
        losses_distributed = history.losses_distributed
        metrics_distributed_fit = history.metrics_distributed_fit
        metrics_distributed = history.metrics_distributed

        # 8. Save results as JSON
        results = {
            "losses_distributed": losses_distributed,
            "metrics_distributed_fit": metrics_distributed_fit,
            "metrics_distributed": metrics_distributed,
        }
        
        save_path = Path("fl_history.json")
        with open(save_path, "w") as f:
            json.dump(results, f, indent=4)

        print(f"Training history saved to {save_path}")
        
    except KeyboardInterrupt:
        print("\nServer stopped by user.")
    except Exception as e:
        print(f"Error running server: {e}")


if __name__ == "__main__":
    main()