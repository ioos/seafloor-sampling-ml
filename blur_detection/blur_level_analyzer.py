import blur_detector
import numpy as np
import argparse
import imutils
import cv2 
import os
import pandas as pd
import config



# adding parser 
ap = argparse.ArgumentParser()

# argparse values
ap.add_argument("-f", "--folder", type=str, required=True,
	help="path input image that we'll detect blur in")
ap.add_argument("-c", "--csv", type=str, default="blur_detection",
	help="naming the csv file")
args = vars(ap.parse_args())

#listing all the images that are present in the folder
folders = os.listdir(args["folder"])
print(folders)

# defining arrays to store the values of the image, folder names and blur values
# to be later used to save into dataframe 
blur_level = []
image_name = []
folder_name = []

# iterating through all the folders
for folder in folders:
    images = os.path.join(args["folder"],folder)

    for frame in os.listdir(images):
        #getting the image loc. by joining the path
        file_location = os.path.join(images, frame)
        #reading the image
        orig = cv2.imread(file_location)
        #cropping the image to have only 60% of the image to detect blur
        # (edge removal due to extra blurry nature)
        x1 = config.X1_COORDINATE_IMAGE_CROPPED
        x2 = config.X2_COORDINATE_IMAGE_CROPPED
        y1 = config.Y1_COORDINATE_IMAGE_CROPPED
        y2 = config.Y2_COORDINATE_IMAGE_CROPPED
        orig = orig[y1:y2, x1:x2]
        #resizing image 
        orig = imutils.resize(orig, width=1500)
        #converting the image to gray
        gray = cv2.cvtColor(orig, cv2.COLOR_BGR2GRAY)

        #finding the mean and the blur value (boolean) after passing the gray image to the blur detector
        (mean, blurry) = blur_detector.detect_blur_fit(gray, size = 40)
        #appending values to the arrays definied earlier
        blur_level.append(mean)
        image_name.append(frame.split(".")[0])
        folder_name.append(folder)
        
# creating a dataframe to store all the values
df = pd.DataFrame(list(zip(folder_name, image_name, blur_level)), columns= ["folder_name","image_name", "blur_level"])
#sorting the dataframe by the image name
df = df.sort_values(by = ["image_name"])
#saving the dataframe to a CSV file
df.to_csv(args["csv"]+".csv", index=False)
