import numpy as np
import streamlit as st
import io
import plotly.express as px
from p2profile import p2pro_image
from np_to_stream import np_to_csv_stream

st.set_page_config('P2Pro thermal image viewer',initial_sidebar_state="expanded",page_icon='🌡')
session = st.session_state

with st.sidebar:
    st.markdown('### extract the raw thermal data from an Infiray P2Pro camera')
    colorscales = px.colors.named_colorscales()
    st.selectbox('units',('Celsius','Fahrenheit'),index=0,key='units')
    session.fahrenheit = False
    if session.units == 'Fahrenheit' : session.fahrenheit = True
    st.selectbox('color map',colorscales,key='colorscale',index=19) 
    rotation = st.selectbox('rotate image',(0,90,180,270))    
    orgimg = st.checkbox('show video image?',value=True)
    height = st.number_input('image height',value=600,step=100)
    st.checkbox('autoscale',value=True,key='autoscale')
    st.number_input('min temp',value=0,key='tmin')
    st.number_input('max temp',value=60,key='tmax')


upload = st.file_uploader('upload P2pro thermal image jpg file',('jpg','jpeg'))
if upload :    
    im,im2 = p2pro_image(io.BytesIO(upload.getbuffer()),fahrenheit=session.fahrenheit)
    if rotation == 90 :
        im = np.rot90(im)  
    if rotation == 180 :
        im = np.rot90(im,2)  
    if rotation == 270 :
        im = np.rot90(im,3)          

    csv = np_to_csv_stream(im) 
    st.download_button('Download CSV', csv,file_name=upload.name.replace('.jpg','.csv'))
    if session.fahrenheit :
        title = 'Temperature in Fahrenheit from raw data'
    else :
        title = 'Temperature in Celsius from raw data'
    if session.autoscale :
        fig = px.imshow(im,aspect='equal',color_continuous_scale=session.colorscale,title=title) 
    else :
        fig = px.imshow(im,aspect='equal',color_continuous_scale=session.colorscale,title=title,zmin=session.tmin,zmax=session.tmax)  
    fig.update_layout(height=height)
    st.plotly_chart(fig,use_container_width=True)

    if orgimg :
        fig = px.imshow(im2,aspect='equal',color_continuous_scale=session.colorscale,title='camera video image')
        fig.update_layout(height=height)
        st.plotly_chart(fig,use_container_width=True)
        
        
