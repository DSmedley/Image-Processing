import re
from random import randrange

import cv2
import json
import os
import time
import wcag_contrast_ratio as contrast
from PIL import Image
from random_words import RandomWords

# TODO: Generate random number to determine how many spots to put the text = DONE
# TODO: Get the height and width of the image = DONE
# TODO: Choose said number of words from random words to put onto the image = DONE
# TODO: Randomly generate a coordinate for where the words will go = DONE
# TODO: Randomly generate a number for font size = DONE
# TODO: Choose random font = DONE
# TODO: Apply the words onto the image = DONE
# TODO: Log the name of the file, text, and text location onto a json object
# TODO: Error handle when random words fail = Done

UNCLASSIFIED_FOLDER = "unclassified_images1"
DATASET = 'dataset1.json'


def dont_overlap(new_bottom, new_left, new_top, new_right, current_words):
    not_overlapped = True
    for current_word in current_words:
        old_bottom = current_word[0]
        old_left = current_word[1]
        old_top = current_word[2]
        old_right = current_word[3]

        # Based on new word
        new_bottom_higher_old_top = new_bottom < old_top
        new_top_lower_old_bottom = new_top > old_bottom
        new_left_right_old_right = new_left > old_right
        new_right_left_old_left = new_right < old_left
        if not (new_bottom_higher_old_top or
                new_top_lower_old_bottom or
                new_left_right_old_right or
                new_right_left_old_left):
            not_overlapped = False
    return not_overlapped


def get_random_words():
    r = RandomWords()
    try:
        return r.random_words(count=50)
    except:
        print("Error: Invalid word")
        get_random_words()


def resize_image(image, old_width, old_height):
    scale_percentage = old_width / 1280
    new_height = int(old_height / scale_percentage)

    return cv2.resize(image, (1280, new_height)), 1280, new_height


def get_image_attributes(file):
    original_img = cv2.imread(UNCLASSIFIED_FOLDER + '/' + file)
    original_height = original_img.shape[0]
    original_width = original_img.shape[1]

    if original_width > 1280:
        original_img, original_width, original_height = resize_image(original_img, original_width, original_height)

    return original_img, original_height, original_width


def get_text_location(new_word, new_font, new_font_scale, new_thickness, no_text, height, width):
    # Find width and height of the word to make sure the whole word in on the image
    (label_width, label_height), baseline = cv2.getTextSize(new_word, new_font, new_font_scale, new_thickness)
    while True:
        word_height = label_height
        new_bottom = randrange(word_height, height)
        new_left = randrange(width - label_width)
        new_top = new_bottom - word_height
        new_right = new_left + label_width

        if len(no_text) == 0:
            break
        if dont_overlap(new_bottom, new_left, new_top, new_right, no_text):
            break
    return new_bottom, new_left, new_top, new_right, baseline


def write_json(image_name, array):
    with open(DATASET) as json_file:
        data = json.load(json_file)
        temp = data['images']
        # python object to be appended
        new_image = {image_name: []}
        temp2 = new_image[image_name]
        for word in array:
            word_attributes = {'text': word[4], 'bottom': word[0], 'left': word[1], 'top': word[2], 'right': word[3]}
            temp2.append(word_attributes)
        # appending data to emp_details
        temp.append(new_image)

    with open(DATASET, 'w') as f:
        json.dump(data, f, indent=4)


def get_font_color(color):
    choices = [(1.0, 0, 0), (0, 1.0, 0), (0, 0, 1.0)]
    if isinstance(color, int):
        color = (color, color, color)
    font_color = tuple(map(lambda s, j: s / j, color, (255, 255, 255)))
    selected = 0
    highest = 0
    for choice in range(len(choices)):
        value = contrast.rgb(choices[choice], font_color)
        if value > highest:
            highest = value
            selected = choice
    return tuple(map(lambda s, j: s * j, choices[selected], (255, 255, 255)))


def classify():
    # Loop through the directory using each image
    for filename in os.listdir(UNCLASSIFIED_FOLDER):
        ts = time.time()
        im = Image.open(UNCLASSIFIED_FOLDER + '/' + filename)  # Can be many different formats.
        pix = im.load()
        img, height, width = get_image_attributes(filename)

        # Use each image 40 times
        for k in range(40):
            random_words = get_random_words()
            no_text_allowed = []
            new_img = img.copy()

            for q in range(randrange(15)):
                # TODO: make sure the coordinates dont overlap so words dont overlap = DONE
                word = random_words[randrange(49)]
                font = randrange(4)
                thickness = 2
                # TODO: Randomize these parameters = DONE
                font_scale = 1

                bottom, left, top, right, base = get_text_location(word, font, font_scale, thickness, no_text_allowed,
                                                                   height, width)
                font_color = get_font_color(pix[left, bottom])
                org = (left, bottom)
                if re.search(r"\b\w*[gjpqy]\w*\b", word):
                    print(f"Match word: {word}")
                    bottom = bottom + base
                no_text_allowed.append([bottom, left, top, right, word])
                new_img = cv2.putText(new_img, word, org, font, font_scale, font_color, thickness, cv2.LINE_AA)

            # cv2.imshow('image', new_img)
            # cv2.waitKey(0)
            # cv2.destroyAllWindows()

            new_file_name = str(ts) + '_' + str(k) + '.jpg'
            write_json(new_file_name, no_text_allowed)
            cv2.imwrite('classified_images1/' + new_file_name, new_img)


classify()

# TODO: Create an classified folder for classified images - DONE
# TODO: Append image count to image name - DONE
# TODO: Append JSON to store the file name, text, and text location - DONE
