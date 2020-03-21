from random_words import RandomWords
from random import randrange
import cv2
import os
from PIL import Image


# TODO: Generate random number to determine how many spots to put the text = DONE
# TODO: Get the height and width of the image = DONE
# TODO: Choose said number of words from random words to put onto the image = DONE
# TODO: Randomly generate a coordinate for where the words will go = DONE
# TODO: Randomly generate a number for font size = DONE
# TODO: Choose random font = DONE
# TODO: Apply the words onto the image = DONE
# TODO: Log the name of the file, text, and text location onto a json object
# TODO: Error handle when random words fail


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


def get_image_attributes(file):
    original_img = cv2.imread('unclassified_images/' + file)
    original_height = original_img.shape[0]
    original_width = original_img.shape[1]
    return original_img, original_height, original_width


def get_text_location(new_word, new_font, new_font_scale, new_thickness):
    # Find width and height of the word to make sure the whole word in on the image
    (label_width, label_height), baseline = cv2.getTextSize(new_word, new_font, new_font_scale, new_thickness)
    while True:
        new_bottom = randrange(label_height + baseline, height)
        new_left = randrange(width - label_width)
        word_height = label_height + baseline
        new_top = new_bottom - word_height
        new_right = new_left + label_width

        if len(no_text_allowed) == 0:
            break
        if dont_overlap(new_bottom, new_left, new_top, new_right, no_text_allowed):
            break
    return new_bottom, new_left, new_top, new_right


if __name__ == "__main__":
    # Loop through the directory using each image
    for filename in os.listdir('unclassified_images'):
        random_words = get_random_words()
        img, height, width = get_image_attributes(filename)
        no_text_allowed = []

        for i in range(randrange(15)):
            # TODO: make sure the coordinates dont overlap so words dont overlap = DONE
            word = random_words[randrange(49)]
            font = randrange(7)
            thickness = 2
            # TODO: Randomize these parameters
            font_scale = randrange(1, 2)

            bottom, left, top, right = get_text_location(word, font, font_scale, thickness)
            im = Image.open('unclassified_images/' + filename)  # Can be many different formats.
            pix = im.load()
            print(im.size)  # Get the width and hight of the image for iterating over
            print(pix[left, bottom])  # Get the RGBA Value of the a pixel of an image
            font_color = tuple(map(lambda i, j: i - j, pix[left, bottom], (255, 255, 255)))
            print([(abs(i)) for i in font_color])
            color = [(abs(i)) for i in font_color]
            org = (left, bottom)
            no_text_allowed.append([bottom, left, top, right])
            img = cv2.putText(img, word, org, font, font_scale, color, thickness, cv2.LINE_AA)

        cv2.imshow('image', img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
