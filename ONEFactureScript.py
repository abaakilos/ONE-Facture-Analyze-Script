import streamlit as st
import fitz  # PyMuPDF
import io
from PIL import Image
import pytesseract
import http.client
import json

pytesseract.pytesseract.tesseract_cmd = r'C:\\Users\\Home\\AppData\\Local\\Programs\\Tesseract-OCR\\tesseract.exe'

# Function to perform OCR on an image
def ocr_image(image):
    # Convert the image to grayscale
    gray_image = image.convert('L')

    # Perform OCR on the grayscale image
    text = pytesseract.image_to_string(gray_image)

    return text

# Initialize HTTP connection
conn = http.client.HTTPSConnection("chatgpt-42.p.rapidapi.com")

headers = {
    'content-type': "application/json",
    'X-RapidAPI-Key': "096e66c0a8mshb1fddf4fb473344p1da386jsn971c26f729a6",
    'X-RapidAPI-Host': "chatgpt-42.p.rapidapi.com"
}

# Upload the PDF file
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
if uploaded_file is not None:
    # Open the PDF file
    pdf_file = fitz.open(stream=uploaded_file.read(), filetype='pdf')

    # Iterate over PDF pages
    for page_index in range(0, len(pdf_file) - 1, 2):  # Process two pages at a time
        text = ""  # Initialize text for the two pages

        # Process two pages
        for i in range(2):
            # Get the page itself
            page = pdf_file[page_index + i]
            image_list = page.get_images(full=True)

            # Iterate over images in the page
            for image_index, img in enumerate(image_list):
                # Extract the image data
                image_data = pdf_file.extract_image(img[0])['image']

                # Save the image as a PIL object
                base_image = Image.open(io.BytesIO(image_data))

                # Perform OCR on the image
                text += ocr_image(base_image) + "\n"

        # Prepare the payload
        payload = json.dumps({
            "messages": [
                {
                    "role": "user",
                    "content": "give me the amount to be paid in this electricity bill : "+text
                }
            ],
            "system_prompt": "",
            "temperature": 0.9,
            "top_k": 5,
            "top_p": 0.9,
            "max_tokens": 256,
            "web_access": False
        })

        # Send the request to the API
        conn.request("POST", "/conversationgpt4", payload, headers)

        # Get the response
        res = conn.getresponse()
        data = res.read()

        # Display the extracted text and the response from the API
        st.text_area(f"Text (Pages {page_index + 1} and {page_index + 2})", text)
        st.text_area(f"API Response (Pages {page_index + 1} and {page_index + 2})", data.decode("utf-8"))
