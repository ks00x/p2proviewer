import streamlit as st
from zipfile import ZipFile, ZIP_DEFLATED
from io import BytesIO
import uuid
import numpy as np
import os
from p2profile import p2pro_image
from np_to_stream import np_to_csv_stream


st.set_page_config('P2Pro thermal image to csv coverter',initial_sidebar_state="expanded",page_icon='💾')
session = st.session_state
if 'uid' not in session:
    session.uid = str(uuid.uuid4())

st.write('''
         ## convert multiple uploaded P2Pro jpeg files into csv files with thermal data and download all as a zip file
         - press F5 to clear the whole list!
         '''
         )

up = st.file_uploader('multi upload test',accept_multiple_files=True,)
if up is not None:
    if len(up) > 0 : # up is a list of files with this option
        stream = BytesIO()     
        errlist = []
        with ZipFile(stream, mode="w",compression=ZIP_DEFLATED, compresslevel=9) as archive:
            for f in up :
                try:
                    data,_ = p2pro_image(f)
                    csv = np_to_csv_stream(data)
                    archive.writestr(f.name.replace('.jpg','.csv'),csv)                                    
                except:
                    errlist.append(f.name)
        if len(errlist)  > 0 :
            st.write('files with errors:')                 
            st.write(errlist)
                
        st.download_button('download zip',data=stream,file_name='download.zip')           