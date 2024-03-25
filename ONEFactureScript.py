import streamlit as st
import requests


# Function to call GPT-4 API with the uploaded image
def analyze_image(image_file):
    url = "https://open-ai21.p.rapidapi.com/ocr"

    files = {"file": image_file}

    headers = {
        "X-RapidAPI-Key": "096e66c0a8mshb1fddf4fb473344p1da386jsn971c26f729a6",
        "X-RapidAPI-Host": "open-ai21.p.rapidapi.com"
    }

    response = requests.post(url, files=files, headers=headers)

    return response.json()


# Streamlit app UI
def main():
    st.title("GPT-4 Image Analyzer")
    st.write("Upload a JPG image for analysis")

    # File uploader
    uploaded_file = st.file_uploader("Choose a JPG image", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        # Display the uploaded image
        st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)

        # Button to trigger analysis
        if st.button("Analyze"):
            with st.spinner("Analyzing..."):
                # Call GPT-4 API
                result = analyze_image(uploaded_file)

                # Display analysis results
                st.write("Analysis Results:")
                st.write(result)


if __name__ == "__main__":
    main()
