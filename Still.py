import cv2
import numpy as np
import matplotlib.pyplot as plt
from skimage import measure    #ssim is already defined

#for use with the analysis of the still reactor video

def mse(original, frame):
    numerator_mse = original.astype('float') - frame.astype('float') #Calculates the mean squared error between reactor images
    numerator_mse = np.sum((numerator_mse ** 2))
    denom_mse = float(original.shape[0]*original.shape[1]) 
    return (numerator_mse/denom_mse)

vid = cv2.VideoCapture(input("File name?"))

if vid.isOpened()== False: 
  print("Error opening video file")
  exit() 

stream, frame = vid.read()
SSIM_vector = []
MSE_vector = [] #for statistics
first_crop = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)[340:560, 445:645]   #crop, turn grey

while(vid.isOpened()): #loop through frames
  if stream == True:  
    crop = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)[340:560, 445:645]    
    MSE_vector.append(mse(first_crop,crop)) #the higher the value, the lower the similarity
    SSIM_vector.append(1-(measure.compare_ssim(first_crop,crop))) #ssim ranges from [-1,1], we want the least similar value to be the max
    stream, frame = vid.read()
    if cv2.waitKey(25) & 0xFF == ord('q'): #press q to exit
      break  
  else:
    break;

max_SSIM = max(SSIM_vector)
max_MSE = max(MSE_vector)
normalized_SSIM = []
normalized_MSE = []
length = len(MSE_vector)

for i in range(0,length):
    normalized_SSIM[i] = (SSIM_vector[i]/max_SSIM)
    normalized_MSE[i] = (MSE_vector[i]/max_MSE)

x = np.linspace(0,length,length)
plt.scatter(x, normalized_MSE, c='r',label = "MSE")
plt.scatter(x,normalized_SSIM, c = 'k', label = "SSIM")
plt.xlabel("Frame number")
plt.ylabel("Relative percentages")
plt.title("Visualized image comparison metrics")
plt.legend(loc = 'upper left')
plt.show()
 
