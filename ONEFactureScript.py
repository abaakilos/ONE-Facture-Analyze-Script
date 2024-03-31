import streamlit as st
import fitz  # PyMuPDF
import io
from PIL import Image
import base64
from openai import OpenAI
import requests

# OpenAI API Key
api_key = "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"

client = OpenAI(api_key=api_key)

def send_request_to_api(base64_image1, base64_image2):
    response = client.chat.completions.create(
        model="gpt-4-vision-preview",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Ces deux images represente une facture de ma societe au Maroc,"
                                "Donne moi en json format les prix unitaire des heures de pointe, heures pleines, et heures creuses",
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image1}",
                        },
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image2}",
                        },
                    },
                ],
            }
        ],
        max_tokens=300,
    )
    return response.choices[0]

# Upload the PDF file
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
if uploaded_file is not None:
    # Open the PDF file
    pdf_file = fitz.open(stream=uploaded_file.read(), filetype='pdf')

    # Iterate over PDF pages
    for page_index in range(0, len(pdf_file) - 1, 2):  # Process two pages at a time
        images = []  # Initialize images for the two pages

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

                # Convert the image to base64
                buffered = io.BytesIO()
                base_image.save(buffered, format="JPEG")
                img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')

                # Add the base64 image to the list
                images.append(img_str)

        # Send the request to the API and get the response
        api_response = send_request_to_api(images[0], images[1])

        # Display the response from the API
        st.text_area(f"API Response (Pages {page_index + 1} and {page_index + 2})",
                     str(api_response), key=f"API Response {page_index + 1}-{page_index + 2}")