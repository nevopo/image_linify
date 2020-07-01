import numpy as np
import cv2
import os
from datetime import datetime
DESTINATION_DIRECTORY = r'C:\Users\Nevo Poran\PycharmProjects\image_artifier\modified_images'
TEST_IMAGE = r'C:\Users\Nevo Poran\PycharmProjects\image_artifier\images\spirited_away.jpg'


def save_image_to_destination_folder(image, output_dir=DESTINATION_DIRECTORY, image_format="png"):
    """
    saves an image variable to file
    :param image: image to save
    :param output_dir: where to save to, default is script folder
    :param image_format: which format to save in, default - png
    :return: 1 for success, else for failures
    """
    if os.path.exists(output_dir) is not True:
        print(OSError("The given directory does not exist! - {0}".format(output_dir)))
        return -1

    os.chdir(DESTINATION_DIRECTORY)
    destination_filename = "output.{}".format(image_format)
    cv2.imwrite(destination_filename, image)
    if os.path.exists(os.path.join(output_dir, destination_filename)):
        print("Image Saved Successfully")
        return 1
    else:
        print("Image Saved Failure!")
        return -2


def get_image_size_size(img):
    """
    gets an image and returns its' dimensions
    :param img: source image
    :return: (<width>, <height>)
    """
    return tuple(img.shape[1::-1])


def create_blank_image(dimensions, default_color=(255, 255, 255)):
    """
    Creates blank image to return to the user
    :param dimensions: target dimensions
    :param default_color: the base color for the blank image, default value is white
    :return: the newly created image
    """
    blank_image = np.zeros((dimensions[1], dimensions[0], 3), np.uint8)
    blank_image[:, :] = default_color
    return blank_image


def remove_small_contours(image, removal_threshold=50):
    """
    Gets an image and removes any contour smaller the given value
    :param image: for this function to work upon
    :param removal_threshold: size in pixels amount, any thing smaller will be removed
    :return:
    """
    # Filter using contour area and remove small noise
    contours = cv2.findContours(image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = contours[0] if len(contours) == 2 else contours[1]
    for contour in contours:
        area = cv2.contourArea(contour)
        if area < removal_threshold:
            cv2.drawContours(image, [contour], -1, (0, 0, 0), -1)

    # Morph close and invert image
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    close = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel, iterations=2)
    return close


def linify_image(binary_image, image_dimensions, line_width=1, line_spacing=3, reference_image=None):
    """
    This function receives the binary image to filter upon, and copies info based on the iterations
    params:
        binary_image - receives an black or white image
        image_dimensions - the size of the source image, passed and not recalculated for optimization
        line_width - the stripe's width
        line_spacing - amount of white lines between image info
        reference_image - if given, will take the colors from this image instead of black and white output

    """
    new_image = create_blank_image(image_dimensions)
    for w in range(int(image_dimensions[0])):
        for h in range(image_dimensions[1]):
            # print(int(w/line_spacing) == (w/line_spacing))
            if binary_image[h, w] != 255 and int(w/line_spacing) == (w/line_spacing):
                if reference_image is None:
                    new_image[h, w:w+line_width] = (0, 0, 0)
                else:
                    new_image[h, w:w + line_width] = reference_image[h, w]

    save_image_to_destination_folder(new_image)
    return new_image


def main():
    # get the source image file
    original_image = cv2.imread(TEST_IMAGE)
    # calculations and color processing are based on gray scaled images
    gray_space_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
    # get image dimensions
    image_size = get_image_size_size(original_image)
    # get the binary image
    (thresh, black_and_white_image) = cv2.threshold(gray_space_image, 130, 255, cv2.THRESH_BINARY)
    # remove recreate the base image based on bigger contours
    after_morphology = remove_small_contours(black_and_white_image)
    # smoothing things out with gaussian blur
    after_blur = cv2.GaussianBlur(after_morphology, (13, 13), 0)
    after_smoothing = cv2.threshold(after_blur, 100, 255, cv2.THRESH_BINARY)[1]

    # a variable for final version before linifying, for clearer code
    processed_image = after_smoothing

    # calling the star of the show!
    output_image = linify_image(processed_image, image_size, 2, 5, original_image)

    # Debug section!!!
    # cv2.imshow("The Original Image", original_image)
    # cv2.imshow("The Grayed Out Image", gray_space_image)
    # cv2.imshow("The B&W Image", black_and_white_image)
    # cv2.imshow("No Small Contours", after_morphology)
    # cv2.imshow("After Blur!", after_smoothing)
    cv2.imshow("Lines Lines Lines !", output_image)

    cv2.waitKey(0)
    cv2.destroyAllWindows()
    pass


if __name__ == '__main__':
    try:
        main()
    except Exception as job_error:
        raise RuntimeError("Runtime Error occurred - {0}".format(job_error))
