from prefect import flow, task
from prefect.task_runners import SequentialTaskRunner
import torch, torchvision
from torchvision import transforms
#from prefect.filesystems import Azure

# Model architecture
class Net(torch.nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.conv1 = torch.nn.Conv2d(1, 10, kernel_size=5)
        self.conv2 = torch.nn.Conv2d(10, 20, kernel_size=5)
        self.fc1 = torch.nn.Linear(320, 50)
        self.fc2 = torch.nn.Linear(50, 10)
        
    def forward(self, x):
        x = torch.nn.functional.relu(torch.nn.functional.max_pool2d(self.conv1(x), 2))
        x = torch.nn.functional.relu(torch.nn.functional.max_pool2d(self.conv2(x), 2))
        x = x.view(-1, 320)
        x = torch.nn.functional.relu(self.fc1(x))
        x = self.fc2(x)
        return torch.nn.functional.log_softmax(x, dim=1)


@task(name="MNIST Traning Task")
def task_train_mnist():
    # Load MNIST dataset
    #block = Azure(bucket_path="az://prefectblock/")
    transform = transforms.Compose([transforms.ToTensor(), transforms.Normalize((0.5,), (0.5,))])
    trainset = torchvision.datasets.MNIST(root='./data', train=True, download=True, transform=transform)
    trainloader = torch.utils.data.DataLoader(trainset, batch_size=64, shuffle=True)

    model = Net()

    # Define the optimizer and loss function
    optimizer = torch.optim.SGD(model.parameters(), lr=0.01, momentum=0.5)
    criterion = torch.nn.CrossEntropyLoss()

    # Train the model
    for epoch in range(10):
        running_loss = 0.0
        for i, data in enumerate(trainloader, 0):
            inputs, labels = data
            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            running_loss += loss.item()
        avg_loss = running_loss / len(trainloader)
        #run.log('Training Loss', avg_loss)
        print('Epoch: %d, Loss: %.3f' % (epoch + 1, avg_loss))

@flow(name="MNIST Traning Flow"
      #,description="MNIST Flow using SequentialTaskRunner"
      #,task_runner=SequentialTaskRunner()
      ,log_prints=True)
def train_mnist():
    print("Beginning Traning for MNIST!")
    task_train_mnist()


if __name__ == "__main__":
    train_mnist()