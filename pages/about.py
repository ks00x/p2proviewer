import streamlit as st
import plotly.express as px

about = '''
### Raw converter/viewer for jpg files created by the Infiray P2Pro infrared camera using the original software
[see the source code on github ks00x/p2proviewer](https://github.com/ks00x/p2proviewer)

Klaus Schwarzburg 2024

Extracts the raw temperature data (192x256 pixels) out of the jpg files created by the original P2Pro Android app. 
The raw data is contained in the jpg file exif data block. The Android app stores the jpg files in the 
dcim/infiray subfolder. 

💡 the image viewer has several options to zoom and save bitmap images. Check the icon bar on the top!

💡 The mouse cursor annotation gives you the temperature at that position. Together with zooming you can analyze
specific areas in high detail!

💡 a quick tip: You can open the downloaded csv image file in [ImageJ](https://imagej.net/software/imagej/) (`file->import text image`) and do more interesting image processing things directly with the temperature data. Linescan profiles for example.

💡 Use the 'blackbody' profile to indicate highlight cliping when using a manual temperature scale

💡 Check out [this repo](https://github.com/ks00x/p2pro-live) for a Python/Streamlit app to use the P2Pro on the Windows desktop PC

💥Always keep an unmodfied version of your camera files. If you modify your P2Pro jpeg files (resize, xml,iptc, etc metadata), 
the raw data import is likely to fail!


'''
session = st.session_state
for k in session.keys():
    session[k] = session[k]

st.write(about)

st.write('### available colormaps')
fig = px.colors.sequential.swatches_continuous()
st.plotly_chart(fig)