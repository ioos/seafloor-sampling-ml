import os
import argparse
import cv2
import numpy as np
import matplotlib.pyplot as plt
from skimage.morphology import skeletonize
from statistics import median
import pandas as pd


#defining the kernel to perform various operations like opening, closing etc
kernel = np.array([[0, 0, 1, 0, 0],
                    [1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1],
                    [0, 0, 1, 0, 0]], dtype=np.uint8)


#adding parguemnt parser
ap = argparse.ArgumentParser()


ap.add_argument("-f", "--folder", type=str, required=True, 
                help="path input image that we'll detect blur in")
    
ap.add_argument("-c", "--csv", type=str, default="laser_distance",
	            help="naming the csv file")

args = vars(ap.parse_args())

folders = os.listdir(args["folder"])
print(folders)

#array to store the folder name (which is one particular transect)
transect_name = []
#array to store the image name
image_name = []
#array to store the value of the laser
laser_distance = []
#arrat to store the values of the area calculated
area_array = []


#function to extract lasers 
def laser_detection(image):
    #cropping the image to only focus on laser area
    image =  image[:, 2000:3000]
    #converting image from BGR to RGB
    image =  cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    #converting the image to HSV format
    hsv = cv2.cvtColor(image,cv2.COLOR_BGR2HSV) 

    #defining the range of red to extract the lasers
    cell_hsvmin  = (100,80,150)  
    cell_hsvmax  = (150,255,255)

    #showing the HSV image for visualization
    hsv = cv2.cvtColor(image,cv2.COLOR_BGR2HSV) 

    #extracting lasers values from images
    color_thresh = cv2.inRange(hsv, cell_hsvmin, cell_hsvmax)

    return color_thresh

#function for inverting the image and extracting the lasers
def inverse_laser_detection(image): 
    #inverting the image to extract the points
    img_not = cv2.bitwise_not(image)

    #converting the inverted image to HSV
    hsv = cv2.cvtColor(img_not,cv2.COLOR_BGR2HSV) 
    
    #saving the inverted image 
    cv2.imwrite("inverted-image.png", hsv)

    #reading the inverted image
    image_inverted = cv2.imread("inverted-image.png")

    #defining the colours for the red-spots/lasers from the inverted image
    cell_hsvmin  = (50,230,240)  
    cell_hsvmax  = (70,250,255)

    #extracting lasers values from images
    hsv = cv2.cvtColor(image_inverted,cv2.COLOR_BGR2HSV) 

    color_thresh = cv2.inRange(hsv, cell_hsvmin, cell_hsvmax)

    return color_thresh

#function to find the area of the lasers
def area_lasers(color_thresh):
    contours, hierarchy = cv2.findContours(color_thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    #finding the total area of the lasers to make sure only the lasers are recognised
    area_lasers = 0

    #going through all the contours that are there and finding the area of each and summing them.
    for i in range(len(contours)):
        area_lasers += cv2.contourArea(contours[i])
    
    return area_lasers

#function to find the distance between the lasers
def measures_laser_distance(color_thresh):
    #performing closing 5 times and opening 2 times to enhance the image and remove noise
    image_closing = cv2.morphologyEx(color_thresh, cv2.MORPH_CLOSE, kernel, iterations =5)
    image_opening = cv2.morphologyEx(image_closing, cv2.MORPH_OPEN, kernel, iterations =2)
    #converting all values from 0,255 to binary ie. 0/1
    image_opening = image_opening/255
    #skeletonizing the image to only get the points in which the lasers are detected. 
    image_skeleton = skeletonize(image_opening)
    #staking the points 
    points = np.column_stack(np.where(image_skeleton == True))

    #defining an array to store the parallel points to find the best distance
    y_coordinates_parallel = []

    ### going through the points in the array 
    for i in range (0,len(points)-1):
      for j in range(i, len(points)-1):
        if points[i][0] == points[j][0]:
          if points[j][1] - points[i][1] > 40 and points[j][1] - points[i][1] < 200:
            # print(points[i], points[j])
            y_coordinates_parallel.append(points[j][1]-points[i][1])


    if len(y_coordinates_parallel) == 0:
      for i in range (0,len(points)-1):
        for j in range(i, len(points)-1):
          if points[i][0]+1 == points[j][0]:
            if points[j][1] - points[i][1] > 40 and points[j][1] - points[i][1] < 200:
            #   print(points[i], points[j])
              y_coordinates_parallel.append(points[j][1]-points[i][1])

    if len(y_coordinates_parallel) != 0:
        return median(y_coordinates_parallel)
    else:
        return 0

#function to calcuate the area of the contoured area
def area_calc(contours):
    area_pixels = 0
    for i in range(len(contours)):
        area_pixels += cv2.contourArea(contours[i])
    
    #need to convert area from pixels^2 to cm^2
    return area_pixels 


#function to find the area of the image
def area_calucation(image):
    #converting image from BGR to RGB
    image =  cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    #converting the image to HSV format
    hsv = cv2.cvtColor(image,cv2.COLOR_BGR2HSV) 
    cell_hsvmin  = (0,0,80)  
    cell_hsvmax  = (255,255,255)

    color_thresh2 = cv2.inRange(hsv, cell_hsvmin, cell_hsvmax)
    opening = cv2.morphologyEx(color_thresh2, cv2.MORPH_OPEN, kernel, iterations =100) #0759

    #finding the contours in the images
    contours, hierarchy = cv2.findContours(opening, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    #calculating the area of the image
    area = area_calc(contours)
    return area

if __name__ ==  "__main__":
    for folder in folders:
        images = os.path.join(args["folder"],folder)

        for frame in os.listdir(images):
            #reading all the images present in the given folder
            file_location = os.path.join(images, frame)

            #reading image from drive
            image =  cv2.imread(file_location)
            area = area_calucation(image)
            #appending the area
            area_array.append(area)
            #check for laser in normal form
            laser_detected_image = laser_detection(image)
            #finding the area of the detected lasers
            laser_area = area_lasers(laser_detected_image)

            # if lasers are not detected or HSV segmentation considers parts of image to be same 
            # color of lasers, then invert the image and try to extract lasers
            if laser_area >= 5000 or laser_area == 0:  
                #checking lasers on the inverted image and performing laser detection
                laser_detected_image = inverse_laser_detection(image)
                #finding the area of the detected lasers
                laser_area = area_lasers(laser_detected_image)

            ### if the area of the laser is greater than 5000 or 0 then they aren't lasers or the lasers are not being detected
            if laser_area >= 5000 or laser_area == 0: 
                #we add in the details and fill the values as 0 for the laser 
                transect_name.append(folder)
                image_name.append(frame.split(".")[0])
                laser_distance.append(0)

            else:
                transect_name.append(folder)
                image_name.append(frame.split(".")[0])
                laser_distance.append(measures_laser_distance(laser_detected_image))
            
            break

    df = pd.DataFrame(list(zip(transect_name, image_name, laser_distance, area_array)), columns= ["folder_name","image_name", "blur_level", "area"])
    df = df.sort_values(by = ["image_name"])
    df.to_csv(args["csv"]+".csv", index=False)

    os.remove("inverted-image.png")