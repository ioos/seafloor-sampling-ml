import os

#the path to where our data will be saved 
DATASET_PATH = "input"
DATASET_PATH_COLAB = "/content/drive/My Drive/Group_Classification/input"

#inititializing the class labels 
CLASSES = ["MUD"]

#defining size of train, test, validation sets
TRAIN_SPLIT = 0.85
TEST_SPLIT = 0.15
VAL_SPLIT = 0.1

#defining the min lr, max lr,   batch size, step size, CLR method and the no of epochs
MIN_LR = 1e-6
MAX_LR = 1e-4
BATHC_SIZE = 32
STEP_SIZE = 8
CLR_METHOD = "triangular"
NUM_EPOCHS = 40

#initializing the output model path
MODEL_PATH = os.path.sep.join(["output", "group classification model"])
MODEL_PATH_COLAB = "/content/drive/My Drive/Group_Classification/model"

#define the path to the output paths for images 
LRFIND_PLOT_PATH = "/content/drive/My Drive/Group_Classification/output/LRFIND_PLOT.png"
TRAINING_PLOT_PATH = "/content/drive/My Drive/Group_Classification/output/TRAINING_PLOT.png"
CLR_PLOT_PATH = "/content/drive/My Drive/Group_Classification/output/CLR_PLOT.png"


