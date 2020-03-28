import json
from imutils.object_detection import non_max_suppression
import numpy as np
import time
import cv2

CLASSIFIED_FOLDER = "classified_images1"
DATASET = 'dataset1.json'


def get_detected_text(boxes, words):
    false_positive = 0
    total_found = 0
    total_percentage = 0
    for (found_left, found_top, found_right, found_bottom) in boxes:
        found = False
        for word in words:
            left = word['left']
            top = word['top']
            right = word['right']
            bottom = word['bottom']

            centerX = right - (right - left) / 2
            centerY = bottom - (bottom - top) / 2

            if found_left < centerX < found_right and found_top < centerY < found_bottom:
                found = True
                total_found += 1
                area = (bottom - top) * (right - left)
                area_top, area_bottom, area_left, area_right = top, bottom, left, right
                # Check if found top is in the acceptable range
                if top < found_top < bottom:
                    area_top = found_top
                # Check if found bottom is in the acceptable range
                if top < found_bottom < bottom:
                    area_bottom = found_bottom
                # Check if found left is in the acceptable range
                if left < found_left < right:
                    area_left = found_left
                # Check if found right is in the acceptable range
                if left < found_right < right:
                    area_right = found_right
                found_area = (area_bottom - area_top) * (area_right - area_left)
                total_percentage += found_area / area
        if not found:
            false_positive += 1
    return false_positive, total_found, total_percentage


def analyze(image, words):
    # load the input image and grab the image dimensions
    image = cv2.imread(f'{CLASSIFIED_FOLDER}/{image}')
    orig = image.copy()
    (H, W) = image.shape[:2]

    # set the new width and height and then determine the ratio in change
    # for both the width and height
    # width and height is 320 x 320
    (newW, newH) = (320, 320)
    rW = W / float(newW)
    rH = H / float(newH)

    # resize the image and grab the new image dimensions
    image = cv2.resize(image, (newW, newH))
    (H, W) = image.shape[:2]

    # define the two output layer names for the EAST detector model that
    # we are interested -- the first is the output probabilities and the
    # second can be used to derive the bounding box coordinates of text
    layerNames = [
        "feature_fusion/Conv_7/Sigmoid",
        "feature_fusion/concat_3"]

    # load the pre-trained EAST text detector
    net = cv2.dnn.readNetFromTensorflow('frozen_east_text_detection.pb')

    # construct a blob from the image and then perform a forward pass of
    # the model to obtain the two output layer sets
    blob = cv2.dnn.blobFromImage(image, 1.0, (W, H),
                                 (123.68, 116.78, 103.94), swapRB=True, crop=False)
    start = time.time()
    net.setInput(blob)
    (scores, geometry) = net.forward(layerNames)
    end = time.time()
    time_spent = end-start

    # grab the number of rows and columns from the scores volume, then
    # initialize our set of bounding box rectangles and corresponding
    # confidence scores
    (numRows, numCols) = scores.shape[2:4]
    rects = []
    confidences = []

    # loop over the number of rows
    for y in range(0, numRows):
        # extract the scores (probabilities), followed by the geometrical
        # data used to derive potential bounding box coordinates that
        # surround text
        scoresData = scores[0, 0, y]
        xData0 = geometry[0, 0, y]
        xData1 = geometry[0, 1, y]
        xData2 = geometry[0, 2, y]
        xData3 = geometry[0, 3, y]
        anglesData = geometry[0, 4, y]

        # loop over the number of columns
        for x in range(0, numCols):
            # if our score does not have sufficient probability, ignore it
            # minimum probability required to inspect a region
            min_confidence = .5  # default
            if scoresData[x] < min_confidence:
                continue

            # compute the offset factor as our resulting feature maps will
            # be 4x smaller than the input image
            (offsetX, offsetY) = (x * 4.0, y * 4.0)

            # extract the rotation angle for the prediction and then
            # compute the sin and cosine
            angle = anglesData[x]
            cos = np.cos(angle)
            sin = np.sin(angle)

            # use the geometry volume to derive the width and height of
            # the bounding box
            h = xData0[x] + xData2[x]
            w = xData1[x] + xData3[x]

            # compute both the starting and ending (x, y)-coordinates for
            # the text prediction bounding box
            endX = int(offsetX + (cos * xData1[x]) + (sin * xData2[x]))
            endY = int(offsetY - (sin * xData1[x]) + (cos * xData2[x]))
            startX = int(endX - w)
            startY = int(endY - h)

            # add the bounding box coordinates and probability score to
            # our respective lists
            rects.append((startX, startY, endX, endY))
            confidences.append(scoresData[x])

    # apply non-maxima suppression to suppress weak, overlapping bounding
    # boxes
    boxes = non_max_suppression(np.array(rects), probs=confidences)
    boxes = [[int(a * b) for a, b in zip(box, [rW, rH, rW, rH])] for box in boxes]

    # show_found_box(boxes, orig)
    # show_original_box(words, orig)
    false, found, percentage = get_detected_text(boxes, words)
    return false, found, percentage, time_spent


def show_found_box(boxes, orig):
    for (startX, startY, endX, endY) in boxes:
        # draw the bounding box on the image
        cv2.rectangle(orig, (startX, startY), (endX, endY), (0, 0, 255), 2)
    cv2.imshow("Text Detection", orig)
    cv2.waitKey(0)


def show_original_box(words, orig):
    for word in words:
        # draw the bounding box on the image
        cv2.rectangle(orig, (word['left'], word['top']), (word['right'], word['bottom']), (0, 255, 0), 2)
    # show the output image
    cv2.imshow("Text Detection", orig)
    cv2.waitKey(0)


with open(DATASET) as json_file:
    data = json.load(json_file)
    images = data['images']
    total_false, total_found, total_percentage, total_words, total_time = 0, 0, 0, 0, 0
    print("Started Analysis")
    for image in images:
        for image_name, texts in image.items():
            print(f"Analyzing image {image_name}")
            false, found, percentage, time_spent = analyze(image_name, texts)
            total_false += false
            total_found += found
            total_percentage += percentage
            total_words += len(texts)
            total_time += time_spent
    print(f"Total false positives: {total_false}")
    print(f"Total found: {total_found}")
    print(f"Total percentage: {total_percentage}")
    print(f"Total words: {total_words}")
    print(f"Percentage of words found: {total_found/total_words}")
    print(f"Average percentage of word detected: {total_percentage/total_found}")
    print(f"Average time to analyze: {total_time/len(images)}")
