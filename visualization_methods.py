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
        st.plotly_chart(fig)

def securityVsParty(cookies):
    """"
    STILL WORKING!!!!!
    Returns a dataframe that will be converted into a stacked bar chart. 
    Shows the proportions of first party/third party cookies that are secure/insecure respectively. 
    X = First Party Cookie, Third Party Cookie
    Stack = Secure Cookie, Insecure Cookie 
    Y = Frequency 
    """
    # initialize four lists 1st + secure, 3rd + secure, 1st + insecure, 3rd + insecure 
    fs = []
    ts = []
    fi = []
    ti = []
    for cookie in cookies: 
        party = cookie["has_cross_site_ancestor"]
        security = cookie["is_secure"]
        if party == 0 and security == 1:
            fs.append(cookie)
        if party == 1 and security == 1:
            ts.append(cookie)
        if party == 0 and security == 0:
            fi.append(cookie)
        else:
            ti.append(cookie)
    
    first = fs + fi
    third = ts + ti

    df = pd.DataFrame(
        {
            "col1": [len(first), len(third)],
            "col2": [[len(fs), len(fi)], [len(ts), len(ti)]]
    }
    )




