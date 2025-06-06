# TP1

## Step 1
Data generation is taken care of by the `generate_data.py` and data loading is taken care of by the `load.py` file. Newly generated data is saved to the `client_data` folder  

The `generate_distributed_datasets` function creates a directory to save the datasets to if it is not already created, takes the dataset name variable set in the `config` file and checks if it is a valid name, transforms the dataset, shuffles & splits it based on the alpha value, and creates as many .csv datasets as there are clients.  

The `load_client_data` function loads the datasets from the directory where they were saved to, normalizes & reshapes them, and splits them into a train/test split. It then transforms them to tensors and combines the tensors and ultimately, loaders.  

## Step 2
This is taken care of by the `model.py` file  

This model has 2 CNN layers.  

The `train_epoch` function calls the train function, initializes metrics to 0, creates a zero gradient, gets loss values, and starts going through the data. it then aggregates metrics until the testing is completed. From here, it then returns the metrics.  

The `test_epoch` function does the testing on unseen data. it initializes metrics to 0, creates a zero gradient, and tries predicting on the unseen data. It finally aggreagates metrics and returns them.  

## Step 3
This is taken care of by the `client.py` file  

The `fit` function calls the train method on the model and does training for the set number of epochs in the `config` file. it gets the metrics from the `train_epoch` method and returns metrics after the epochs are done.  

The `evaluate` function calls the `test_epoch` method and returns the metrics.  

## Step 4
This is taken care of by the `run_client.py` file. The command `python3 run_client.py --cid INTEGER` will run the client. The server must be running or else the client will fail.  

the `run_client.py` file had added `--cid` and `--server` arguments. `--server` is optional and lets the user enter a custom IP address to connect to. `--cid` sets the client id number. This file calls the `load_client_data` function to load in the data and creates the model and client. It then finally starts the client.  

## Step 5
The client manager is taken care of by the `custom_client_manager.py` file and the strategy is taken care of by the `fed_avg.py` file.  

The client manager has a dictionary where it stores the registered clients in a dictionary by their ID number. The `register` function adds the client to the dictionary and `unregister` function removes the client from the dictionary. The `wait_for` function sets a timeout for the server to let clients connect. The `sample` function returns a group of clients.  

The `configure_fit` and `configure_evaluate` functions get the larger of the min number of clients, or a fraction of the amount of clients connected to the server and returns the response from the `sample` function.  

The `aggregate_fit` function aggregates the weight results. It gets the weight results, combines them, and does a weighted average on them.  

The `aggregate_evaluate` function does the same as `aggregate_fit` but for testing data instead of training data.  

## Step 6
The server is contained in the `run_server.py` file. The following command runs the server `python3 run_server.py`  

Running this file creates the datasets, sets the server address, and imports number of rounds from the `config` file. It then imports the custom client manager and sets the Fed AVG strategy. From there, it then configures the server and tries to run it. Finally, it gets the history and saves it to a file name `fl_history.json`. 

## Step 7
This is taken care of by the `run_visualizer.py` file. The following command runs the data visualization: `python3 run_visualizer.py  --output NAME_OF_OUTPUT`  

Results are saved to the `plots` folder and end with what the user has enetered for NAME_OF_OUTPUT. The title of each plots also contains the NAME_OF_OUTPUT string

## Step 8
Hyperparameters are saved to the `config.py`  
In order to run the simulation, Multiple terminal tabs need to be opened. Each terminal will need to run the virtual environment in the folder. Complete the following steps to run the simulation
1. Open terminal and run `source venv/bin/activate` to run the Python virtual environment  
2. Run `python3 run_server.py`. The server will now be waiting for the specified number of clients to connect
3. Open as many terminal tabs as clients are required
4. In each newly opened terminal, run the following commands:
    1. `source venv/bin/activate` to run the Python virtual environment  
    2. `python3 run_client.py --cid INTEGER` making sure to change the CID Integer for each client  
5. Wait for the tests to complete
6. Run `python3 run_visualizer.py --output NAME_OF_OUTPUT` to generate the images for reporting  

### Simulation 1
Num of clients: 10  
Alpha: 1  
Rounds: 30  
Epochs: 1  
Dataset: Fashion MNIST  
Batch size: 32  
Learning Rate: 0.01  
[![Image 1](plots/accuracy_eval_plot_10_clients_30_rounds_1_epoch_1_alpha.png)](plots/accuracy_eval_plot_10_clients_30_rounds_1_epoch_1_alpha.png)
[![Image 2](plots/accuracy_fit_plot_10_clients_30_rounds_1_epoch_1_alpha.png)](plots/accuracy_fit_plot_10_clients_30_rounds_1_epoch_1_alpha.png)
[![Image 3](plots/loss_fit_plot_10_clients_30_rounds_1_epoch_1_alpha.png)](plots/loss_fit_plot_10_clients_30_rounds_1_epoch_1_alpha.png)
[![Image 4](plots/losses_distributed_plot_10_clients_30_rounds_1_epoch_1_alpha.png)](plots/losses_distributed_plot_10_clients_30_rounds_1_epoch_1_alpha.png)

