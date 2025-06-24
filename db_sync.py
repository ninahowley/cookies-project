import os
import tempfile
import requests
import base64
import streamlit as st

# Set the DB location in temp space for Streamlit Cloud
temp_dir = tempfile.gettempdir()
DB_PATH = os.path.join(temp_dir, "peckish.db")

def get_db_path():
    return DB_PATH

def download_db_from_github():
    """
    Downloads the latest DB file from your private GitHub repo
    and saves it to /tmp/ for use by Streamlit.
    """
    token = st.secrets["github"]["token"]
    repo = st.secrets["github"]["repo"]
    path = st.secrets["github"]["db_path"]
    url = f"https://api.github.com/repos/{repo}/contents/{path}"

    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3.raw"
    }

    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        with open(DB_PATH, "wb") as f:
            f.write(r.content)
        return True
    else:
        st.error(f"Failed to download DB: {r.status_code}")
        return False

def push_db_to_github():
    """
    Encodes and uploads the updated DB back to the GitHub repo.
    """
    token = st.secrets["github"]["token"]
    repo = st.secrets["github"]["repo"]
    path = st.secrets["github"]["db_path"]
    url = f"https://api.github.com/repos/{repo}/contents/{path}"

    with open(DB_PATH, "rb") as f:
        content = base64.b64encode(f.read()).decode()

    # Get existing file SHA to overwrite
    headers = {"Authorization": f"token {token}"}
    r = requests.get(url, headers=headers)
    if r.status_code != 200:
        st.error(f"Failed to fetch existing DB info: {r.status_code}")
        return False

    sha = r.json()["sha"]

    data = {
        "message": "Update aggregate_cookies.db from Streamlit app",
        "content": content,
        "sha": sha
    }

    headers = {
        "Authorization": f"token {token}"
    }

    r = requests.put(url, headers=headers, json=data)
    if r.status_code in (200, 201):
        st.success("✅ DB pushed back to private repo.")
        return True
    else:
        st.error(f"❌ Failed to push DB: {r.status_code}")
        return False
