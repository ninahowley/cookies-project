import streamlit as st
import sqlite3
import pandas as pd
import numpy as np

import db_methods as db
import db_sync

import methods as m

st.title("Introduction")

st.header("Disclaimer")
st.warning("Cookies are stored locally on your computer." \
"\n\nAny file you upload to this Streamlit will not be saved anywhere, unless you give explicit permission at the end of the follow along." \
"\n\nIf you DO give permission, your data will be anonymized and all sensitive values will be removed." \
"\n\nDuring the follow along you will be given the option to use an example cookies database if you are not comfortable uploading your own.")

st.header("What Are Cookies?")
st.write("Cookies, at the surface level, are small data files which are sent by websites and stored on your device." \
"\n\nCookies are what allow browsers to remember information about a user such as their login or browsing history." \
"\n\nThere are many types of cookies, first party, third party, secure and insecure, to name a few." \
"\n\nOn this Streamlit you will learn about the different types and how to protect your information, as well as visualize your data.")

conn = sqlite3.connect("Example_Cookies.db")
cur = conn.cursor()

cookies = pd.read_sql_query(f"SELECT * FROM cookies", conn)

st.header("Chrome's Cookie Database")
st.write("Below is an example cookie database.")

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

st.header("Confused?")
st.write("That is completely fine! The cookies database contains a large amount of columns. Each of these columns defines something unique about a cookie, and it can be difficult to understand all of them."
"\n\n**The big picture**" \
"\n\nThe cookies placed on your computer are not all *bad*. Cookies can help websites remember your settings and preferences, saving you time and creating a unique experience." \
"\n\nHowever, some cookies may track user activity in order to place targetted ads, or, in worse cases, steal user data or sensitive information. For this reason it is important that we know how to identify and protect against insecure cookies." \
"\n\n**How to identify whether a cookie is secure**" \
"\n\nA safe cookie will usually have some or all of the following values...\n\nis_secure: 1\n\nsamesite: 1 or 2\n\nsource_scheme: 2" \
# "\n\n**How to block insecure cookies before they are placed**" \
# "\n\nThere are many preventative measures a person can use to avoid insecure cookies. Check 'Managing Cookies' and 'Browsing Cookies' in the Resources tab to learn more."
)
