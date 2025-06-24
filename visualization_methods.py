import plotly.express as px
import streamlit as st
from datetime import datetime
import pandas as pd
import methods as m

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
        st.plotly_chart(fig)
    else:
        st.write("No data yet. Input data for visualization.")
#domain double bar chart

def double_bar(cookies):
    if cookies is not None and 'host_key' in cookies.columns and 'is_secure' in cookies.columns:
        df = cookies.copy()
        df['domain_short'] = cookies['host_key'].str.lstrip('.').str.split('.').str[-2:].str.join('.')

        counts = df.groupby(['domain_short', 'is_secure']).size().reset_index(name='count')
        # Convert is_secure to string labels before creating df_counts and plotting
        counts['is_secure'] = counts['is_secure'].map({1: 'Secure', 0: 'Not Secure'})
        df_counts = pd.DataFrame(counts)

        #pivot so domain is row
        pivot_df_counts = df_counts.pivot(index= 'domain_short', columns='is_secure', values='count')
        #st.write(pivot_df_counts)
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
        st.plotly_chart(fig)

#domains for secure
def on_secure(cookies):
    if cookies is not None and 'is_secure' in cookies.columns and 'host_key' in cookies.columns:
        secure_cookies = cookies[cookies['is_secure'] == 1]['host_key'].unique() #NumPy array of unique domain values
        st.write("Here are the domains with secure cookies:")
        for domain in secure_cookies:
            st.write(domain)

def on_insecure(cookies):
    if cookies is not None and 'is_secure' in cookies.columns and 'host_key' in cookies.columns:
        insecure_cookies = cookies[cookies['is_secure'] == 0]['host_key'].unique() #NumPy array of unique domain values
        st.write("Here are the domains with insecure cookies:")
        for domain in insecure_cookies:
            st.write(domain)