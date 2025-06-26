import streamlit as st
import sqlite3
import pandas as pd
import numpy as np

import db_methods as db
import db_sync

import methods as m

st.title("Introduction")

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
