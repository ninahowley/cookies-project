import streamlit as st
import db_methods as db
import methods as m
import pandas as pd

st.html("""<style>
[data-testid="stSidebar"]> div:first-child{
background-image: url("https://thumbs.dreamstime.com/b/chocolate-chip-cookies-crumbs-forming-vertical-frame-white-background-scattered-create-visually-appealing-clean-surface-352442146.jpg");
background-size: cover;
}
</style>""")

st.header(":cookie: Share Your Data")

st.write("Our group would like to continue working with cookies to investigate the lack of transparency behind the deployment of third-party cookies, so we are asking for volunteers to upload their cookies for a potential future project. All uploaded cookies will be anonymized with their values removed for security.")

cookies = m.upload_cookies()

if isinstance(cookies, pd.DataFrame):
    st.write("Streamlit does not automatically save uploaded files.")
    st.write("The cookies you uploaded for the follow along will be removed from the website's memory when you close the tab.")
    st.write("If you would like to share your cookies, click the checkbox below.")

    consent = st.checkbox("I understand and would like to share my cookies.")

    if consent:
        
        cookie_name = m.your_cookie_type(cookies)
        st.write(f"Your anonymized cookie username is: *{cookie_name}*.")

        upload = st.button("Share my cookies!")
        if upload:
            try:
                db.upload_cookies(cookie_name, cookies)
            except Exception as e:
                st.warning("An error occured.")