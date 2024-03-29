import streamlit as st
from zipfile import ZipFile, ZIP_DEFLATED
from io import BytesIO
import numpy as np
from p2profile import p2pro_image
import plotly.express as px
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

st.set_page_config('P2Pro thermal image png converter',initial_sidebar_state="expanded",page_icon='💾')
session = st.session_state
for k in session.keys():
    session[k] = session[k]
    
st.write('''
         ## regenerate multiple uploaded P2Pro jpeg files using the settings from the main page and download all as a zip file
         - generates png files with original sensor pixel size (192 x 256) without colorbar
         - uses the  scaling, rotation, units and colormap settings from the main page
         - useful to display a bunch of thermal images with the same temperature range (manual scaling)
         - press F5 to clear the whole list!
         '''
         )

# convert the plotly colormap to matplotlib (it turns out to be difficult to save the plotly plots programatically)
# https://stackoverflow.com/questions/77886066/plotly-colormaps-in-matplotlib
SAMPLES = 256
plotlymap = px.colors.sample_colorscale(session.colorscale, SAMPLES)
rgb = [px.colors.unconvert_from_RGB_255(px.colors.unlabel_rgb(c)) for c in plotlymap]
cmap = mcolors.ListedColormap(rgb, name='temp', N=SAMPLES)

up = st.file_uploader('multi upload P2Pro jpg files',accept_multiple_files=True,)
if up is not None:
    if len(up) > 0 : # up is a list of files with this option
        stream = BytesIO()     
        png = BytesIO()     
        errlist = []
        with ZipFile(stream, mode="w",compression=ZIP_DEFLATED, compresslevel=9) as archive:
            for f in up :
                try:
                    im,_ = p2pro_image(f,session.fahrenheit)
                    if session.rotation == 90 :
                        im = np.rot90(im)  
                    if session.rotation == 180 :
                        im = np.rot90(im,2)  
                    if session.rotation == 270 :
                        im = np.rot90(im,3)   
                    png.seek(0)                    
                    if session.autoscale :
                        plt.imsave(png,im,format='png', cmap=cmap)                         
                    else :
                        plt.imsave(png,im,format='png',vmin=session.tmin,vmax=session.tmax, cmap=cmap)  
                    png.seek(0)                                                                           
                    if session.fahrenheit :
                        fname = f.name.replace('.jpg','_F.png')                        
                    else :
                        fname = f.name.replace('.jpg','_C.png')                        
                    archive.writestr(fname,png.read())    
                    png.flush()
                except Exception as e:
                    print(e)
                    errlist.append(f.name)
        if len(errlist)  > 0 :
            st.write('files with errors:')                 
            st.write(errlist)        
        st.download_button('download zip',data=stream,file_name='download.zip')           