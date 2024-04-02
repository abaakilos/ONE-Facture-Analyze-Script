import streamlit as st
import fitz  # PyMuPDF
import io
from PIL import Image
import base64
from openai import OpenAI
import json

# OpenAI API Key
api_key = "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"

client = OpenAI(api_key=api_key)


def send_request_to_api(base64_image1, base64_image2, prompt):
    response = client.chat.completions.create(
        model="gpt-4-vision-preview",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt,
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



prompt1 = ("Extract the following information in json format: "
           "{"
           "\"heures_de_pointes\": { \"nouveau\": \"\", \"ancien\": \"\", \"difference\": \"\", \"consommation_kWh\": \"\", \"prix_unitaire_HT_DH\": \"\", \"montant_DH_HT\": \"\" }, "
           "\"heures_pleines\": { \"nouveau\": \"\", \"ancien\": \"\", \"difference\": \"\", \"consommation_kWh\": \"\", \"prix_unitaire_HT_DH\": \"\", \"montant_DH_HT\": \"\" }, "
           "\"heures_creuses\": { \"nouveau\": \"\", \"ancien\": \"\", \"difference\": \"\", \"consommation_kWh\": \"\", \"prix_unitaire_HT_DH\": \"\", \"montant_DH_HT\": \"\" }, "
           "\"Type de tarif\": \"\", "
           "\"Date de releve\": \"\", "
           "\"Mois de Facturation\": \"\", "
           "\"Total a regler\": \"\" "
           "}")


prompt2 = ("Extract the following information in json format: 'Puissance Installe', 'Puissance a vide', "
           "'Type compteur', 'Option Tarifiaire', 'Energie active', 'Energie reactive', 'CosPhi', 'Puissance "
           "Souscrite', 'Dépassement Puissance', 'Redevance Comptage', 'Total HT', 'TVA' (pour chaque pourcentage)")

prompt3 = ("Agis comme un expert en électricité et efficacité énergétique et en prenant en considération le cas d'une entreprise agricole dans le contexte marocain"
           " qui souhaite optimiser la consommation d'energie analyse la facture suivante et fais un diagnostic détaillé selon le contexte de l'ONE au Maroc et donne"
           " les recommandations nécessaires. Take a deep breath and do it step by step")



# Upload the PDF file
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
if uploaded_file is not None:
    # Open the PDF file
    pdf_file = fitz.open(stream=uploaded_file.read(), filetype='pdf')

    # Iterate over PDF pages
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


        api_response1 = send_request_to_api(images[0], images[1], prompt1)
        api_response2 = send_request_to_api(images[0], images[1], prompt2)
        api_response3 = send_request_to_api(images[0], images[1], prompt3)

        # Extract the content from the API response
        content1 = api_response1.message.content
        content2 = api_response2.message.content
        # print(api_response)

        # Find the start and end of the JSON part
        start1 = content1.find('{')
        end1 = content1.rfind('}') + 1

        start2 = content2.find('{')
        end2 = content2.rfind('}') + 1

        # Extract the JSON part
        json_part1 = content1[start1:end1]
        json_part2 = content2[start2:end2]


        # Display the response from the API
        st.text_area(f"API Response (Pages {page_index + 1} and {page_index + 2}) - Part 1",
                     json_part1)
        st.text_area(f"API Response (Pages {page_index + 1} and {page_index + 2}) - Part 2",
                     json_part2)
        st.text_area(f"API Response (Pages {page_index + 1} and {page_index + 2}) - Part 3",
                     api_response3.message.content)
