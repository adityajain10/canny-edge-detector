import math
import os

import numpy as np
from cv2 import imread
from cv2 import imwrite

# Canny Edge Detector consists of four steps:
# 1. Smooth image with a Gaussian filter
# 2. Compute gradient magnitude and angle
# 3. Apply non-maxima suppression to gradient magnitude
# 4. Thresholding - Here we are using double thresholding


# setting output folder
output_path = str(os.path.dirname(os.path.realpath(__file__))) + "/output"
if not os.path.exists(output_path):
    os.makedirs(output_path)


def canny(img):
    # Step 1: Gaussian smoothing & normalization
    gaussian_output = gaussian_smoothing(img)

    # Step 2: Gradient Operator
    gradient_magnitude, gradient_angle = gradient_operation(gaussian_output)

    # Step 3:Non maxima suppression
    non_maxima_suppressed = non_maxima_suppression(gradient_magnitude, gradient_angle)

    # Step 4:Double thresholding
    double_thresholding(non_maxima_suppressed, gradient_angle)


# Step 1: Gaussian smoothing & normalization
def gaussian_smoothing(input_image):
    # Loading image in form of a matrix
    image = imread(input_image, 0)

    # gaussian mask initiated
    gaussian_mask = np.array(
        [
            [ 1, 1, 2, 2, 2, 1, 1 ],
            [ 1, 2, 2, 4, 2, 2, 1 ],
            [ 2, 2, 4, 8, 4, 2, 2 ],
            [ 2, 4, 8, 16, 8, 4, 2 ],
            [ 2, 2, 4, 8, 4, 2, 2 ],
            [ 1, 2, 2, 4, 2, 2, 1 ],
            [ 1, 1, 2, 2, 2, 1, 1 ]
        ])

    image_height = image.shape[ 0 ]
    image_width = image.shape[ 1 ]

    # Initializing 2-D array to store convolution values
    convoluted_gaussian_arr = np.empty((image_height, image_width))

    for row in range(image_height):
        for col in range(image_width):

            # setting the undefined pixel value to 0
            if 0 <= row < 3 or image_height - 3 <= row <= image_height - 1 or 0 <= col < 3 or image_width - 3 <= col <= image_width - 1:
                convoluted_gaussian_arr[ row ][ col ] = 0
            else:
                x = 0

                # calculating convoluted values for each pixel position and storing it in 'convoluted_gaussian_arr'
                for k in range(7):
                    for l in range(7):
                        x = x + (image[ row - 3 + k ][ col - 3 + l ] * gaussian_mask[ k ][ l ])

                # normalizing the value
                convoluted_gaussian_arr[ row ][ col ] = x / 140

    # Writing output image from Gaussian Smoothing
    imwrite(os.path.join(output_path, "gaussian_smoothing.bmp"), convoluted_gaussian_arr)
    return convoluted_gaussian_arr


