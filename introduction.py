import streamlit as st
import sqlite3
import pandas as pd
import numpy as np

import db_methods as db
import db_sync

import methods as m


col1, col2 = st.columns((2,1))
with col1:
    st.header(":cookie: An Introduction to Web Cookies")
    st.write("by: Jessica Chen, Nina Howley, Crystal Zhao, and Dianna Gonzalez")
    st.write("Advised by: Eni Mustafaraj")
with col2:
    st.image("bettercookie.jpg", width = 500)
st.subheader("A Brief Overview of Cookies")
#col1, col2 = st.columns((2,1))
#with col1:
st.write(" A cookie is a **text string** that is placed on a client **browser** when it accesses a given server. " \
"The cookie is transmitted back to that server in the header of subsequent requests.")

st.write("A cookie is a formatted string consisting of semi-colon separated key-value pairs.")
st.write("\t\tFor example: *Name=Value; Host=example.com; Path=/account; Expires=Tue, 1 Dec 2018 10:12:05 UTC; Secure;*")
st.caption("Source: https://doi.org/10.1145/2872427.2882991")
#with col2:
    


col1, col2 = st.columns((2,1))
with col1:
    st.subheader("What are cookies used for?")
    st.write("Cookies are useful for websites to **save previously entered information** like login credentials and webpage settings (ie light or dark mode)" \
    ", so users don't have to continously re-enter information. ")
    st.write ("While cookies are used to remember information, they don't actually store personal information. Instead, they store information in a **unique session ID**" \
    " that gets sent from the server to the browser.")
with col2:
    st.image("cookie-basic-example.png", width = 800)
    st.caption("Source: Mozilla [https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Cookies]")

st.subheader("Are cookies dangerous?")
#col1, col2 = st.columns((2,1))
#with col1:
st.write("**Not all cookies are dangerous!** In fact, many are still necessary for a smooth website expereince.")
st.write("However, cookies can be harmful when they turn into **tracking cookies**. " \
"These cookies can create a detailed profile of a user's browsing history, interests, habits, and personal information (more on this in the Third-Party Cookies tab!). " \
"Many browsers—such as Firefox, Brave, and Safari—have completely banned third-party cookies. " \
"Google has yet to ban them, but has enforced an opt-in system.")
#with col2:
  #  st.image("dangerous-cookie.jpg")

st.subheader("Go to the Follow Along tab to learn more! ")
st.write("In this interactive website, you will learn about...")
st.markdown("- First Party Cookies and Cookie Security")
st.markdown("- Third Party Cookies and Privacy")
st.markdown("- Persistent Cookies")
st.markdown("- Cookies over time")

conn = sqlite3.connect("Example_Cookies.db")
cur = conn.cursor()

cookies = pd.read_sql_query(f"SELECT * FROM cookies", conn)

st.subheader("Chrome's Cookie Database")

col1, col2 = st.columns((2,1))
with col1:
    m.display_raw_cookies(cookies)

columns = ['creation_utc', 'host_key', 'top_frame_site_key', 'name', 
           'value', 'encrypted_value', 'path', 'expires_utc',
           'is_secure', 'is_httponly', 'last_access_utc', 'has_expires',
           'is_persistent', 'priority', 'samesite', 'source_scheme',
           'source_port', 'last_update_utc', 'source_type', 'has_cross_site_ancestor']

selection = col2.selectbox(options=columns,label="Choose a column to learn more about.")

if selection:
    col2.write(m.display_description(selection))
