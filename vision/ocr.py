from PIL import Image
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extract_text_from_image(image):
    """
    "Give me all of this in English and what do triple quotes do? Receives a frame (Frame) of OpenCV or a PIL Image and returns the text that appears in it."
    """
    # אם זה מסגרת OpenCV (numpy array), נהפוך ל-PIL Image
    if not isinstance(image, Image.Image):
        image = Image.fromarray(image)
    
    text = pytesseract.image_to_string(image)
    return text
