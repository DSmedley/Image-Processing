from random_word import RandomWords
from random import randrange
import cv2
import os

# TODO: Generate random number to determine how many spots to put the text = DONE
# TODO: Get the height and width of the image = DONE
# TODO: Choose said number of words from random words to put onto the image = DONE
# TODO: Randomly generate a coordinate for where the words will go = DONE
# TODO: Randomly generate a number for font size
# TODO: Choose random font
# TODO: Apply the words onto the image
# TODO: Log the name of the file, text, and text location onto a json object


if __name__ == "__main__":
    # Loop through the directory using each image
    for filename in os.listdir('unclassified_images'):
        r = RandomWords()
        number_of_words = randrange(5)
        random_words = r.get_random_words()

        img = cv2.imread('unclassified_images/' + filename)

        height = img.shape[0]
        width = img.shape[1]

        no_text_allowed = []

        for i in range(5):
            # TODO: make sure the coordinates dont overlap so words dont overlap
            word = random_words[randrange(49)]

            font = randrange(7)
            thickness = 2
            #TODO: Randomize these parameters
            fontScale = 1
            color = (0, 0, 0)

            # Find width and height of the word to make sure the whole word in on the image
            (label_width, label_height), baseline = cv2.getTextSize(word, font, fontScale, thickness)

            while True:
                random_height = randrange(height - label_height - baseline)
                random_width = randrange(width - label_width)

                print(no_text_allowed)
                if len(no_text_allowed) == 0:
                    break

                for i in no_text_allowed:
                    if((random_height < i[0] or random_height > i[2]) and (random_width < i[1] or random_width > i[3])):
                        break

            org = (random_width, random_height)

            no_text_allowed.append([random_height, random_width, label_height+baseline+random_height, random_width+label_width])

            image = cv2.putText(img, word, org, font, fontScale, color, thickness, cv2.LINE_AA)

        cv2.imshow('image', image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
