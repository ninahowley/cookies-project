import plotly.express as px
import streamlit as st
from datetime import datetime, timedelta
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
        fig.update_traces(line_color = '#3f1c13')
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

        fig = px.pie(df, names = "SameSite", values = "Count", title = "SameSite Attribute Distribution", 
                     color = "SameSite",
                     color_discrete_map = {
                    'None': '#fae1b8',
                    'Strict': '#3f1c13',
                    'Lax*': '#dc8e5e',
                }
                     )
        st.plotly_chart(fig, key="samesite")
    else:
        st.write("No data yet. Input data for visualization.")
        

#Cookie Security visualization
    
def pie_chart(cookies):
    cookies['domains'] = cookies['host_key'].str.lstrip('.').str.split('.').str[-2:].str.join('.')
    #secure_counts = cookies.groupby(['domains', 'is_secure']).size().reset_index(name='count')
    domain_security_sets = cookies.groupby('domains')['is_secure'].agg(set).reset_index(name='secure_set')

    only_secure = 0
    only_insecure = 0
    both = 0

    for _, row in domain_security_sets.iterrows():
        secure_set = row['secure_set']
        if secure_set == {1}:
            only_secure += 1
        elif secure_set == {0}:
            only_insecure += 1
        else:
            both += 1
        
    data = {
    "Security Status": ["Only Secure", "Only Not Secure", "Both"],
    "Count": [only_secure, only_insecure, both]
    }
    df_counts = pd.DataFrame(data)

    fig = px.pie(df_counts, 
                names = "Security Status", 
                values = "Count",
                title='Number of Domains by Cookie Security', 
                color = "Security Status",
                color_discrete_map = {
                    'Only Secure': '#fae1b8',
                    'Only Not Secure': '#3f1c13',
                    'Both': '#dc8e5e',
                })
    fig.update_layout(showlegend=True)
    st.plotly_chart(fig, key="pie_chart")
   
#domain double bar chart
def double_bar(cookies, num):
    if isinstance(cookies, pd.DataFrame) and 'host_key' in cookies.columns and 'is_secure' in cookies.columns:
        df = cookies.copy()
        #turning host_key to domain (other function didn't work)
        df['domain'] = df['host_key'].str.lstrip('.').str.split('.').str[-2:].str.join('.')

        #counts = df.groupby(['domain', 'is_secure']).size().reset_index(name='count').sort_values(by='count', ascending = False)
        #st.write(counts)
        # Convert is_secure to string labels before plotting
        # Group and pivot so each domain has separate columns for Secure and Not Secure
        grouped = df.groupby(['domain', 'is_secure']).size().unstack(fill_value=0)
        grouped.columns = ['Not Secure', 'Secure']  # Make column names readable
        grouped = grouped.reset_index()

        # Add total column to sort and limit to top `num` domains
        grouped['Total'] = grouped['Not Secure'] + grouped['Secure']
        grouped = grouped.sort_values(by='Total', ascending=False).head(num)

        #long data
        counts = grouped.melt(id_vars='domain', value_vars=['Not Secure', 'Secure'],
                      var_name='is_secure', value_name='count')
        #counts['is_secure'] = counts['is_secure'].map({1: 'Secure', 0: 'Not Secure'})

        #make bar chart
        fig = px.bar(counts, 
                     x='domain', 
                     y='count', 
                     color='is_secure', 
                     barmode = 'stack',
                     labels={'domain': 'Domain', 'count': 'Number of Cookies', 'is_secure':'Security'},
                    title='Number of Secure and Not Secure Cookies per Domain',
                    color_discrete_map = {
                         'Secure': '#fae1b8',
                         'Not Secure': '#3f1c13',
                     }

        )
        fig.update_layout(xaxis= {'categoryorder':'total descending'})
        st.plotly_chart(fig, key="double_bar")
    
def domain_breakdown(sorted_cookies: pd.DataFrame, count: int, title:str,  key:str):
    top_domains = sorted_cookies.head(count).sort_values(by="Number of Cookies", ascending=False)
    fig = px.bar(top_domains, 
                    x='Domain', 
                    y='Number of Cookies', 
                    title=title,
                    color="Number of Cookies",
                    color_continuous_scale=px.colors.make_colorscale(['#fae1b8', '#3f1c13']),
                    )
    st.plotly_chart(fig, key=key)

def name_breakdown(sorted_cookies: pd.DataFrame, count: int, title:str,  key:str):
    top_domains = sorted_cookies.head(count).sort_values(by="Number of Cookies", ascending=False)
    fig = px.bar(top_domains, 
                    x='Name', 
                    y='Number of Cookies', 
                    title=title,
                    color="Number of Cookies",
                    color_continuous_scale=px.colors.make_colorscale(['#fae1b8', '#3f1c13']),
                    )
    st.plotly_chart(fig, key=key)


def tfsk_breakdown(cookies:pd.DataFrame):
    tfsk_dict = m.get_tfsk_domains(cookies)
    if tfsk_dict:
        count = 0
        for tfsk in tfsk_dict:
            st.write(f"**{tfsk}**")
            count2 = 0
            for hk in tfsk_dict[tfsk]:
                if hk != tfsk:
                    st.markdown(f":primary[{hk}: {tfsk_dict[tfsk][hk]}]")
                    count2+=1
                    if count2 > 2:
                        break
            count+=1
            if count>=3:
                break
        return True
    else:
        return False

def chrome_time_to_datetime(chrome_time):
    """Convert Chrome/WebKit time to datetime (UTC)"""
    # Chrome/WebKit epoch starts on 1601-01-01
    epoch_start = datetime(1601, 1, 1)
    return epoch_start + timedelta(microseconds=chrome_time)

def average_expiration_date(cookies):
    if isinstance(cookies, pd.DataFrame):
        df = cookies.copy()
        average = df['expires_utc'].mean()
        average = convert_time(average)
        df['time'] = df['expires_utc'].apply(chrome_time_to_datetime)
        df = df[['host_key', 'time']]
        df['expired'] = df['time'].rank(method='max').astype(int)
        df = df.groupby('time')['expired'].agg('max').reset_index()
        fig = px.line(df, x='time', y='expired')
        fig.update_traces(line_color = '#3f1c13')
        st.plotly_chart(fig, key="expiration of cookies")
        return average