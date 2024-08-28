import streamlit as st
from PIL import Image
import numpy as np
from matplotlib import pyplot as plt
import cv2


# define a function to analyse grayscale values of image
# the function takes an image as input and returns a plot with the image and the histogram
def get_image_info(img_ravel):    
    # first, define break points to get 10 equal sized bins
    breaks = np.linspace(0, 255, 11)
    # the min value of the 4th bin (index 3) is the lower threshold for midtones 
    # convert to integer to use it as index
    mid_lower = breaks[3].min().astype(int)
    # righthand side of the 7th bin (index 6) is the upper threshold for midtones
    mid_upper = breaks[6].max().astype(int)
   
    plt.subplot(1,2,2)
    hist,bin = np.histogram(img_ravel,256,[0,255])
    plt.xlim([0,255])
    plt.plot(hist)
    plt.title('histogram')
    # add vertical threshold line at midtones > 100 and < 150
    plt.axvline(x= mid_lower, color='r', linestyle='--')
    plt.axvline(x=mid_upper, color='r', linestyle='--')
    # fill area under the curve between 100 and 150
    plt.fill_between(bin[mid_lower:mid_upper], hist[mid_lower:mid_upper], color='grey', alpha=0.5)
    # fill area under the curve between 0 and 100
    plt.fill_between(bin[:mid_lower], hist[:mid_lower], color='black', alpha=0.7)
    # calculate the area under the curve between 100 and 150 with the relative area size
    area_midtone = np.sum(hist[mid_lower:mid_upper]) / np.sum(hist)
    area_lights = np.sum(hist[:mid_lower]) / np.sum(hist)
    area_darks = np.sum(hist[mid_upper:]) / np.sum(hist)
    # add text to the plot in percentage
    # calculate lower quantile of the y-axis to place the text in the middle of the plot
    ymid = np.quantile(hist, 0.5)
    plt.text(mid_lower+5, ymid, str(round(area_midtone*100, 2)) + '%', color='red', fontdict={'size': 8})
    plt.text(10, ymid, str(round(area_lights*100, 2)) + '%', color='red', fontdict={'size': 8})
    plt.text(mid_upper+5, ymid, str(round(area_darks*100, 2)) + '%', color='red', fontdict={'size': 8})
    fig = plt# return the plot   
    return  fig






st.title("Image Uploader")

uploaded_file = st.file_uploader("Choose an image...", type="jpg")

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image")
    # get ravel of image
    image_ravel = np.array(image).ravel()
   # call the function to plot the image and histogram
    my_plot = get_image_info(image_ravel)
    # display the plot in the streamlit app also provide a figure argument to display the plot
    st.pyplot(my_plot, clear_figure=True)