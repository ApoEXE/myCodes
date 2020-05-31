import torch
import torchvision
from torchvision import transforms, datasets
import matplotlib.pyplot as plt
import torch.nn as nn
import torch.nn.functional as F

train = datasets.MNIST('', train=True, download=True,
                       transform=transforms.Compose([
                           transforms.ToTensor()
                       ]))

test = datasets.MNIST('', train=False, download=True,
                       transform=transforms.Compose([
                           transforms.ToTensor()
                       ]))
trainset = torch.utils.data.DataLoader(train, batch_size=10, shuffle=True)
testset = torch.utils.data.DataLoader(test, batch_size=10, shuffle=False)

class Net(nn.Module):
    def __init__(self):
        super().__init__()
        #INPUT HxW, how many Neurals to create
        self.fc1 = nn.Linear(28*28, 64)
        self.fc2 = nn.Linear(64, 64)
        self.fc3 = nn.Linear(64, 64)
        self.fc4 = nn.Linear(64, 10)

    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = F.relu(self.fc3(x))
        x = self.fc4(x)
        return F.log_softmax(x, dim=1)

net = Net()
for i in trainset:
    data = i
    X, Y = data[0][0], data[1][0]
    print(Y)
    image = X.view(28,28)
    output =net.forward(X.view(1,28*28))
    print(output[0])
    entry = 0
    inc = 0
    number = 0
    for value in output[0]:
        if(value < entry):
            entry = value
            number = inc
        inc+=1
    print("biggest: ",entry, "number:", number)
    #plt.imshow(image)
    #plt.show()
    
