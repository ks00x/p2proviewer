import numpy as np
import streamlit as st
import io
import plotly.express as px
from p2profile import p2pro_image
from np_to_stream import np_to_csv_stream

st.set_page_config('P2Pro thermal image viewer',initial_sidebar_state="expanded",page_icon='🌡')
session = st.session_state
if 'units' not in session : # init
    session.upload = None
    session.units = 'Celsius'
    session.colorscale = 'icefire'
    session.rotation = 0
    session.autoscale = True
    session.tmax = 50
    session.tmin = 20
    session.orgimg = True
    session.height = 600
else :
    for k in session.keys():
        session[k] = session[k]

with st.sidebar:
    st.markdown('### extract the raw thermal data from an Infiray P2Pro camera')
    colorscales = px.colors.named_colorscales()
    st.selectbox('units',('Celsius','Fahrenheit'),key='units')
    session.fahrenheit = False
    if session.units == 'Fahrenheit' : session.fahrenheit = True
    st.selectbox('color map',colorscales,key='colorscale') 
    st.selectbox('rotate image',(0,90,180,270),key='rotation')    
    st.checkbox('show camera rendered image?',key='orgimg')
    st.number_input('image height',step=100,key='height')
    st.checkbox('autoscale',key='autoscale')
    st.number_input('min temp',key='tmin',step=5.)
    st.number_input('max temp',key='tmax',step=5.)


upload = st.file_uploader('upload P2pro thermal image jpg file',('jpg','jpeg'))
if upload or session.upload is not None :    
    if upload :
        session.upload = upload
    try:
        im,im2 = p2pro_image(io.BytesIO(session.upload.getbuffer()),fahrenheit=session.fahrenheit)

        if session.rotation == 90 :
            im = np.rot90(im)  
        if session.rotation == 180 :
            im = np.rot90(im,2)  
        if session.rotation == 270 :
            im = np.rot90(im,3)          

        csv = np_to_csv_stream(im) 

        session.upload.name.replace('.jpg','.csv')
        if session.fahrenheit :
            fname = session.upload.name.replace('.jpg','_F.csv')
            title = 'Temperature in Fahrenheit from raw data'
        else :
            fname = session.upload.name.replace('.jpg','_C.csv')
            title = 'Temperature in Celsius from raw data'
        
        st.download_button('Download CSV', csv,file_name=fname)
        
        if session.autoscale :
            fig = px.imshow(im,aspect='equal',color_continuous_scale=session.colorscale,title=title) 
        else :
            fig = px.imshow(im,aspect='equal',color_continuous_scale=session.colorscale,title=title,zmin=session.tmin,zmax=session.tmax)  
        fig.update_layout(height=session.height)
        st.plotly_chart(fig,use_container_width=True)
        st.write(f"min = {im.min():1.2f}, max = {im.max():1.2f}, mean = {im.mean():1.2f}")

        if session.orgimg :
            fig = px.imshow(im2,aspect='equal',color_continuous_scale=session.colorscale,title='camera video image')
            fig.update_layout(height=session.height)
            st.plotly_chart(fig,use_container_width=True)
            
    except IndexError:
        st.error("⛔ Not a p2pro jpg file. Extracting the raw data failed!")
    
            