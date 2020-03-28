import cv2
import matplotlib.pyplot as plt
image = cv2.imread("img/1.jpg")
# convert to RGB
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
# convert to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
# create a binary thresholded image
_, binary = cv2.threshold(gray, 155, 255, cv2.THRESH_BINARY_INV)
# show it
#plt.imshow(binary, cmap="gray")
#plt.show()

# find the contours from the thresholded image
img, contours, _ = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
#plt.imshow(img)
#plt.show()
_, binary2 = cv2.threshold(img, 155, 255, cv2.THRESH_BINARY_INV)
#plt.imshow(binary2, cmap="gray")
#plt.show()
# draw all contours
image = cv2.drawContours(image, contours, -1, (0, 255, 0), 1)
first = image[0][0][1]
print(first)
print(image.shape)
#color =[0,255,0]
#cv2.fillPoly(image, contours, color)
plt.imshow(image)
plt.show()

# show the image with the drawn contours
added_image = cv2.addWeighted(gray,0.4,binary2,0.1,0)
#plt.imshow(added_image)
#plt.show()
height = gray.shape[0]
width = gray.shape[1]
print(gray.shape)
for x in range(1,width):
    for y in range(1,height):
        if(image[y][x][1]!=255):
            value =gray[y][x]-50
            if value < 0:
                gray[y][x]= 0
            else:
                gray[y][x]=value
        elif image[y][x][1]==255:
            break
        
            #print(added_image[y][x], end=" ")
    #print("")
print(added_image.dtype)
plt.imshow(gray, cmap="gray")
plt.show()
