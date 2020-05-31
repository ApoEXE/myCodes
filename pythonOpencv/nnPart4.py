import torch
import torchvision
from torchvision import transforms, datasets
import matplotlib.pyplot as plt
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import cv2
import numpy as np



class Net(nn.Module):
    def __init__(self):
        super().__init__()
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
net = Net()
   


def train():
    global trainset, testset, net
    loss_function = nn.CrossEntropyLoss()
    optimizer = optim.Adam(net.parameters(), lr=0.001)

    for epoch in range(3): # 3 full passes over the data
        for data in trainset:  # `data` is a batch of data
            X, y = data  # X is the batch of features, y is the batch of targets.
            net.zero_grad()  # sets gradients to 0 before loss calc. You will do this likely every step.
            output = net(X.view(-1,28*28))  # pass in the reshaped batch (recall they are 28x28 atm)
            loss = F.nll_loss(output, y)  # calc and grab the loss value
            loss.backward()  # apply this loss backwards thru the network's parameters
            optimizer.step()  # attempt to optimize weights to account for loss/gradients
        print(loss)  # print loss. We hope loss (a measure of wrong-ness) declines! 

def calculateA():
    global trainset, testset, net
    correct = 0
    total = 0
    with torch.no_grad():
        for data in testset:
            X, y = data
            output = net(X.view(-1,784))
            #print(output)
            for idx, i in enumerate(output):
                #print(torch.argmax(i), y[idx])
                if torch.argmax(i) == y[idx]:
                    correct += 1
                total += 1
    print("Accuracy: ", round(correct/total, 3)*100)

def guessNumberDataset():

    global trainset, testset, net
    for data in testset:
        X, y = data
    image = X[0].view(-1,784)
    print("image tag:",y[0])
    output = net(image)
    output = output[0]
    print("output:",output)

    print(torch.argmax(output))




def guessNumberCV():
    global trainset, testset, net
    circle = np.zeros((28, 28), np.uint8)
    cv2.circle(circle, (14,14), 6, 255, thickness=1, lineType=8, shift=0)
    img=Normalize(circle)
    image = img.reshape(1,28*28)#converto to 1D array numpy
    print("circle image tag:",0)
    newImage= torch.from_numpy(image).float()#converto to tensor data type
    output = net(newImage)
    output = output[0]
    print("output:",output)
    print(torch.argmax(output))

def Normalize(numpyImage):
    H = numpyImage.shape[0]
    W = numpyImage.shape[1]

    print("H:",H,"W:",W)
    imgFloat = np.empty((H,W))
    for y in range(H):
        for x in range(W):
            
            imgFloat[y][x]=((numpyImage[y][x]/255.))
            print(imgFloat[y][x], end=" ")
        print("")
    return imgFloat

def part2():
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


if __name__ == '__main__':
    train()
    calculateA()
    guessNumberDataset()
    guessNumberCV()