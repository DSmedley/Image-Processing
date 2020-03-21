from random_word import RandomWords
from random import randrange
import cv2
import os

# TODO: Generate random number to determine how many spots to put the text = DONE
# TODO: Get the height and width of the image = DONE
# TODO: Choose said number of words from random words to put onto the image = DONE
# TODO: Randomly generate a coordinate for where the words will go = DONE
# TODO: Randomly generate a number for font size = DONE
# TODO: Choose random font = DONE
# TODO: Apply the words onto the image = DONE
# TODO: Log the name of the file, text, and text location onto a json object
# TODO: Error handle when random words fail


def dont_overlap():
    something = True
    for current_word in no_text_allowed:
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
            something = False
    return something


def get_random_words():
    r = RandomWords()
    return r.get_random_words()


def get_image_attributes(file):
    original_img = cv2.imread('unclassified_images/' + file)
    original_height = original_img.shape[0]
    original_width = original_img.shape[1]
    return original_img, original_height, original_width


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
            color = (0, 0, 0)

            # Find width and height of the word to make sure the whole word in on the image
            (label_width, label_height), baseline = cv2.getTextSize(word, font, font_scale, thickness)
            while True:
                new_bottom = randrange(label_height + baseline, height)
                new_left = randrange(width - label_width)
                new_top = new_bottom - label_height - baseline
                new_right = new_left + label_width

                if len(no_text_allowed) == 0:
                    break
                if dont_overlap():
                    break
            org = (new_left, new_bottom)
            no_text_allowed.append([new_bottom, new_left, new_top, new_right])
            image = cv2.putText(img, word, org, font, font_scale, color, thickness, cv2.LINE_AA)

        cv2.imshow('image', image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
