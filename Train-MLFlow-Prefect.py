from prefect import flow, task
from prefect.task_runners import SequentialTaskRunner
import argparse
import tensorflow as tf
from tensorflow import keras
import mlflow
import mlflow.keras
import os

os.environ['AZURE_STORAGE_ACCESS_KEY'] ="XXXXXXXXXXXXXXX"

@task(name="MNIST Task Prefect-AKS-MLFlow")
def task_train_mnist():

    parser = argparse.ArgumentParser()
    parser.add_argument('--epochs', type=int, default=10, help='Number of epochs to train for')
    parser.add_argument('--batch_size', type=int, default=128, help='Batch size for training')
    parser.add_argument('--learning_rate', type=float, default=0.001, help='Learning rate for optimizer')
    parser.add_argument('--dropout_rate', type=float, default=0.25, help='Dropout rate for regularization')
    args = parser.parse_args()

    # Load MNIST dataset
    (x_train, y_train), (x_test, y_test) = keras.datasets.mnist.load_data()
    x_train = x_train.astype('float32') / 255.0
    x_test = x_test.astype('float32') / 255.0
    y_train = keras.utils.to_categorical(y_train)
    y_test = keras.utils.to_categorical(y_test)

    # Define model architecture
    model = keras.Sequential([
        keras.layers.Flatten(input_shape=(28, 28)),
        keras.layers.Dense(128, activation='relu'),
        keras.layers.Dropout(args.dropout_rate),
        keras.layers.Dense(10, activation='softmax')
    ])
    model.compile(optimizer=tf.optimizers.Adam(lr=args.learning_rate),
                loss='categorical_crossentropy',
                metrics=['accuracy'])
    # Set MLFlow tracking server URL
    model_name="MNIST-Model"
    mlflow.set_tracking_uri("http://mlflowserver-aci-latest-dnsname.eastus.azurecontainer.io:5000")
    mlflow.set_experiment("MNIST-Prefect-AKS-MLFlow-ADLS")

    # Start MLFlow tracking
    with mlflow.start_run() as run:
        # Log parameters
        mlflow.log_param('epochs', args.epochs)
        mlflow.log_param('batch_size', args.batch_size)
        mlflow.log_param('learning_rate', args.learning_rate)
        mlflow.log_param('dropout_rate', args.dropout_rate)

    mlflow.keras.log_model(model,model_name)
    mlflow.end_run()

@flow(name="MNIST Traning Flow Prefect-AKS-MLFlow"
      #,description="MNIST Flow using SequentialTaskRunner"
      #,task_runner=SequentialTaskRunner()
      ,log_prints=True)
def train_mnist():
    print("Beginning Traning for MNIST! Traning on AKS Tracking MLFlow Workflow Prefect")
    task_train_mnist()


if __name__ == "__main__":
    train_mnist()