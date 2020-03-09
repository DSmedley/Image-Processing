from skimage import io
import cv2


def text_detect(input, ele_size=(8, 2)):
    print(input.shape)
    print(len(input.shape))
    # If image is colored
    if len(input.shape) == 3:
        print("Equals 3")
        # Turn to black and white
        test = cv2.cvtColor(input, cv2.COLOR_BGR2GRAY)
        cv2.imwrite("1.png", test)
    # inverts colors
    img_sobel = cv2.Scharr(test, cv2.CV_8U, 1, 0)
    img_sobel2 = cv2.Sobel(test, cv2.CV_8U, 0, 1)
    cv2.imwrite("2.png", img_sobel)
    cv2.imwrite("3.png", img_sobel2)
    img_threshold = cv2.threshold(img_sobel, 0, 255, cv2.THRESH_OTSU + cv2.THRESH_BINARY)
    print(img_threshold)
    element = cv2.getStructuringElement(cv2.MORPH_RECT, ele_size)
    img_threshold = cv2.morphologyEx(img_threshold[1], cv2.MORPH_CLOSE, element)
    res = cv2.findContours(img_threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    if cv2.__version__.split(".")[0] == '3':
        _, contours, hierarchy = res
    else:
        contours, hierarchy = res
    Rect = [cv2.boundingRect(i) for i in contours if i.shape[0] > 100]
    RectP = [(int(i[0] - i[2] * 0.08), int(i[1] - i[3] * 0.08), int(i[0] + i[2] * 1.1), int(i[1] + i[3] * 1.1)) for i in
             Rect]
    return RectP


def main(input_file):
    outputFile = input_file.split('.')[0] + '-rect.' + '.'.join(input_file.split('.')[1:])
    print(outputFile)
    img = io.imread(input_file)
    rect = text_detect(img)
    print(rect)
    for i in rect:
        print(i[:2])
        print(i[2:])
        # image, upper left, lower right, color
        cv2.rectangle(img, i[:2], i[2:], (0, 0, 255))
    cv2.imwrite(outputFile, img)


if __name__ == '__main__':
    main("ML-ImageTest.png")
