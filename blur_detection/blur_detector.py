import matplotlib.pyplot as plt
import numpy as np
import cv2


#function to calculate the value of the blur of an image
def detect_blur_fit(image, size=40):
    #getting the size of the image
    (height, width) = image.shape
    #finding the center of the image
    (X_center, Y_center) = (int(width/2.0), int(height/2.0))

    ## implementing fft on image
    # performing 2D FFT on the gray image 

    fft = np.fft.fft2(image)
    # shifting the zero-frequenY_center component to the center of the spectrum 
    fftShift = np.fft.fftshift(fft)

    # setting all the values of the zero-frequecny component to 0
    fftShift[Y_center - size:Y_center + size, X_center - size:X_center + size] = 0
    # inverting the previously performed shift
    fftShift = np.fft.ifftshift(fftShift)
    # inverting the un-shifted image
    recon = np.fft.ifft2(fftShift)


    ### code to plot the images - although doing so might not make much sense XD
    ###  uncomment the code to plot images while running this single program

    # plt.imsave("original_image2.png", image, cmap = "gray")
    # plt.imsave("inverse_FFT_image2.png",np.log(abs(recon)), cmap='gray')


    # finding the magnitude and then the mean of the re-inverted image
    magnitude = 20 * np.log(np.abs(recon))
    mean = np.mean(magnitude)

    # returning the mean calculated

    return mean


if __name__ == "__main__":
    #
    read_image = cv2.imread("images/G0018106.JPG")
    read_image_gray = cv2.cvtColor(read_image, cv2.COLOR_BGR2GRAY)
    detect_blur_fit(read_image_gray)

