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
    index=None,
    placeholder="Select topic to explore..."
)

if visualization == "Cookie Security":
    st.header("Cookie Security")
    st.write("Let's learn about cookie security! Below is a pie chart showing the proportions of your secure and insecure cookies.")
    #creating cookie security pie charts
    col1, col2 = st.columns((1,1))
    with col1:
        m.pie_chart(cookies)
    
    with col2:
        st.write("Toggle to view domains that have secure vs not secure cookies!")
        col1, col2 = st.columns((1,1))
        with col1:
            on_secure = col1.toggle("Secure")
            if on_secure:
                m.on_secure(cookies)
        with col2:
            on_insecure = col2.toggle("Not Secure")
            if on_insecure:
                m.on_insecure(cookies)
        
    st.subheader("Secure vs. insecure cookies")
    st.write("Secure cookies are designed to only be transmitted over HTTPS, which means they are encrypted during when sent from the domain to server and less vulnerable to interception. " \
    "Web browsers (or user agents) will only include the cookie in an HTTPS request, only if it is transmitted over a secure channel (likely HTTPS). HTTPS is secure because it uses encryption to " \
    "protect data in transit between the user's browser to server." \
    "\n\nHowever, insecure cookies can be sent over HTTP, which transmits data in plain text, potentially exposing this information to attackers. " \
    "\n\n In the database, to see if cookies are secure or insecure, look at the *is_secure* attribute. *is_secure* = 1 means it's secure and *is_secure* = 0 means it's insecure. ")
    st.subheader("")

if visualization == 'Persistent Cookies':
    st.header("Persistent Cookies")
    st.write("Add text")
    #creating cookie security pie charts
    col1, col2 = st.columns((1,1))
    with col1:
        vm.persistent_cookies(cookies)
    with col2:
         st.write("Add information")

#creating some initial visualizations
m.sort_cookie_domains(cookies)

# m.categorize_cookies(cookies)

vm.last_accessed(cookies)

m.cookie_type(cookies)