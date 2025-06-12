import streamlit as st

st.set_page_config(
        page_title="Cookies Project",
        initial_sidebar_state="expanded",
        layout="wide")

pages = {
    "Menu": [
        st.Page("introduction.py", title="Introduction"), #intro to cookies --> example db
        st.Page("followalong.py", title="Follow Along"),
    ]
}

pg = st.navigation(pages)
pg.run()