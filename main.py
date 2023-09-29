import cv2

import plotly.express as px
import plotly.figure_factory as ff

import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

from PIL import Image
from mpl_toolkits.mplot3d import Axes3D


csv = pd.read_csv('colors.csv')

def get_color_name(Red, Green, Blue):
        minimum = 10000
        for i in range(len(csv)):
            d = abs(Red - int(csv.loc[i, "Red"])) + abs(Green - int(csv.loc[i, "Green"])) + abs(Blue - int(csv.loc[i, "Blue"]))
            if d <= minimum:
                minimum = d
                cname = csv.loc[i, "Color"]
        return cname
    
st.set_page_config(page_title="Product description", page_icon=":robot:", layout="centered")
st.header("Product description")

st.image(image='logo.jpeg', width=700)

st.markdown("## Please upload your product image")

upload = st.file_uploader("Upload your image")
    
if upload:
    image = Image.open(upload).convert('RGB')
    st.image(image, width=700)   

    # Load the image
    img = Image.open(upload)

    # Convert the image to RGB mode if it's not already
    if img.mode != 'RGB':
        img = img.convert('RGB')

    # Define a threshold for the white background (adjust as needed)
    background_threshold = 253

    # Initialize a dictionary to store unique RGB values of the object
    object_colors = {}

    # Get the image dimensions
    width, height = img.size

    # Iterate through each pixel in the image
    for x in range(width):
        for y in range(height):
            # Get the RGB values of the pixel
            r, g, b = img.getpixel((x, y))

            # Check if the pixel is not part of the white background
            if r < background_threshold and g < background_threshold and b < background_threshold:
                # Store the RGB values in the dictionary
                object_colors[(r, g, b)] = object_colors.get((r, g, b), 0) + 1
                
    colours = []
    counts = []

    for color, count in object_colors.items():
        colours.append(get_color_name(color[0], color[1], color[2]))
        counts.append(count)

    df = pd.DataFrame()

    df['colour'] = colours
    df['value_count'] = counts
    
    D = df.groupby('colour').sum()
    D['ratio'] = D['value_count'] / D['value_count'].sum()*100
    D['ratio'] = D['ratio'].round()
    
    D = D.sort_values('value_count', ascending=False)
    
    common_colour = D.index[0]
    ratio = str(D['ratio'].iloc[0])
    

    st.markdown('## Most common colour is:')
    st.write(common_colour)
    
    st.markdown('## Colour occurs in this percentage of pixels:')
    st.write(ratio)

    fig = plt.figure(figsize=(12, 10))

    ax = fig.add_subplot(111, projection='3d')

# Scatter plot
    scatter = ax.scatter(csv['Red'], csv['Green'], csv['Blue'], c=csv['Color'], s=100, marker='o')

# Add color labels next to each point
    for i, txt in enumerate(csv['Color']):
        ax.text(csv['Red'][i], csv['Green'][i], csv['Blue'][i], txt, size=12, color='black')

# Set axis labels
    ax.set_xlabel('Red')
    ax.set_ylabel('Green')
    ax.set_zlabel('Blue')

# Customize the legend
    legend_labels = csv['Color'].unique()
    handles = [plt.Line2D([0], [0], marker='o', color='w', label=label, markersize=10, markerfacecolor=color) for label, color in zip(legend_labels, scatter.get_facecolor())]
# ax.legend(handles=handles, title='Color')
    st.markdown('## Colour space:')
    st.pyplot(fig)

    figure = px.scatter_3d(csv, x='Red', y='Green', z='Blue', color='Color', text='Color', size_max=10)

# Customize the layout
    figure.update_layout(
        scene=dict(
            xaxis_title='Red',
            yaxis_title='Green',
            zaxis_title='Blue',
        ),
        legend_title='Color',
    )
    st.markdown('## Colour space interactive:')
    st.plotly_chart(figure, use_container_width=True)
    
