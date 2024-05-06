import cv2
import pytesseract
from pytesseract import Output

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe"

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
        green = (0, 255, 0)
        thickness = 3  # pixels

        cv2.rectangle(img, top_left, bottom_right, green, thickness)

    # Display the image with bounding boxes
    cv2.imshow('Image with Bounding Boxes', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
 
    input_image_path = "ow.png"
    
    extract_text_and_draw_boxes(input_image_path)
