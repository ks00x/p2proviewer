from PIL import Image
from PIL.ExifTags import TAGS
import numpy as np
import streamlit as st
import io
import uuid
import os
import plotly.express as px

st.set_page_config('P2Pro thermal image viewer',initial_sidebar_state="collapsed",page_icon='🌡')
session = st.session_state

if 'uid' not in session:
    session.uid = str(uuid.uuid4())
    session.rescale = False
    session.scale_clear = False   
    
with st.sidebar:
    colorscales = px.colors.named_colorscales()
    st.selectbox('color map',colorscales,key='colorscale',index=19)
    
    


upload = st.file_uploader('upload P2pro thermal image jpg file',('jpg','jpeg'))
if upload :
    
    im = Image.open(io.BytesIO(upload.getbuffer()))
    exif = im.applist[0][1]
    
    # concatenate APP3 chunks of data. It is 6Bytes of data per pixel... 
    # played around with the code given here: https://exiftool.org/forum/index.php?topic=11401.msg61816#msg61816
    buf = im.applist[2][1]    
    for i in range(3, 7):
        buf += im.applist[i][1]
    # create image from bytes
    # https://pillow.readthedocs.io/en/stable/handbook/concepts.html#concept-modes
    # this setting at least gives an image that looks like the original thermal image. Details unclear..
    #img = Image.frombytes('I;16B', (256, 192), a[0xC000*0:])
    img = Image.frombytes('I;16B', (256, 192),buf)
    img = img.transpose(Image.ROTATE_270)
    print('hi')
        

    # what scaling to apply??? There seems to be no scaling factors in the exif that change with the min max range of the thermal image -> Absolute scaling
    temps = np.array(img,dtype=np.float32)     

    with st.form('set temperature range in C'):
        c1,c2,c3,c4 = st.columns(4)
        c1.number_input('Tmin in C',value=24.,key='tmin')
        c2.number_input('Tmax in C',value=30.,key='tmax')
        c4.checkbox('clear scaling',key='scale_clear')
        def callb_scale():            
            temps = np.array(img,dtype=np.float32)                 
            if not session.scale_clear :                
                session.z0 = temps.min()
                session.zf = (session.tmax - session.tmin) / (temps.max() - temps.min())
                session.zm = session.tmin
                session.rescale = True 
            else :
                session.rescale = False
            session.scale_clear=False
            
        scale = c3.form_submit_button('scale data',on_click=callb_scale)        
        
    if session.rescale :
        temps = (temps - session.z0) * session.zf + session.zm
            

    # convert to csv string
    x = np.savetxt(session.uid, temps, delimiter=',')
    with open(session.uid) as f:
        csv = f.read()
    os.remove(session.uid)
    # tif stream
    tif = io.BytesIO()
    img.save(tif,format="tiff")
    
    
    c1,c2,_,_,_ = st.columns(5)
    c1.download_button('Download CSV', csv,file_name=upload.name.replace('.jpg','.csv'))
    c2.download_button('Download TIF', tif,file_name=upload.name.replace('.jpg','.tif'))    
        
    fig = px.imshow(temps,aspect='equal',color_continuous_scale=session.colorscale) #,labels = labels)  
    fig.update_layout(height=800)
    st.plotly_chart(fig,use_container_width=True)

    
    
        
    


    


