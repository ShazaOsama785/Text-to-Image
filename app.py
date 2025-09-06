import streamlit as st
import replicate
import os
import requests
from PIL import Image
from io import BytesIO

# Safely get the token from Streamlit secrets
replicate_token = st.secrets.get("REPLICATE_API_TOKEN")

if not replicate_token:
    st.error("Replicate API token is missing. Please set REPLICATE_API_TOKEN in your Streamlit secrets.")
    st.stop()

# Set up the Replicate client
replicate.Client(api_token=replicate_token)

# Streamlit config
st.set_page_config(page_title="Anan Generator", layout="centered")
st.title("Anan Generator")


# UI input
prompt = st.text_input("Enter your prompt")

if st.button("Generate") and prompt:
    with st.spinner("Generating..."):
        try:
            output = replicate.run(
                "stability-ai/stable-diffusion:ac732df83cea7fff18b8472768c88ad041fa750ff7682a21affe81863cbe77e4",
                input={"prompt": prompt}
            )

            # Get the image URL from the output
            image_url = output[0]
            response = requests.get(image_url)

            if response.status_code == 200:
                image = Image.open(BytesIO(response.content))
                st.image(image, caption="Here’s your image!")

                # Convert image to byte stream for download
                img_byte_arr = BytesIO()
                image.save(img_byte_arr, format="PNG")
                img_byte_arr.seek(0)

                # Add download button
                st.download_button(
                    label="Download Image",
                    data=img_byte_arr,
                    file_name="generated_image.png",
                    mime="image/png"
                )
            else:
                st.error("Failed to fetch the image.")

        except replicate.exceptions.ReplicateError as e:
            st.error(f"Replicate error: {e}")
