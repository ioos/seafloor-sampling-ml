# Sea Floor Sampling
This repo consists of work on Sea Floor Sampling using machine learning and computer vision techniques, in which there are two main objectives:

1. Identifying species present on the sea floor.
2. Measure the area of the frame being analysed using the distance between the lasers.
3. Identifying the Sea Floor Habitat through videos. 
4. Measure the number of sea floor creatures in a video feed.

# Running this application:

## Clone the repository/download it.

There are a couple ways you can do this.

1. Click on Green Code button on the right side of the repository and donwload the zip file.
2. If you have a G1itHub account and git installed on your machine, fork the repository and clone ir.
3. Use using the follwoing code on the terminal to clone the repository.
    ```git clone `https://github.com/ioos/seafloor-sampling-ml.git``


#### You need to install an ```anaconda``` environment to run the code. 

## If you have anaconda already on your system. Go to step 2.

1. Follow [this link](https://docs.conda.io/projects/conda/en/latest/user-guide/install/windows.html) and follow all the steps to install anaconda on your system.
2. After installing anaconda, create a ```new environment``` on your system. To create a new environement, check the steps below 
    - Open the terminal and type ```conda create --name <name of the envorinment you want to create> python=<python version you want to install>```
    - For example, ```conda create --name SeaFloorSampling python=3.8```
    - Once you have created the environment, jump into the environment using ```conda activate <name of the environment you created```
    - For example, ```conda activate SeaFloorSampling```
    - You are now inside the environment you created.


## Installing requirements

After we have installed anaconda, and inside the environment we created, we need to setup libraries to use/run the code. 

1. Open the the folder where the file is downloaded and unzip the code.
2. After unzipping the code, go inside the folder where all the code exists, with this ```README.md``` file. 
2. If you are using a windows device, at the path of the folder on the top and type ```cmd```. This will open the terminal.
3. If you are not inside the environment you created already, type ```conda activate <name of the environment you created```. For example, ```conda activate SeaFloorSampling```.
4. Inside the terminal type ```pip install -r requirements.txt``` to install all the necessary libraries to run the code further on.

### TO RUN THE PROGRAM ON THE IMAGES, MAKE SURE THERE IS A FOLDER WITH ALL THE IMAGES FROM VARIOUS TRANSECTS IN FOLDERS IN THEIR RESPECTIVE APPLICATION FOLDER. FOR EXAMPLE, IF YOU WANT TO RUN THE BLUR DETECTOR CODE, PLACE THE IMAGE FOLDER INSIDE THE BLUR DETECTOR CODE FOLDER.   

## Blur Detection Program

This program measures how blurred a given image is. It uses Fourier Transform to measure the level of blur. If the image is too blurred, we can't perform any kind of analysis on it.

1.  Once you have unzipped the folder and you are inside the ```blur_detection``` folder and have the images in place, run the following code. 
    - ```python3 blur_level_analyzer.py -f <folder destination which contain other folders (eg. /images)> -c "<name of the final csv file you want to have>" ```. For example, ```python3 blur_level_analyzer.py -f images -c SeaFloorSampling```
2.  After some time, this will create a csv file with the name SeaFloorSampling.csv (the name of the file you input).

## Area Computation

This program measures what the area of the image being analyses is. This will be crucial when the report is made finally.

1.  Once you have unzipped the folder and you are inside the ```laser_area_computation``` folder and have the images in place, run the following code. 
    - ```python3 laser_detection_area_computation.py -f <folder destination which contain other folders (eg. /images)> -c "<name of the final csv file you want to have>" ```. For example, ```python3 blur_level_analyzer.py -f images -c AreaComputation_SeaFloorSampling```
2.  After some time, this will create a csv file with the name AreaComputation_SeaFloorSampling.csv (the name of the file you input).

## Habitat Classification

This program analyses the images and picks out images with 100% sand or mud images.

Coming soon...


MIT © [IOOS]()

