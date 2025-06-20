import streamlit as st
import sqlite3
import pandas as pd
import tempfile
import requests
import csv
import plotly.express as px

def display_windows_filepath():
    """
    Displays instructions to find Cookies.db on a Windows machine.
    """
    st.write("**Follow this filepath, replacing 'your profile' with your windows login username...**")
    st.write(rf"C:\Users\your profile\AppData\Local\Google\Chrome\User Data\Default\Network")
    st.write("\n**Drag and Drop:** Cookies.db")

def display_mac_filepath():
    """
    Displays instructions to find Cookies.db on a Mac machine.
    """
    st.write("**Follow these instructions to find your cookies...**")
    st.write("1. Open Finder")
    st.write("2. Command + Shift + G")
    st.write("3. Type: ~/Library/Application Support/Google/Chrome/Default/")
    st.write("\n**Drag and Drop:** Cookies.db")

def upload_cookies() -> pd.DataFrame:
    """
    Collects Cookies.db from user and returns it as a pandas dataframe.
    """
    db_file = st.file_uploader("Upload your cookies!")

    if db_file is not None:
        # Create a temporary file to store the uploaded DB
        with tempfile.NamedTemporaryFile(delete=False, suffix=".db") as tmp_file:
            tmp_file.write(db_file.getvalue())
            tmp_db_path = tmp_file.name
            
            conn = sqlite3.connect(tmp_db_path)
            cur = conn.cursor()

            df = pd.read_sql_query(f"SELECT creation_utc, host_key, top_frame_site_key, name, value, path, expires_utc, is_secure, is_httponly, last_access_utc, has_expires, is_persistent, priority, samesite, source_scheme, source_port, last_update_utc,source_type,has_cross_site_ancestor FROM cookies", conn)
            if not df.empty:
                return df
                        
def display_raw_cookies(cookies):
    """
    Displays the raw data from a user's Cookies.db file.
    """
    if isinstance(cookies, pd.DataFrame):
        st.write(cookies)

def get_domain(host_key: str) -> str:
    """
    Returns the domain associated with a cookie's host key.
    """
    try:
        parts = str(host_key).split(".")
        return (parts[-2], f".{parts[-1]}")
    except IndexError:
        return str(host_key)

def sort_cookie_domains(cookies: pd.DataFrame) -> dict:
    """
    Returns something...
    """
    if isinstance(cookies, pd.DataFrame):
        host_keys = cookies['host_key']
        domain_dict = {}
        for key in host_keys:
            domain = get_domain(key)[0]
            if domain not in domain_dict:
                domain_dict[domain] = 1
            else:
                domain_dict[domain] = domain_dict[domain] +1

        df = pd.DataFrame(domain_dict.items(), columns=["Domain", "Count"])
        sorted_df = df.sort_values(by=['Count'], ascending=False)

        st.header("**Top 10 domains...**")
        top_10 = sorted_df.head(10)
        st.bar_chart(
            data=top_10,
            x="Domain",
            y="Count",
            horizontal=True,
            )
        
        st.header("**Domains breakdown...**")
        st.write(sorted_df)

        return sorted_df
    
    else:
        return

#Getting cookies
def get_cookies(website):
    if st.form_submit_button("Fetch First-Party Cookies"):
        try:
            response = requests.get(website)
            cookies = response.cookies

            st.success(f"{len(cookies)} cookie(s) found.")

        # Display each cookie
            for cookie in cookies:
                st.write({
                    "name": cookie.name,
                    "value": cookie.value,
                    "domain": cookie.domain,
                    "path": cookie.path,
                    "expires": cookie.expires,
                    "secure": cookie.secure
                })
        except Exception as e:
            st.error(f"Failed to fetch cookies: {e}")

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

# print(get_domain(".vote.org"))
# print(get_domain("chat.google.com"))
# print(get_domain(".workspace.google.com"))
# print(get_domain("github.com"))
# print(get_domain("localhost"))

def categorize_cookies(cookies):
    with open("open-cookie-database.csv", 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        all_cookies = list(reader)

    domains = [row["Domain"] for row in all_cookies]
    category = [row["Category"] for row in all_cookies]
    dom_cat = dict(zip(domains, category))
    print(dom_cat)
    if isinstance(cookies, pd.DataFrame):
        host_keys = cookies['host_key']
        domain_dict = {}
        for key in host_keys:
            if key.lstrip('.') in dom_cat.keys():
                print(key.lstrip('.'))
                domain_dict[key] = dom_cat[key.lstrip('.')]
            else:
                domain_dict[key] = "Unknown"

        df = pd.DataFrame(domain_dict.items(), columns=["Domain", "Type"])
        st.header("Categorization of your cookies")
        st.dataframe(df)

def display_description(selection: str) -> str:
    descriptions_dict = {
        'creation_utc':"Specifies the exact time that a cookie was placed on your computer.\n\nUTC stands for 'Coordinated Universal Time'.\n\nAll timezones, such as EST, are defined by their offset from UTC.",
        'host_key':"Specifies the domain or subdomain that a cookie is associated with.\n\nCetermines which website(s) can access and use that cookie.\n\nFor example, a host key of .example.com allows the cookie to be used by www.example.com and sub.example.com.",
        'top_frame_site_key':"",
        'name':"", 
        'value':"",
        'encrypted_value':"", 
        'path':"", 
        'expires_utc':"",
        'is_secure':"", 
        'is_httponly':"", 
        'last_access_utc':"", 
        'has_expires':"",
        'is_persistent':"", 
        'priority':"", 
        'samesite':"", 
        'source_scheme':"",
        'source_port':"", 
        'last_update_utc':"", 
        'source_type':"", 
        'has_cross_site_ancestor':""
        }
    
    
    return descriptions_dict[selection]