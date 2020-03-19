# Canny-Edge-Detector
* First derivative of a Gaussian.
* Produces segments of thin image contours.
* Approximation to an operator that optimizes the product of signal-to-noise ratio and localization

## Steps
Canny Edge Detector consists of four steps:

1. Gaussian smoothing: Smooth image with a Gaussian filter.
2. Gradient operation: Compute gradient magnitude and gradient angle at each pixel location of the smoothed location using SObel's operator.
3. Non-maxima suppression: Apply non-maxima suppression to gradient magnitude.
4. Thresholding: Simple thresholding or Double thresholding.

## Additional Considerations
* The input to your program is a grayscale image of size N X M.
* Use the 7 x 7 Gaussian mask as shown below for smoothing the input image. 
* Use the center of the mask as the reference center. If part of the Gaussian mask goes outside of the image border, let the output image be undefined at the location of the reference center. 

    Note: The entries in the Gaussian mask do not sum to 1. 

* After performing convolution (or cross-correlation), you need to perform normalization by dividing the results by the sum of the entries (= 140 for the given mask) at each pixel location. 

* If part of the 3 x 3 mask of the operator goes outside of the image border or lies in the undefined region of the image after Gaussian filtering, let the output value be undefined. For the third step, follow the procedure in the lecture slides for non-maxima suppression. 

* At locations with undefined gradient values and at locations where the center pixel has a neighbor with undefined gradient value, let the output be zero (i.e., no edge.) 

* For the fourth step, use double thresholding to threshold the gradient magnitude 𝑁𝑁(𝑖𝑖,𝑗𝑗) after non-maxima suppression into a
binary edge map 𝐸𝐸(𝑖𝑖,𝑗𝑗). Set up a low threshold 𝑇𝑇1 and a high threshold 𝑇𝑇2 so that 𝑇𝑇2 = 2𝑇𝑇1.
