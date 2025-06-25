import streamlit as st
import db_methods as db
import db_sync
import sqlite3
import pandas as pd
import methods
import methods

db_sync.download_db_from_github()

conn = sqlite3.connect("Example_Cookies.db")
cur = conn.cursor()

cookies = pd.read_sql_query(f"SELECT * FROM cookies", conn)

st.write(db.get_db())

username = methods.generate_username()
st.write(f"Test username: {username}")

upload = st.button("Test uploading cookies")
if upload:
    db.upload_cookies(str(username), cookies)
    st.rerun()

clear = st.button("Clear cookies DB")
if clear:
    db.clear_db()
    st.rerun()