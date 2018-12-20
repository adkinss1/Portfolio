import numpy as np
from skimage import color
import matplotlib.pyplot as plt
from scipy import misc

class Image_Analysis():

    def __init__(self,image):
        self.image = color.rgb2gray(image)
        self.FT = np.fft.fft2(self.image)

    def plot_fourier(self):
        f, (ax2, ax3) = plt.subplots(1, 2, figsize=(20,10))
        gray = color.rgb2gray(self.image);
        ax2.imshow(gray, cmap='gray')
        ax2.axis('equal')
        ax2.axis('off')
        ax2.set_title('gray image')
        Fs = self.FT
        F2 = np.fft.fftshift(Fs)
        psd2D = np.abs(F2)#**2
        ax3.imshow( np.log10(psd2D))
        ax3.axis('equal')
        ax3.axis('off')
        ax3.set_title('frequency space')


    def plot_function(self):
        gray = color.rgb2gray(self.image);
        plt.imshow(gray, cmap='gray')
        plt.show()

    def mask(self):
        f, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(20,10))
        image = self.image
        rows = image.shape[0]
        cols = image.shape[1]

        #Generate a simple square mask
        mask = np.ones([rows,cols])

        mask[round(rows/2),:] = 0
        mask[:,round(cols/2)] = 0

        #Plot the mask
        ax1.imshow(mask)
        ax1.axis('equal')
        ax1.axis('off')

        #Calculate the Grayscale image
        gray = self.image

        # Take 2D FFT
        Fs = np.fft.fft2(gray)

        # Shift the 2D FFT into the "Standard" view
        F2 = np.fft.fftshift( Fs )

        #Apply the mask
        F3 = F2*mask

        # Generate easy-to-see plot
        psd2D = np.abs( F3 )#**2
        ax2.imshow( np.log10(psd2D))
        ax2.axis('equal')
        ax2.axis('off')

        # Shift the masked image back
        F4 = np.fft.fftshift( F3 )

        # Apply the inverse fft and show the final result.
        im2 = abs(np.fft.ifft2(F4))
        ax3.imshow(im2, cmap='gray')
        ax3.axis('equal')
        ax3.axis('off')
