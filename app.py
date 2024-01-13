from PIL import Image
from PIL.ExifTags import TAGS
import numpy as np

import streamlit as st
import io
import uuid
import os
import plotly.express as px
from p2profile import p2pro_image


st.set_page_config('P2Pro thermal image viewer',initial_sidebar_state="collapsed",page_icon='🌡')
session = st.session_state

if 'uid' not in session:
    session.uid = str(uuid.uuid4())


with st.sidebar:
    st.markdown('### extract the raw thermal data from an Infiray P2Pro camera')
    colorscales = px.colors.named_colorscales()
    st.selectbox('color map',colorscales,key='colorscale',index=19) 
    rotation = st.selectbox('rotate image',(0,90,180,270))    
    print(rotation)

upload = st.file_uploader('upload P2pro thermal image jpg file',('jpg','jpeg'))
if upload :    
    im = p2pro_image(io.BytesIO(upload.getbuffer()))
    if rotation > 0 :
        im = np.rot90(im)  
    if rotation > 90 :
        im = np.rot90(im)  
    if rotation > 180 :
        im = np.rot90(im)          

    # convert to csv string
    x = np.savetxt(session.uid, im, delimiter=',')
    with open(session.uid) as f:
        csv = f.read()
    os.remove(session.uid)
    st.download_button('Download CSV', csv,file_name=upload.name.replace('.jpg','.csv'))

    fig = px.imshow(im,aspect='equal',color_continuous_scale=session.colorscale) #,labels = labels)  
    fig.update_layout(height=800)
    st.plotly_chart(fig,use_container_width=True)

    
        
