import streamlit as st
import sqlite3
import pandas as pd
import tempfile

def display_windows_filepath():
    """
    Displays instructions to find Cookies.db on a Windows machine.
    """
    st.write("**Follow this filepath, replacing 'your profile' with your windows login username...**")
    st.write(rf"C:\Users\your profile\AppData\Local\Google\Chrome\User Data\Default\Network")
    st.write("\n**Drag and Drop:** Cookies.db")

def display_mac_filepath():
    """
    Displays instructions to find Cookies.db on a Mac machine.
    """
    st.write("**Follow these instructions to find your cookies...**")
    st.write("1. Open Finder")
    st.write("2. Command + Shift + G")
    st.write("3. Type: ~/Library/Application Support/Google/Chrome/Default/")
    st.write("\n**Drag and Drop:** Cookies.db")

def upload_cookies() -> pd.DataFrame:
    """
    Collects Cookies.db from user and returns it as a pandas dataframe.
    """
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
                        
def display_raw_cookies(cookies):
    """
    Displays the raw data from a user's Cookies.db file.
    """
    if isinstance(cookies, pd.DataFrame):
        st.write(cookies)

def get_domain(host_key: str) -> str:
    """
    Returns the domain associated with a cookie's host key.
    """
    try:
        parts = host_key.split(".")
        return (parts[-2], f".{parts[-1]}")
    except IndexError:
        return host_key

def sort_cookie_domains(cookies: pd.DataFrame) -> dict:
    """
    Returns something...
    """
    if isinstance(cookies, pd.DataFrame):
        host_keys = cookies['host_key']
        domain_dict = {}
        for key in host_keys:
            print(key)
            domain = get_domain(key)
            if domain not in domain_dict:
                domain_dict[domain] = 1
            else:
                domain_dict[domain] = domain_dict[domain] +1
        st.write(domain_dict)
        return domain_dict
    else:
        return

print(get_domain(".vote.org"))
print(get_domain("chat.google.com"))
print(get_domain(".workspace.google.com"))
print(get_domain("github.com"))



