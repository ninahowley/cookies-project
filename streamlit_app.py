import streamlit as st

st.set_page_config(
        page_title="Cookies Project",
        initial_sidebar_state="expanded",
        layout="wide")

pages = {
    "Menu": [
        st.Page("introduction.py", title="Introduction"), #intro to cookies --> example db
        st.Page("followalong.py", title="Follow Along"),
        st.Page("share.py", title="Share Your Data"),
        st.Page("feedback.py", title="Feedback"),
        st.Page("resources.py", title="Resources")
    ]
}

pg = st.navigation(pages)
pg.run()