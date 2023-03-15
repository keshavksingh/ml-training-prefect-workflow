from prefect.deployments import run_deployment


def main():
    response = run_deployment(name="MNIST Traning Flow/mnist-train")
    print(response)


if __name__ == "__main__":
   main()