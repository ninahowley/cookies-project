import streamlit as st
import os 
import pandas as pd

import methods as m

#cd cookies_streamlit
#python -m streamlit run cookies_streamlit.py

st.set_page_config(
        page_title="Cookies Streamlit",
        layout="centered")

st.header("Cookies Streamlit (WIP)")

user = os.getlogin()
st.write("Hello, ", user)

cookies = ""     
st.write("Which operating system are you using?")
c1, c2 = st.columns((1.5,3))
with c1:
        col1, col2 = st.columns((2), gap="small")
        windows = col1.button("Windows", key="windows")
        mac = col2.button("Mac", key="mac")

if windows:
      cookies = m.display_windows_filepath(user)

if mac:
      cookies = m.display_mac_filepath(user)

st.write(m.display_cookies())
