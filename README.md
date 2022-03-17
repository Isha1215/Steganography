# Steganography
Hiding an image inside another image using LSB algorithm

In this project I have implemented Steganography by hiding a image inside another

The image to be hidden should be small enough as compared to the image in which it is to be hidden

--Language used:
Python

--Libraries used:
PIL,Opencv

--image to hide- secret image

--image to hide in- cover image

--LSB Algorithm

-> Every image is made up of pixel

-> Every pixel has three componenets r,g,b (here we are talking about color images)

-> Every component is of 8 bits (total 24 bits for a pixel)

-> The msb contributes the maximum to the color pixel and the lsb the least.

-> Hence in this lsb Algorithm we are going to hide secret image in cover by replacing the lsb of the cover image with the bits of the secret image.

-> The encoded image won't change as the lsb has been changed which contributes the least to the color.

--Encode
-> We will specify a variable n_bits denoting how many lsb's should be replaced in the cover image

-> We will check a condition that if Total pixels of the secret_image * (8/n_bits) < Total pixels of cover_image

-> If the above is true only then hiding is possible else the secret image isn't small enough.

-> Then according to the value of n_bits we will replace that many lsb bits  of the cover image with the bits of secret image

-> We will continue till all the bits of secret image are stored in cover image

--Decode

-> We just have to retreive the secret image by getting the lsb values of pixels from the cover image.

-> Depending on the value of n_bits used 8/n_bits tells us that for hiding one pixel in secret image how many pixels were are required from the cover image.

-> According we have to generate one pixel from 8/n_bits pixels of cover image


--Histogram

-> We will display histograms of the images to show difference between cover image and encoded image

-> To also show that the histogram of secret image and decoded image is exactly same
