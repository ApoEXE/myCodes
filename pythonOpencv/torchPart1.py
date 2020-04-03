import torch
import torchvision
from torchvision import transforms, datasets
import matplotlib.pyplot as plt


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

for i in trainset:
    data = i
    break
X, Y = data[0][0], data[1][0]
print(Y)
print(X.shape[2])
image = X.view(28,28)
print(X.view(28,28))
print(type(image))
plt.imshow(image)
plt.show()