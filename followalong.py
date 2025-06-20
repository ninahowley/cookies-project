import streamlit as st
import os 
import pandas as pd

import methods as m
import visualization_methods as vm

st.header("Cookies Streamlit (WIP)")

# user = os.getlogin()
# st.write("Hello, ", user)

# Creating a form submission to count the number of cookies on a single website. 
# We can use it for our wellesley college website demo.
# unfortunately only fetches first party cookies...
st.header("How many cookies does the Wellesley College website have?")

cookie_count = st.form("cookies_count")

with cookie_count:
       st.write("Paste https://www.wellesley.edu/ below to find out!")
       website = cookie_count.text_input('Enter a website:') 
       cookies_count = m.get_cookies(website)


cookies = None
st.header("You try!")
st.write("Click the buttons below for instructions on how to upload your cookies, depending on your operating system.")
c1, c2 = st.columns((1.5,3))
with c1:
        col1, col2 = st.columns((2), gap="small")
        windows = col1.button("Windows", key="windows")
        mac = col2.button("Mac", key="mac")

if windows:
      cookies = m.display_windows_filepath()

if mac:
      cookies = m.display_mac_filepath()

#upload cookies
cookies = m.upload_cookies()

#Button to show raw cookies db
if "show_db" not in st.session_state:
    st.session_state.show_db = False

def toggle_db():
    st.session_state.show_db = not st.session_state.show_db

button_label = "Collapse database" if st.session_state.show_db else "Click to see cookies database"

# Use the button to toggle
st.button(
    button_label,
    on_click=toggle_db
)

if st.session_state.show_db:
    m.display_raw_cookies(cookies)

st.write("After you upload, toggle through these topics to visualize your own cookies and learn about these concepts!")

#creating selectbox for visualizations
visualization = st.selectbox(
    "Click here to learn about each topic",
    ["Cookie Security", "Third Party Cookies", "Persistent Cookies", "Size of Cookies"],
    index=0,  # or None if you want no default selection
)
st.write("You selected:", visualization)

#creating some initial visualizations
m.sort_cookie_domains(cookies)

m.categorize_cookies(cookies)

vm.persistent_cookies(cookies)

vm.last_accessed(cookies)