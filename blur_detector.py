import matplotlib.pyplot as plt
import numpy as np

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

    # finding the magnitude and then the mean of the re-inverted image
    magnitude = 20 * np.log(np.abs(recon))
    mean = np.mean(magnitude)

    # returning the mean calculated
    return mean