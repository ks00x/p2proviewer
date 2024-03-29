import streamlit as st
from zipfile import ZipFile, ZIP_DEFLATED
from io import BytesIO
import numpy as np
from p2profile import p2pro_image
from np_to_stream import np_to_csv_stream

st.set_page_config('P2Pro thermal image to csv coverter',initial_sidebar_state="expanded",page_icon='💾')
session = st.session_state
for k in session.keys():
    session[k] = session[k]
    
st.write('''
         ## convert multiple uploaded P2Pro jpeg files into csv text files with thermal data and download all as a zip file
         - press F5 to clear the whole list!
         '''
         )

up = st.file_uploader('multi upload P2Pro jpg files',accept_multiple_files=True,)
if up is not None:
    if len(up) > 0 : # up is a list of files with this option
        stream = BytesIO()     
        errlist = []
        with ZipFile(stream, mode="w",compression=ZIP_DEFLATED, compresslevel=9) as archive:
            for f in up :
                try:
                    data,_ = p2pro_image(f,session.fahrenheit)
                    csv = np_to_csv_stream(data)
                    if session.fahrenheit :
                        fname = f.name.replace('.jpg','_F.csv')                        
                    else :
                        fname = f.name.replace('.jpg','_C.csv')        
                    archive.writestr(fname,csv)                                    
                except:
                    errlist.append(f.name)
        if len(errlist)  > 0 :
            st.write('files with errors:')                 
            st.write(errlist)
                
        st.download_button('download zip',data=stream,file_name='download.zip')           