# gradient calculation function which takes in the gaussian convoluted matrix as argument
def gradient_operation(smoothed_image):
    # Sobel's operator for Gx
    sobel_gx = np.array([ [ -1, 0, 1 ], [ -2, 0, 2 ], [ -1, 0, 1 ] ])

    # Sobel's operator for Gy
    sobel_gy = np.array([ [ 1, 2, 1 ], [ 0, 0, 0 ], [ -1, -2, -1 ] ])

    image_height = smoothed_image.shape[ 0 ]
    image_width = smoothed_image.shape[ 1 ]

    # initializing 2-d array to store the horizontal and vertical gradient
    horizontal_gradient = np.zeros((image_height, image_width))
    vertical_gradient = np.zeros((image_height, image_width))

    for row in range(image_height):
        for col in range(image_width):

            # sets the undefined pixel value to 0
            if 0 <= row < 4 or image_height - 4 <= row <= image_height - 1 or 0 <= col < 4 or image_width - 4 <= col <= image_width - 1:
                horizontal_gradient[ row ][ col ] = 0

            else:
                x = 0
                for i in range(3):
                    for j in range(3):
                        # calculating horizontal gradient value
                        x = x + ((smoothed_image[ row - 1 + i ][ col - 1 + j ]) * sobel_gx[ i ][ j ])

                # normalizing the pixel values
                horizontal_gradient[ row ][ col ] = x / 3

    for row in range(image_height):
        for col in range(image_width):

            # setting the undefined pixel value to 0
            if 0 <= row < 4 or image_height - 4 <= row <= image_height - 1 or 0 <= col < 4 or image_width - 4 <= col <= image_width - 1:
                vertical_gradient[ row ][ col ] = 0

            else:
                x = 0
                # calculating vertical gradient value for each pixel
                for i in range(3):
                    for j in range(3):
                        x = x + (smoothed_image[ row - 1 + i ][ col - 1 + j ] * sobel_gy[ i ][ j ])
                # normalizing the pixel values
                vertical_gradient[ row ][ col ] = x / 3

    # initializing 2-d array to store gradient angles
    gradient_angle = np.empty((image_height, image_width))

    for row in range(image_height):
        for col in range(image_width):

            # checking if the denominator is 0
            if horizontal_gradient[ row ][ col ] == 0:
                gradient_angle[ row ][ col ] = 90

            else:
                gradient_angle[ row ][ col ] = math.degrees(
                    math.atan((vertical_gradient[ row ][ col ]) / (horizontal_gradient[ row ][ col ])))

    # calculating absolute values
    for row in range(image_height):
        for col in range(image_width):
            horizontal_gradient[ row ][ col ] = abs(horizontal_gradient[ row ][ col ])
            vertical_gradient[ row ][ col ] = abs(vertical_gradient[ row ][ col ])

    # writing the horizontal and vertical gradient
    imwrite(os.path.join(output_path, "horizontal_gradient.bmp"), horizontal_gradient)
    imwrite(os.path.join(output_path, "vertical_gradient.bmp"), vertical_gradient)

    # initializing 2-d array to store gradient magnitude with normalized values (divided by root(2))
    gradient_mag = np.empty((image_height, image_width))
    # inserts values in the gradient magnitude matrix
    for row in range(image_height):
        for col in range(image_width):
            x = math.pow(horizontal_gradient[ row ][ col ], 2)
            y = math.pow(vertical_gradient[ row ][ col ], 2)
            gradient_mag[ row ][ col ] = (math.sqrt(x + y)) / math.sqrt(2)

    # writing gradient magnitude
    imwrite(os.path.join(output_path, "gradient_image.bmp"), gradient_mag)

    return gradient_mag, gradient_angle


# 3. Apply non-maxima suppression to gradient magnitude
def non_maxima_suppression(gradient_mag, gradient_angle):
    image_height = gradient_mag.shape[ 0 ]
    image_width = gradient_mag.shape[ 1 ]

    # a zero matrix initiated to hold the values after non-maxima suppression
    suppressed_arr = np.zeros((image_height, image_width), dtype='int')

    # for loops iterating each pixel
    for i in range(image_height):
        for j in range(image_width):
            # sets the undefined pixel value to 0
            if 0 <= i < 5 or image_height - 5 <= i <= image_height - 1 or 0 <= j < 5 or image_width - 5 <= j <= image_width - 1:
                suppressed_arr[ i ][ j ] = 0
            else:
                x = gradient_angle[ i ][ j ]
                y = gradient_mag[ i ][ j ]

                # checking if gradient angle is in 0th sector
                if (-22.5 < x <= 22.5) or ((180 >= x > 157.5) and (-180 <= x <= -157.5)):
                    # checks if the current pixel is greater than the sector neighbors
                    if y >= gradient_mag[ i ][ j - 1 ] and y >= gradient_mag[ i ][ j + 1 ]:
                        suppressed_arr[ i ][ j ] = int(round(y))

                # checking if gradient angle is in 1st sector
                elif (22.5 < x <= 67.5) or (-112.5 >= x > -157.5):
                    # checks if the current pixel is greater than the sector neighbors
                    if y >= gradient_mag[ i - 1 ][ j + 1 ] and y >= gradient_mag[ i + 1 ][ j - 1 ]:
                        suppressed_arr[ i ][ j ] = int(round(y))

                # checking if gradient angle is in 2nd sector
                elif (67.5 < x <= 112.5) or (-67.5 >= x > -112.5):
                    # checks if the current pixel is greater than the sector neighbors
                    if y >= gradient_mag[ i - 1 ][ j ] and y >= gradient_mag[ i + 1 ][ j ]:
                        suppressed_arr[ i ][ j ] = int(round(y))

                # checking if gradient angle is in 3rd sector
                elif (112.5 < x <= 157.5) or (-22.5 >= x > -67.5):
                    # checks if the current pixel is greater than the sector neighbors
                    if y >= gradient_mag[ i - 1 ][ j - 1 ] and y >= gradient_mag[ i + 1 ][ j + 1 ]:
                        suppressed_arr[ i ][ j ] = int(round(y))

    # Writing suppressed matrix
    imwrite(os.path.join(output_path, "non-maxima_suppressed.bmp"), suppressed_arr)
    return suppressed_arr


