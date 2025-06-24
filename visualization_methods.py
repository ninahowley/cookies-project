import plotly.express as px
import streamlit as st
from datetime import datetime
import pandas as pd

def persistent_cookies(cookies):
    if isinstance(cookies, pd.DataFrame):
        # df = cookies[['host_key', 'is_persistent']]
        persistent = cookies['is_persistent'].sum()
        total = len(cookies['is_persistent'])
        data = {
            'Type' : ['persistent', 'not persistent'],
            'Amount' : [persistent, total-persistent]
        }
        df = pd.DataFrame(data=data)
        fig = px.pie(df, values='Amount', color='Type', title='Persistent Cookies')
        st.plotly_chart(fig)
        st.write(f'{(persistent/total * 100).round(2)}% of your cookies are persistent!')
       
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

def is_Secure(cookie): 
    """
    Helper method.
    Returns true if secure, false if insecure. 
    """
    return cookie['is_secure'] == 1

def is_FirstParty(cookie): 
   """
   Helper method.
   Returns true if first party, false if third party.
   """
   return cookie['has_cross_site_ancestor'] == 1

def securityVsParty(cookies):
    """"
    Returns a dataframe that will be converted into a stacked bar chart. 
    Shows the proportions of first party/third party cookies that are secure/insecure respectively. 
    X = First Party Cookie, Third Party Cookie
    Stack = Secure Cookie, Insecure Cookie 
    Y = Frequency 
    """
    # initialize four counters (first secure, third secure etc)
    fs, ts, fi, ti = 0, 0, 0, 0
    if isinstance(cookies, pd.DataFrame):
        for _, cookie in cookies.iterrows():
            if is_FirstParty(cookie):
                if is_Secure(cookie): 
                    fs+=1
                else: 
                    fi+=1
            else:
                if is_Secure(cookie):
                    ts+=1
                else:
                    ti+=1
    
        df = pd.DataFrame({
            "Party": ["First Party", "First Party", "Third Party", "Third Party"],
            "Security": ["Secure", "Insecure", "Secure", "Insecure"],
            "Count": [fs, fi, ts, ti]
        })
        fig = px.bar(df, x = "Party", y = "Count", color = "Security", title = "Party Security Cookies")
        st.plotly_chart(fig)

def sameSite(cookies): 
    """
    Labels and counts cookies with samesite = none, lax, strict (or NA). 
    """    
    none, lax, strict = 0, 0, 0
    if isinstance(cookies, pd.DataFrame):
        for _, cookie in cookies.iterrows():
            value = cookie['samesite']
            if value == 0: 
                none += 1
            elif value == 2:
                strict += 1
            else:
                lax += 1
        df = pd.DataFrame({
            "SameSite": ["None", "Lax*", "Strict"],
            "Count": [none, lax, strict]
        })

        fig = px.pie(df, names = "SameSite", values = "Count", title = "SameSite Attribute Distribution")
        st.plotly_chart(fig)
    else:
        st.write("No data yet. Input data for visualization.")
        