Since this is our first simulation and it uses all the given hyper parameters, we will use this as a baseline for future simulations.  

### Simulation 2
Num of clients: 10  
Alpha: 5  
Rounds: 30  
Epochs: 1  
Dataset: Fashion MNIST  
Batch size: 32  
Learning Rate: 0.01   
[![Image 1](plots/accuracy_eval_plot_10_clients_30_rounds_1_epoch_5_alpha.png)](plots/accuracy_eval_plot_10_clients_30_rounds_1_epoch_5_alpha.png)
[![Image 2](plots/accuracy_fit_plot_10_clients_30_rounds_1_epoch_5_alpha.png)](plots/accuracy_fit_plot_10_clients_30_rounds_1_epoch_5_alpha.png)
[![Image 3](plots/loss_fit_plot_10_clients_30_rounds_1_epoch_5_alpha.png)](plots/loss_fit_plot_10_clients_30_rounds_1_epoch_5_alpha.png)
[![Image 4](plots/losses_distributed_plot_10_clients_30_rounds_1_epoch_5_alpha.png)](plots/losses_distributed_plot_10_clients_30_rounds_1_epoch_5_alpha.png)

In this simulation, I kept all parameters the same but increased the Alpha from 1 to 5. We can see that learning is slightly more stable than before which makes sense due to the increased homogenity in the datasets as a direct result from the increase in Alpha. With more overlapping data, we expect the local minima of each client to be closer than before, leading to less variation in the plot history. This is most prominent on the Accuracy Evaluation plot.  

### Simulation 3
Num of clients: 10  
Alpha: 1  
Rounds: 30  
Epochs: 3  
Dataset: Fashion MNIST  
Batch size: 32  
Learning Rate: 0.01  
[![Image 1](plots/accuracy_eval_plot_10_clients_30_rounds_3_epochs_1_alpha.png)](plots/accuracy_eval_plot_10_clients_30_rounds_3_epochs_1_alpha.png)
[![Image 2](plots/accuracy_fit_plot_10_clients_30_rounds_3_epochs_1_alpha.png)](plots/accuracy_fit_plot_10_clients_30_rounds_3_epochs_1_alpha.png)
[![Image 3](plots/loss_fit_plot_10_clients_30_rounds_3_epochs_1_alpha.png)](plots/loss_fit_plot_10_clients_30_rounds_3_epochs_1_alpha.png)
[![Image 4](plots/losses_distributed_plot_10_clients_30_rounds_3_epochs_1_alpha.png)](plots/losses_distributed_plot_10_clients_30_rounds_3_epochs_1_alpha.png)

In this simulation, I kept all parameters the same from the 1st simulation but increased the Epoch count from 1 to 3. The learning appears to also be slightly more stable than the baseline, potentially due to the fact that the higher epoch count gives the clients more instances to train the model and adjust the weights. I was expecting there to be more client drift, giving plots with more variations but that was not the case in this simulation.  

### Simulation 4
num of clients: 5  
alpha: 1  
rounds: 30  
epoch: 3  
[![Image 1](plots/accuracy_eval_plot_5_clients_30_rounds_3_epochs_1_alpha.png)](plots/accuracy_eval_plot_5_clients_30_rounds_3_epochs_1_alpha.png)
[![Image 2](plots/accuracy_fit_plot_5_clients_30_rounds_3_epochs_1_alpha.png)](plots/accuracy_fit_plot_5_clients_30_rounds_3_epochs_1_alpha.png)
[![Image 3](plots/loss_fit_plot_5_clients_30_rounds_3_epochs_1_alpha.png)](plots/loss_fit_plot_5_clients_30_rounds_3_epochs_1_alpha.png)
[![Image 4](plots/losses_distributed_plot_5_clients_30_rounds_3_epochs_1_alpha.png)](plots/losses_distributed_plot_5_clients_30_rounds_3_epochs_1_alpha.png)

In this simulation, I kept all parameters the same from the 3rd simulation but decreased the Client count from 10 to 5. This made the learning more unstable which isn't too surprising, as we have fewer gradients than before and a low alpha, so we can expect any client drift to have a larger effect on the model than before. Surprisingly though, the simulations ends up giving similar end results compared to simulation 3.  