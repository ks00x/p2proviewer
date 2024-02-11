# p2proviewer
- extract the 192x256 pixel raw data out of Infiray P2Pro thermal camera jpeg images
- visualize data and read the temperature at the mouse cursor
- temperature in Celsius or Fahrenheit
- set a manual temperature range
- save temperature data as csv or png file
- many color maps available
- on the sidebar menu one can access a multi file csv/png conversion tools
- streamlit app (`pip install streamlit`) [Streamlit • A faster way to build and share data apps](https://streamlit.io/). Start the script with `streamlit run app.py`

💡 a quick tip:
You can open the downloaded csv image file in [ImageJ](https://imagej.net/software/imagej/) (`file->import text image`) and do more interesting things directly with the temperature data. Linescan profiles for example.


[live version of the app](https://p2proviewer.streamlit.app/)


![app](media/Screenshot.png)