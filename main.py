import streamlit as st

from PIL import Image
import cv2
import numpy as np
from collections import Counter


st.set_page_config(page_title="Product description", page_icon=":robot:", layout="centered")
st.header("Product description")

st.image(image='logo.jpeg', width=700)

st.markdown("## Please upload your product image")

upload = st.file_uploader("Upload your image")

# col1, col2 = st.columns(2)

# with col1:
#     option_model = st.selectbox(
#         'Which model do you wish to use?',
#         ('pretrain_flant5xl', 'pretrain_flant5xl_vitL', 'pretrain_flant5xxl', 'caption_coco_flant5xl'))
    
# with col2:
#     option_prompt = st.selectbox(
#         'Would you like a product description, a product classification, or a custom question?',
#         ('Description', 'Classification', 'Custom'))

    
# if option_prompt == 'Custom':
#     def get_text():
#         """
#         :output: function to receive prompt from user
#         """
#         input_text = st.text_area(label="Question", label_visibility='collapsed', placeholder="What is your question about the image?...", key="text_input")
#         return input_text

#     if len(text_input.split(" ")) > 25:
#         st.write("Please enter a shorter question. The maximum length is 25 words.")
#         st.stop()

#     prompt = get_text()
    
# if option_prompt == 'Description':
#     prompt = 'Can you describe this image?'

# if option_prompt == 'Classification':
#     prompt = 'Is this product a wardrobe?'
    

# if upload and prompt and option_model:
#     image = Image.open(upload).convert('RGB')
    
#     st.image(image, width=700)
#     st.markdown('## Model loading')
#     model, vis_processors, _ = load_model_and_preprocess(name="blip2_t5", model_type=option_model, is_eval=True, device='cpu')
#     st.markdown('## Model loaded')

#     image = vis_processors["eval"](raw_image).unsqueeze(0).to('cpu')
    
#     # model.generate({"image": image, "prompt": "Can you give a detailed description of this image?"})
#     response = model.generate({"image": image, "prompt": "Is this a picture of a wardrobe?"})
    
#     st.markdown("### Model response: + /n")
#     st.markdown(response)
    
if upload:
    image = Image.open(upload).convert('RGB')
    st.image(image, width=700)

    image = cv2.imread(upload)

    # Reshape the 3D image array into a 2D array where each row represents a pixel (R, G, B values)
    pixels = image.reshape(-1, 3)
    
    pixel_counts = Counter(map(tuple, pixels))
    
    most_common_pixel, count = pixel_counts.most_common(2)[1]

    st.markdown('## Most common colour is:')
    st.write(str(most_common_pixel))
    
