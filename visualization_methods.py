import plotly.express as px
import streamlit as st
from datetime import datetime
import pandas as pd

def persistent_cookies(cookies):
    if isinstance(cookies, pd.DataFrame):
        persistent = cookies['is_persistent'].sum()
        total = len(cookies['is_persistent'])
        st.write(persistent)
        st.write(total)
        st.write(f'{persistent/total * 100}% of your cookies are persistent!')

def convert_time(time):
    time = time/1000000
    time = time - 11644473600
    timestamp = datetime.fromtimestamp(time)
    date = timestamp.date()
    return date

def last_accessed(cookies):
    if isinstance(cookies, pd.DataFrame):
        df = cookies.copy()
        df['time'] = df['creation_utc'].apply(convert_time)
        df = df[['host_key', 'time']]
        df['existing'] = df['time'].rank(method='max').astype(int)
        df = df.groupby('time')['existing'].agg('max').reset_index()
        fig = px.line(df, x='time', y='existing')
        st.write(df.sort_values('time'))
        st.plotly_chart(fig)