# Step 4. Thresholding
def double_thresholding(suppressed_image, gradient_angle):
    image_height = suppressed_image.shape[ 0 ]
    image_width = suppressed_image.shape[ 1 ]

    maximum_value = np.amax(suppressed_image)
    high_threshold_ratio = 0.20
    low_threshold_ratio = 0.10

    high_threshold = maximum_value * high_threshold_ratio
    low_threshold = maximum_value * low_threshold_ratio

    output_image = np.empty((image_height, image_width), dtype='int')

    strong_edge_pixel = suppressed_image > high_threshold
    output_image[ strong_edge_pixel ] = 255

    no_edge_pixel = suppressed_image < low_threshold
    output_image[ no_edge_pixel ] = 0
    weak_edge_pixel = (suppressed_image >= low_threshold) & (suppressed_image <= high_threshold)
    index_weak_edge_pixel = np.argwhere(weak_edge_pixel)

    for i in index_weak_edge_pixel:
        x = i[ 0 ]
        y = i[ 1 ]
        pixel_gradient = gradient_angle[ x ][ y ]

        if 0 < x < image_width and 0 < y < image_height:

            # checking if any of the 8 neighbors is a strong edge pixel and classifying the pixel as an edge pixel
            if (((suppressed_image[ x - 1 ][ y ] in strong_edge_pixel) and abs(
                    gradient_angle[ x - 1 ][ y ] - pixel_gradient) > 45) or
                    ((suppressed_image[ x + 1 ][ y ] in strong_edge_pixel) and abs(
                        gradient_angle[ x + 1 ][ y ] - pixel_gradient) > 45) or
                    ((suppressed_image[ x ][ y + 1 ] in strong_edge_pixel) and abs(
                        gradient_angle[ x ][ y + 1 ] - pixel_gradient) > 45) or
                    ((suppressed_image[ x ][ y - 1 ] in strong_edge_pixel) and abs(
                        gradient_angle[ x ][ y - 1 ] - pixel_gradient) > 45) or
                    ((suppressed_image[ x - 1 ][ y + 1 ] in strong_edge_pixel) and abs(
                        gradient_angle[ x - 1 ][ y + 1 ] - pixel_gradient) > 45) or
                    ((suppressed_image[ x - 1 ][ y - 1 ] in strong_edge_pixel) and abs(
                        gradient_angle[ x - 1 ][ y - 1 ] - pixel_gradient) > 45) or
                    ((suppressed_image[ x + 1 ][ y - 1 ] in strong_edge_pixel) and abs(
                        gradient_angle[ x + 1 ][ y - 1 ] - pixel_gradient) > 45) or
                    ((suppressed_image[ x + 1 ][ y - 1 ] in strong_edge_pixel) and abs(
                        gradient_angle[ x + 1 ][ y - 1 ] - pixel_gradient) > 45)):
                output_image[ x ][ y ] = 255

    # writing the output after double thresholding
    imwrite(os.path.join(output_path, "double_thresholding.bmp"), output_image)


def main():
    # input name of image with extensions on which you want to apply Canny Edge Detection
    image = input("Enter image name: ")
    canny(image)
    input()


if __name__ == "__main__":
    main()
