"""
from prefect import flow
from prefect.task_runners import SequentialTaskRunner
from prefect_databricks import DatabricksCredentials
from prefect_databricks.jobs import jobs_runs_submit

@flow(name="MNIST Training Flow",log_prints=True)
def train_mnist():
    print("Beginning Training for MNIST!")
    databricks_credentials = DatabricksCredentials.load("databricks")
    job = jobs_runs_submit(databricks_credentials=databricks_credentials,run_name="TrainOnDatabricks")

if __name__ == "__main__":
    train_mnist()

"""

from prefect import flow
from prefect_databricks import DatabricksCredentials
from prefect_databricks.jobs import jobs_list


@flow
def example_execute_endpoint_flow():
    databricks_credentials = DatabricksCredentials.load("databricks")
    jobs = jobs_list(
        databricks_credentials,
        limit=5
    )
    return jobs

example_execute_endpoint_flow()

"""
from prefect_databricks import DatabricksCredentials

credentials = DatabricksCredentials(
    databricks_instance="https://adb-1813648540267587.7.azuredatabricks.net/",
    token="dapi4fa0bf749f7553e9e602c36846371505-2"
    )

credentials.save("databricks")
"""