import streamlit as st
import os 
import pandas as pd

import methods as m

st.header("Cookies Streamlit (WIP)")

# user = os.getlogin()
# st.write("Hello, ", user)

# Creating a form submission to count the number of cookies on a single website. 
# We can use it for our wellesley college website demo.
st.header("How many cookies does the Wellesley College website have?")

cookie_count = st.form("cookies_count")

with cookie_count:
       st.write("Paste https://www.wellesley.edu/ below to find out!")
       website = cookie_count.text_input('Enter a website:') 
       st.form_submit_button("Click for number of cookies")



cookies = None
st.header("You try!")
st.write("Which operating system are you using?")
c1, c2 = st.columns((1.5,3))
with c1:
        col1, col2 = st.columns((2), gap="small")
        windows = col1.button("Windows", key="windows")
        mac = col2.button("Mac", key="mac")

if windows:
      cookies = m.display_windows_filepath()

if mac:
      cookies = m.display_mac_filepath()

cookies = m.upload_cookies()

m.display_raw_cookies(cookies)

m.sort_cookie_domains(cookies)

m.categorize_cookies(cookies)