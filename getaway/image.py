import cv2

__all__ = ['geta_zoom']


def geta_zoom(img, scale=10):
    #get the webcam size
    height, width, channels = img.shape

    # print(img[0:2])
    # prepare the crop
    centerX, centerY = int(height / 2), int(width / 2)
    radiusX, radiusY = int(scale * height / 100), int(scale * width / 100)

    minX, maxX = centerX - radiusX, centerX + radiusX
    minY, maxY = centerY - radiusY, centerY + radiusY

    cropped = img[minX:maxX, minY:maxY]
    resized_cropped = cv2.resize(cropped, (width, height))

    return resized_cropped

