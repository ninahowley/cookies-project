import plotly.express as px
import streamlit as st
from datetime import datetime
import pandas as pd
import methods as m


def persistent_cookies(cookies):
    if isinstance(cookies, pd.DataFrame):
        # df = cookies[['host_key', 'is_persistent']]
        persistent = cookies['is_persistent'].sum()
        total = len(cookies['is_persistent'])
        data = {
            'Type' : ['Persistent', 'Session'],
            'Amount' : [persistent, total-persistent]
        }
        df = pd.DataFrame(data=data)
        fig = px.pie(df, 
                     values='Amount', 
                     color='Type', 
                     title='Persistent Cookies',
                     color_discrete_map = {
                         'Persistent': '#fae1b8',
                         'Session': '#3f1c13',
                     })
        st.plotly_chart(fig, key="Persistent")
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
        st.plotly_chart(fig, key="last_accessed")

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
        st.plotly_chart(fig, key="security")

        return df
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
        st.plotly_chart(fig, key="samesite")
    else:
        st.write("No data yet. Input data for visualization.")
        

#Cookie Security visualization
def pie_chart(cookies):
    if cookies is not None:
        counts = cookies['is_secure'].value_counts().rename({1: 'Secure', 0: 'Not Secure'})
        df = counts.reset_index()
        df.columns = ['Security', 'Count']

        fig = px.pie(df, 
                     values='Count', 
                     names='Security', 
                     title='Proportion of Secure and Insecure Cookies', 
                     color= 'Security',
                     color_discrete_map = {
                         'Secure': '#dc8e5e',
                         'Not Secure': '#3f1c13',
                     })
        fig.update_traces(textinfo = 'label+percent')
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, key="pie_chart")
    else:
        st.write("No data yet. Input data for visualization.")
#domain double bar chart

def double_bar(sorted_cookies, count):
    '''
    Creates a double bar chart showing num of secure and insecure cookies per domain 
    '''
    top_domains = sorted_cookies.head(count).sort_values(by="Number of Cookies", ascending=False)
    counts = top_domains.groupby(['domain_short', 'is_secure']).size().reset_index(name='count')
    # Convert is_secure to string labels before creating df_counts and plotting
    counts['is_secure'] = counts['is_secure'].map({1: 'Secure', 0: 'Not Secure'})
    df_counts = pd.DataFrame(counts)

    df_counts = df_counts.fillna(0)
    df_counts = df_counts.sort_values(['domain_short', 'is_secure'])

    #make bar chart
    fig = px.bar(df_counts, 
                    x='domain_short', 
                    y='count', 
                    color='is_secure', 
                    barmode = 'group',
                    labels={'domain_short': 'Domain', 'count': 'Number of Cookies', 'is_secure':'Security'},
                title='Number of Secure and Not Secure Cookies per Domain',
                color_discrete_map = {
                        'Secure': '#fae1b8',
                        'Not Secure': '#3f1c13',
                    }

    )
    st.plotly_chart(fig, key="double_bar")

def domain_breakdown(sorted_cookies: pd.DataFrame, count: int):
    top_domains = sorted_cookies.head(count).sort_values(by="Number of Cookies", ascending=False)
    fig = px.bar(top_domains, 
                    x='Domain', 
                    y='Number of Cookies', 
                    title='Number of Cookies per Domain',
                    color="Number of Cookies",
                    color_continuous_scale=px.colors.make_colorscale(['#fae1b8', '#3f1c13']),
                    )
    st.plotly_chart(fig, key="domains")
    
