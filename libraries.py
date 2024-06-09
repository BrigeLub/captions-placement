import cv2
import pytesseract
from pytesseract import Output
import os
import random

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe"

def count_text_boxes_in_box(data, box):
    x1, y1, x2, y2 = box
    n_boxes = len(data["text"])
    count = 0

    for i in range(n_boxes):
        # Skip -1 confidence, because they correspond with blocks of text
        if data["conf"][i] == -1:
            continue
        # Coordinates of the text box
        x, y = data["left"][i], data["top"][i]
        w, h = data["width"][i], data["height"][i]
        text_box = (x, y, x + w, y + h)

        # Check if the text box overlaps with the given box
        if (x1 < text_box[2] and x2 > text_box[0] and y1 < text_box[3] and y2 > text_box[1]):
            count += 1
    return count

def draw_boxes_at_edges(img, data, box_names, num_boxes=3):
    height, width, _ = img.shape

    # Define the height of the boxes (5% of the image height)
    box_height = int(height * 0.05)
    box_width = int(width / num_boxes)
    text_counts = {}

    # Top row
    for i in range(num_boxes):
        top_left = (i * box_width, 0)
        bottom_right = ((i + 1) * box_width, box_height)
        box = (top_left[0], top_left[1], bottom_right[0], bottom_right[1])
        box_name = list(box_names.keys())[i]
        text_count = count_text_boxes_in_box(data, box)
        text_counts[box_name] = text_count
   
        cv2.rectangle(img, top_left, bottom_right, (255, 255, 255), 3)

    # Bottom row
    for i in range(num_boxes):
        top_left = (i * box_width, height - box_height)
        bottom_right = ((i + 1) * box_width, height)
        box = (top_left[0], top_left[1], bottom_right[0], bottom_right[1])
        box_name = list(box_names.keys())[num_boxes + i]
        text_count = count_text_boxes_in_box(data, box)
        text_counts[box_name] = text_count
      
        cv2.rectangle(img, top_left, bottom_right, (255, 255, 255), 3)

    # Find the box with the least amount of text
    min_text_box = min(text_counts, key=text_counts.get)
    min_text_box_index = list(box_names.keys()).index(min_text_box)

    if min_text_box_index < num_boxes:
        # It's a top row box
        top_left = (min_text_box_index * box_width, 0)
        bottom_right = ((min_text_box_index + 1) * box_width, box_height)
    else:
        # It's a bottom row box
        min_text_box_index -= num_boxes
        top_left = (min_text_box_index * box_width, height - box_height)
        bottom_right = ((min_text_box_index + 1) * box_width, height)

    cv2.putText(img, "Captions go here!", (top_left[0] + 10, top_left[1] + box_height // 2),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

def extract_text_and_draw_boxes(image_path):
    # Read the image using OpenCV
    img = cv2.imread(image_path)

    # Extract recognized data
    data = pytesseract.image_to_data(img, output_type=Output.DICT)
    n_boxes = len(data["text"])

    for i in range(n_boxes):
        # Skip -1 confidence, because they correspond with blocks of text
        if data["conf"][i] == -1:
            continue
        # Coordinates
        x, y = data["left"][i], data["top"][i]
        w, h = data["width"][i], data["height"][i]

        # Corners
        top_left = (x, y)
        bottom_right = (x + w, y + h)

        # Box params
        red = (0, 0, 255)
        thickness = 3  # pixels

        cv2.rectangle(img, top_left, bottom_right, red, thickness)

    # Define box names and initial states
    box_names = {"alpha": True, "beta": True, "gamma": True, "delta": True, "epsilon": True, "zeta": True}

    # Draw additional boxes at the top and bottom
    draw_boxes_at_edges(img, data, box_names)

    # Display the image with bounding boxes
    cv2.imshow('Image with Bounding Boxes', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

  
if __name__ == "__main__":
    folder_path = "C:/Users/Brigitte/Documents/GitHub/captions-placement" 

    # Get a list of all .png files in the folder
    png_files = [f for f in os.listdir(folder_path) if f.endswith('.png')]
    print(png_files)
    # Select a random .png file from the list
    if png_files:
        input_image_path = os.path.join(folder_path, random.choice(png_files))
        extract_text_and_draw_boxes(input_image_path)
    else:
        print("No .png files found in the specified folder.")
