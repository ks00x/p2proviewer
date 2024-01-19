import streamlit as st
about = '''
### viewer and raw converter for jpg files created by the Infiray P2Pro infrared camera using the original software
Klaus Schwarzburg 2024

💡 a quick tip: You can open the downloaded csv image file in [ImageJ](https://imagej.net/software/imagej/) (`file->import text image`) and do more interesting image processing things directly with the temperature data. Linescan profiles for example.

💡 Use the 'blackbody' profile to indicate highlight cliping when using a manual temperature scale


'''
session = st.session_state
for k in session.keys():
    session[k] = session[k]

st.write(about)