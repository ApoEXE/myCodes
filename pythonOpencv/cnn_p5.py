import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
#DESACTIVAR ESTO DESPUES DE CREAR EL DATASET, SOLO HACER UNA VEZ
REBUILD_DATA = False

class DogsVSCats():
    IMAGE_SIZE = 50
    CATS = "../../PetImages/Cat"
    DOGS = "../../PetImages/Dog"
    LABELS = {CATS: 0, DOGS: 0}
    
    training_data = []
    catcount = 0
    dogcount = 0
    
    def make_training_data(self):
        for label in self.LABELS:
            print("label",label)
            try:
                for f in tqdm(os.listdir(label)):
                    path = os.path.join(label,f)

                    img = cv2.imread(path,cv2.IMREAD_GRAYSCALE)

                    if img is not None :
                        img = cv2.resize(img,(self.IMAGE_SIZE,self.IMAGE_SIZE))
                        self.training_data.append([np.array(img),np.eye(2)[self.LABELS[label]]])

                        if label == self.CATS:
                            self.catcount += 1
                        elif label == self.DOGS:
                            self.dogcount += 1
            except Exception as e:
                
                print("Error:",e)
                pass
        np.random.shuffle(self.training_data)
        #GUARDAR DATASET
        np.save("training_data.npy", self.training_data)
        print("Cats:",self.catcount,"Dogs:",self.dogcount)



if REBUILD_DATA == True:
    dogsvcats = DogsVSCats()
    dogsvcats.make_training_data()

training_data = np.load("training_data.npy", allow_pickle=True)
print(len(training_data))
print(training_data[0])
plt.imshow(training_data[0][0], cmap="gray")
plt.show()