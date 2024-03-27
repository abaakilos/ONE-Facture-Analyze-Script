import streamlit as st
import fitz  # PyMuPDF
import io
from PIL import Image
import pytesseract



pytesseract.pytesseract.tesseract_cmd = r'C:\Users\Home\AppData\Local\Programs\Tesseract-OCR/tesseract.exe'
# Function to perform OCR on an image
def ocr_image(image):
    # Convert the image to grayscale
    gray_image = image.convert('L')

    # Perform OCR on the grayscale image
    text = pytesseract.image_to_string(gray_image)

    return text


# Upload the PDF file
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
if uploaded_file is not None:
    # Open the PDF file
    pdf_file = fitz.open(stream=uploaded_file.read(), filetype='pdf')

    # Iterate over PDF pages
    for page_index in range(0, len(pdf_file), 2):  # Skip every second page
        # Get the page itself
        page = pdf_file[page_index]
        image_list = page.get_images(full=True)

        # Iterate over images in the page
        for image_index, img in enumerate(image_list):
            # Extract the image data
            image_data = pdf_file.extract_image(img[0])['image']

            # Save the image as a PIL object
            base_image = Image.open(io.BytesIO(image_data))

            # Perform OCR on the image
            text = ocr_image(base_image)

            # Display the extracted text
            st.text_area(f"Text (Page {page_index + 1}, Image {image_index + 1})", text)
