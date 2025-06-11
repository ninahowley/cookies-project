import streamlit as st
import sqlite3
import pandas as pd
import tempfile

def display_windows_filepath():
    st.write("**Follow this filepath, replacing 'your profile' with your windows login username...**")
    st.write(rf"C:\Users\your profile\AppData\Local\Google\Chrome\User Data\Default\Network")
    st.write("\n**Drag and Drop:** Cookies.db")

def display_mac_filepath():
    st.write("**Follow these instructions to find your cookies...**")
    st.write("1. Open Finder")
    st.write("2. Command + Shift + G")
    st.write("3. Type: ~/Library/Application Support/Google/Chrome/Default/")
    st.write("\n**Drag and Drop:** Cookies.db")

def upload_cookies():
    db_file = st.file_uploader("")

    if db_file is not None:
        # Create a temporary file to store the uploaded DB
        with tempfile.NamedTemporaryFile(delete=False, suffix=".db") as tmp_file:
            tmp_file.write(db_file.getvalue())
            tmp_db_path = tmp_file.name
            
            conn = sqlite3.connect(tmp_db_path)
            cur = conn.cursor()

            df = pd.read_sql_query(f"SELECT * FROM cookies;", conn)
            if not df.empty:
                return df
                        
def display_cookies(cookies):
    st.write(cookies)

