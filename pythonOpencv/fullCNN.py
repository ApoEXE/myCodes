import os
import cv2
import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt
#NEURAL LAYERS CREATION
import torch
import torch.nn as nn
import torch.nn.functional as F
#TRAINING IMPORT
import torch.optim as optim
REBUILD_DATA = False

#CREATING DATASET FROM RAW IMAGES
class DogsVSCats():
    IMG_SIZE = 50
    CATS = "../../PetImages/Cat"
    DOGS = "../../PetImages/Dog"
    LABELS = {CATS: 0, DOGS: 1}
    
    training_data = []
    catcount = 0
    dogcount = 0
    
    def make_training_data(self):
        for label in self.LABELS:
            #print(label)
            for f in tqdm(os.listdir(label)):
                if "jpg" in f:
                    try:
                        path = os.path.join(label, f)
                        img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
                        img = cv2.resize(img, (self.IMG_SIZE, self.IMG_SIZE))
                        self.training_data.append([np.array(img), np.eye(2)[self.LABELS[label]]])  # do something like print(np.eye(2)[1]), just makes one_hot 
                        #print(np.eye(2)[self.LABELS[label]])

                        if label == self.CATS:
                            self.catcount += 1
                        elif label == self.DOGS:
                            self.dogcount += 1

                    except Exception as e:
                        print(label, f, str(e))

        np.random.shuffle(self.training_data)
        np.save("training_data.npy", self.training_data)
        print('Cats:',dogsvcats.catcount)
        print('Dogs:',dogsvcats.dogcount)


#CREATING NEURAL NETWORK
class Net(nn.Module):
        
    def convs(self, x):
        #F.relu is activation function
        # max pooling over 2x2
        x = F.max_pool2d(F.relu(self.conv1(x)), (2, 2))
        x = F.max_pool2d(F.relu(self.conv2(x)), (2, 2))
        x = F.max_pool2d(F.relu(self.conv3(x)), (2, 2))
        #flatthen to get into a linear fully connected  neural
        x = torch.flatten(x, 1, -1)
        if self._to_linear is None:#this was created to obtain the output of last conv
            self._to_linear =x.shape[1]
            print("output of conv:",self._to_linear)
        return x
    
    def forward(self, x):
        x = self.convs(x)#convolutions maxpull pass
        x = F.relu(self.fc1(x))#pass the convolution through fully connected linear
        x = self.fc2(x) # bc this is our output layer. No activation here.
        return F.softmax(x, dim=1)

    def __init__(self):
        super().__init__()
        #Number of Channel 1,32,64, OUPUT FEATURE 32, 64, 128, KERNEL SIZE 5x5 
        #LAYER 1 CONVOLUTIONAL THIS ARE 2D CONVOLUTIONAL LAYERS
        self.conv1 = nn.Conv2d(1,32,5)
        #LAYER 2 CONVOLUTIONAL THIS ARE 2D CONVOLUTIONAL LAYERS
        self.conv2 = nn.Conv2d(32,64,5)
        #LAYER 3 CONVOLUTIONAL THIS ARE 2D CONVOLUTIONAL LAYERS
        self.conv3 = nn.Conv2d(64,128,5)
        
        #dummy image to get output of conv so fc neurans has a starting input
        x = torch.randn(50,50).view(-1,1,50,50)
        self._to_linear = None
        #output of this is the self.to_linear output of conv
        self.convs(x)
        
        #INPUT HxW, how many Neurals to create (its call Dense Layer)
        #LAYER LINEAR 1
        self.fc1 = nn.Linear(self._to_linear, 512) #flattening.
        #LAYER LINEAR 2
        self.fc2 = nn.Linear(512, 2) # 512 in, 2 out bc we're doing 2 classes (dog vs cat).
        
def train(train_X,train_y):
    #TRAINNING
    BATCH_SIZE = 100
    EPOCHS = 1
    print("TRAINING MODEL WITH BATCH:",BATCH_SIZE, "AND EPOCHS:",EPOCHS)
    for epoch in range(EPOCHS):# from 0, to the len of x, stepping BATCH_SIZE at a time. [:50] ..for now just to dev
        for i in tqdm(range(0, len(train_X), BATCH_SIZE)): 
            #print(f"{i}:{i+BATCH_SIZE}")
            batch_X = train_X[i:i+BATCH_SIZE].view(-1, 1, 50, 50)
            batch_y = train_y[i:i+BATCH_SIZE]  
            net.zero_grad()
            outputs = net(batch_X)
            loss = loss_function(outputs, batch_y)
            loss.backward()
            optimizer.step()    # Does the update



    print(f"Epoch: {epoch+1}. Loss: {loss}")
    #SAVE MODEL
    torch.save(net.state_dict(), "fullcnn.pt")

def test(test_X,test_y):
    #VALIDATING DATA
    print("TESTING ACCURACY OF MODEL")
    correct = 0
    total = 0
    with torch.no_grad():
        for i in tqdm(range(len(test_X))):
            real_class = torch.argmax(test_y[i])
            net_out = net(test_X[i].view(-1, 1, 50, 50))[0]  # returns a list, 
            predicted_class = torch.argmax(net_out)

            if predicted_class == real_class:
                correct += 1
            total += 1
    print("Accuracy: ", round(correct/total, 3))

def convertData(training_data):
    X = torch.Tensor([i[0] for i in training_data]).view(-1,50,50)
    X = X/255.0
    y = torch.Tensor([i[1] for i in training_data])

    #separate train and test dataset
    VAL_PCT = 0.1  # lets reserve 10% of our data for validation
    val_size = int(len(X)*VAL_PCT)
    print(val_size)
    #slice
    train_X = X[:-val_size]
    train_y = y[:-val_size]

    test_X = X[-val_size:]
    test_y = y[-val_size:]
    print(len(train_X), len(test_X))
    return test_y,test_X,train_y,train_X

#--------------------------CODE FROM HERE ON ------------------------------#        
#STEP1: CREATE OUR DATASET ANS SAVE IT
if REBUILD_DATA == True:
    dogsvcats = DogsVSCats()
    dogsvcats.make_training_data()
training_data = np.load("training_data.npy", allow_pickle=True)
print("DATASET SIZE",len(training_data))

#STEP2: CREATE OUR NEURAL NETWORK  IN A MODULE "CLASS"      
#STEP3: LOAD OUR NEURAL NETWORK
net = Net()
print(net)
#STEP4: PREPARE NN PARAMETERS AND LOSS FOR TRAINNING
optimizer = optim.Adam(net.parameters(), lr=0.001)
loss_function = nn.MSELoss()
#STEP5: PREPARE DATASET: TRAINING TESTING
test_y,test_X,train_y,train_X = convertData(training_data)
#STEP6: TRAIN WITH TRAINNING DATASET
train(train_X,train_y)
#STEP7: TEST WITH TESTING DATASET
test(test_X,test_y)
