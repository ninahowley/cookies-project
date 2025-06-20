import plotly.express as px
import streamlit as st

def persistent_cookies(cookies):
    persistent = cookies['is_persistent'].sum()
    total = len(cookies['is_persistent'])
    st.write(persistent)
    st.write(total)
    st.write(f'{persistent/total * 100}% of your cookies are persistent!')