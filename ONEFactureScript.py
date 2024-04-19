import streamlit as st
import fitz  # PyMuPDF
import io
from PIL import Image
import base64
from openai import OpenAI
from ReportGen import generate_report
import json

# OpenAI API Key
api_key = "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"

client = OpenAI(api_key=api_key)

i = 0

data_list = []

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
        max_tokens=600,
    )
    return response.choices[0]



prompt1 = ("Extract the following information in json format, if there is a number give to me as a number not as a string, don't forget any element I will give toy, because I will use it directly from your answer: "
           "{"
           "\"heures_de_pointes\": { \"puissance_appelee\": \"\", \"difference\": \"\", \"consommation_kWh\": \"\", \"prix_unitaire_HT_DH\": \"\", \"montant_DH_HT\": \"\" }, "
           "\"heures_pleines\": { \"puissance_appelee\": \"\", \"difference\": \"\", \"consommation_kWh\": \"\", \"prix_unitaire_HT_DH\": \"\", \"montant_DH_HT\": \"\" }, "
           "\"heures_creuses\": { \"puissance_appelee\": \"\", \"difference\": \"\", \"consommation_kWh\": \"\", \"prix_unitaire_HT_DH\": \"\", \"montant_DH_HT\": \"\" } "
           #"'Total_HT', 'TVA' (pour chaque pourcentage)"
           #'{"Puissance_Installe":"","Puissance_a_vide":"","Mois_de_Consomation":"","Total_a_regler":"","Destinataire":"","N_Client":"","Type_compteur":"","Option_Tarifiaire":"","Energie_active":{"nouveau":"","ancien":"","difference":""},'
           #'"Energie_reactive": "","CosPhi":"","Puissance_Souscrite":{"quantite":"","prix_unitaire":"","montant":""},"Depassement_Puissance":"", "Redevance_comptage":{"location":"","entretien":""},"interets_retard":""}, "Puissance_Appelee": {}}'
           "}, don't add any comments do the json")


prompt2 = ("Extract the following information in json format, if there is a number give to me as a number not as a string, don't make any mistake in the json format, because I will use it directly from your answer:"
           "'Total_HT', 'TVA' (pour chaque pourcentage)"
           "but return such that it will be the first part of a json, it will be added to another json string at the first line, so that it makes one, and give me only the json, don't write anything else"
           "don't add any comments do the json"
           )

prompt3 = ("Extract the following information in json format, if there is a number give to me as a number not as a string, don't make any mistake in the json format, because I will use it directly from your answer"
    '{"Puissance_Installe":"","Puissance_a_vide":"","Mois_de_Consomation":"","Total_a_regler":"","Destinataire":"","N_Client":"","Type_compteur":"","Option_Tarifiaire":"","Energie_active":{"nouveau":"","ancien":"","difference":""},'
    '"Energie_reactive":{"nouveau":"","ancien":"","difference":""},"CosPhi":"","Puissance_Souscrite":{"quantite":"","prix_unitaire":"","montant":""},"Depassement_Puissance":"", "Redevance_comptage":{"location":"","entretien":""},"interets_retard":""}}'
    "but return such that it will be the first part of a json, it will be added to another json string at the first line, so that it makes one, If you don't find any value, make it a 0."
    "don't add any comments do the json"
    )

prompt4 = ("Agis comme un expert en électricité et efficacité énergétique et en prenant en considération le cas d'une entreprise agricole dans le contexte marocain"
           " qui souhaite optimiser la consommation d'energie analyse la facture suivante et fais un diagnostic détaillé selon le contexte de l'ONE au Maroc et donne"
           " les recommandations nécessaires. Take a deep breath and do it step by step")

j = 0


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
        api_response4 = send_request_to_api(images[0], images[1], prompt4)

        content1 = api_response1.message.content
        content2 = api_response2.message.content
        content3 = api_response3.message.content
        # print(api_response)

        # Find the start and end of the JSON part
        start1 = content1.find('{')
        end1 = content1.rfind('}') + 1

        start2 = content2.find('{')
        end2 = content2.rfind('}') + 1

        start3 = content3.find('{')
        end3 = content3.rfind('}') + 1

        # Extract the JSON part
        json_part1 = content1[start1:end1]
        json_part2 = content2[start2:end2]
        json_part3 = content3[start3:end3]

        json_part1 = json_part1[:-3]
        json_part2 = json_part2[2:-2]
        json_part3 = json_part3[2:]


        final = json_part1 + '},\n' + json_part2 + '},\n' + json_part3

        try:
            final = json.loads(final)
            data_list.append(final)
        except json.JSONDecodeError as e:
            # Handle the JSON decode error
            print("Error decoding JSON:", e)

        if not (json_part1 and json_part2 and json_part3):
            st.error("Les images fournies ne sont pas visibles.")

        else:

            st.text_area(f"API Response (Pages {page_index + 1} and {page_index + 2}) - Part 1",
                         final)
            #st.text_area(f"API Response (Pages {page_index + 1} and {page_index + 2}) - Part 2",
            #             api_response4.messsage.content)



        j += 1

        if j >= 4:
            break



        # Display the response from the API
        #st.text_area(f"API Response (Pages {page_index + 1} and {page_index + 2}) - Part 0",
        #             content1)
        #st.text_area(f"API Response (Pages {page_index + 1} and {page_index + 2}) - Part 1",
        #             json_part1)
        #st.text_area(f"API Response (Pages {page_index + 1} and {page_index + 2}) - Part 2",
        #             content2)
        #st.text_area(f"API Response (Pages {page_index + 1} and {page_index + 2}) - Part 3",
        #             api_response4.message.content)

#data = [json.loads(json_str) for json_str in data_list]




generate_report(data_list, "template.docx", "report.docx")

