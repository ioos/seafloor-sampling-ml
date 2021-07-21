import matplotlib.pyplot as plt
import numpy as np

def detect_blur_fit(image, size=60, thresh= 10, vis=False):
    (h, w) = image.shape
    (cX, cY) = (int(w/2.0), int(h/2.0))

    #implementing fft on image
    fft = np.fft.fft2(image)
    fftShift = np.fft.fftshift(fft)

    if vis:
        magnitude = 20 * np.log(np.abs(fftShift))

        (fig, ax) = plt.subplot(1, 2, )
        ax[0].imshow(image, cmap="gray")
        ax[0].set_title("Input")
        ax[0].set_xticks([])
        ax[0].set_yticks([])
		# display the magnitude image
        ax[1].imshow(magnitude, cmap="gray")
        ax[1].set_title("Magnitude Spectrum")
        ax[1].set_xticks([])
        ax[1].set_yticks([])
        
        plt.show()

    fftShift[cY - size:cY + size, cX - size:cX + size] = 0
    fftShift = np.fft.ifftshift(fftShift)
    recon = np.fft.ifft2(fftShift)

    magnitude = 20 * np.log(np.abs(recon))
    mean = np.mean(magnitude)

    return (mean, mean <= thresh)