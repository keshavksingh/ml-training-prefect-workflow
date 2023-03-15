from prefect import flow, task
from prefect.deployments import Deployment

@task
def speak(message: str):
    print(message)


@flow(log_prints=True)
def hi():
    print("Hi from Prefect! 🤗")
    speak(message="Hi from Prefect! 🤗")

if __name__=="__main__":
    hi()

#deployment = Deployment.build_from_flow(
#    flow=hi,
#    name="prefect-example-deployment",
#)

#deployment.apply()