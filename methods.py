import streamlit as st
import sqlite3
import pandas as pd
import tempfile

def display_windows_filepath():
      st.write("**Your filepath will look something like this**")
      st.write("C:\Users\your profile\AppData\Local\Google\Chrome\User Data\Default\Network")
      st.write("Make sure to replace 'your profile' with your windows login name!")
      st.write("**Upload:** Cookies.db")

def display_mac_filepath():
      st.write("1. **Go to this filepath:**", rf"Working on it...")
      st.write("2. **Upload:** Cookies.db")

def display_cookies():
        db_file = st.file_uploader("Upload your Cookies:") #type = ["db"]

        if db_file is not None:
                # Create a temporary file to store the uploaded DB
                with tempfile.NamedTemporaryFile(delete=False, suffix=".db") as tmp_file:
                        tmp_file.write(db_file.getvalue())
                        tmp_db_path = tmp_file.name
                        print(tmp_db_path)
                        
                        conn = sqlite3.connect(tmp_db_path)
                        cur = conn.cursor()

                        df = pd.read_sql_query(f"SELECT * FROM cookies;", conn)
                        if not df.empty:
                                return df

