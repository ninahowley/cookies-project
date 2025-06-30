import streamlit as st
import sqlite3
import pandas as pd
import tempfile
import requests
import csv
from bs4 import BeautifulSoup
import time
import plotly.express as px
import random

def display_windows_filepath():
    """
    Displays instructions to find Cookies.db on a Windows machine.
    """
    st.write("Copy this filepath, replacing '🍪' with your windows login username...")
    st.write(rf"C:\Users\🍪\AppData\Local\Google\Chrome\User Data\Default\Network")
    st.write("\n**Drag and Drop:** Cookies.db")

def display_mac_filepath():
    """
    Displays instructions to find Cookies.db on a Mac machine.
    """
    st.write("Open Finder")
    st.write("Command + Shift + G")
    st.write("Type: ~/Library/Application Support/Google/Chrome/Default/")
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
        st.dataframe(cookies, hide_index=True)

def display_single_cookie(cookies):
    if isinstance(cookies, pd.DataFrame):
        cookies = cookies.head(1)
        st.dataframe(cookies, hide_index=True)

def get_domain(host_key: str) -> tuple[str, str]:
    """
    Returns the domain associated with a cookie's host key.
    """
    try:
        parts = str(host_key).split(".")
        return (parts[-2], f".{parts[-1]}")
    except IndexError:
        return str(host_key)
    
def get_domain_tld(host_key: str) -> tuple[str, str]:
    """
    Returns the domain associated with a cookie's host key.
    """
    try:
        parts = str(host_key).split(".")
        return (f"{parts[-2]}.{parts[-1]}")
    except IndexError:
        return str(host_key)
    
def get_domain_long(host_key: str) -> tuple[str, str]:
    """
    Returns the domain associated with a cookie's host key.
    """
    try:
        parts = str(host_key).split(".")
        if parts[0].split("/")[-1]:
            return (parts[0].split("/")[-1], f".{parts[-1]}")
        else:
            return (f"{parts[0].strip('/:')}*", f".{parts[-1]}")
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

        df = pd.DataFrame(domain_dict.items(), columns=["Domain", "Number of Cookies"])
        sorted_df = df.sort_values(by=['Number of Cookies'], ascending=False)

        return sorted_df
    
    else:
        return
    
def sort_cookie_domains_tld(cookies: pd.DataFrame) -> dict:
    """
    Returns something...
    """
    if isinstance(cookies, pd.DataFrame):
        host_keys = cookies['host_key']
        domain_dict = {}
        for key in host_keys:
            domain = get_domain_tld(key)
            if domain not in domain_dict:
                domain_dict[domain] = 1
            else:
                domain_dict[domain] = domain_dict[domain] +1

        df = pd.DataFrame(domain_dict.items(), columns=["Domain", "Number of Cookies"])
        sorted_df = df.sort_values(by=['Number of Cookies'], ascending=False)

        return domain_dict
    
    else:
        return

def get_num_domains(cookies: pd.DataFrame) -> int:
    """
    Returns something...
    """
    if isinstance(cookies, pd.DataFrame):
        host_keys = cookies['host_key']
        domain_list = []
        for key in host_keys:
            domain = get_domain(key)[0]
            if domain not in domain_list:
                domain_list.append(domain)

        return len(domain_list)
    
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


# print(get_domain(".vote.org"))
# print(get_domain("chat.google.com"))
# print(get_domain(".workspace.google.com"))
# print(get_domain("github.com"))
# print(get_domain("localhost"))

def categorize_cookies(cookies):
    with open("open-cookie-database.csv", 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        all_cookies = list(reader)

    all_names = [row["Cookie / Data Key name"] for row in all_cookies]
    category = [row["Category"] for row in all_cookies]
    dom_cat = dict(zip(all_names, category))
    if isinstance(cookies, pd.DataFrame):
        names = cookies['name'].unique()
        domain_dict = {}
        for name in names:
            if name in dom_cat.keys() and name not in domain_dict.keys():
                domain_dict[name] = dom_cat[name]
            # else:
            #     base_url = f'https://cookiepedia.co.uk/website/{key_stripped}'
            #     headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36"}
            #     response = requests.get("http://httpbin.io/user-agent", headers=headers)
            #     response = requests.get(base_url, headers=headers)
            #     if response.status_code == 200:
            #         try:
            #             soup = BeautifulSoup(response.text, 'html.parser')
            #             cookie_type = soup.find(class_='cookie-details clearfix')
            #             cookie_type = cookie_type.find_all('li')
            #             cookie_type = str(cookie_type[0]).split(' ')[-1]
            #             cookie_type = cookie_type.split('<')[0]
            #             domain_dict[key] = cookie_type
            #             time.sleep(2)
            #             print(f'{key} retrieved')
            #         except:
            #             domain_dict[key] = 'Unknown'
            elif "_ga" in name or "_pk" in name:
                domain_dict[name] = "Analytics"
            elif "_uin" in name or "_uir" in name or "KRTB" in name:
                domain_dict[name] = "Marketing"
            else:
                print(f'{name} not found')
                #domain_dict[name] = "Unknown"

        df = pd.DataFrame(domain_dict.items(), columns=["Name", "Type"])
        st.header("Categorization of your cookies")
        st.dataframe(df)

def display_description(selection: str) -> str:
    descriptions_dict = {
        'creation_utc':"Specifies the exact time that a cookie was placed on your computer.\n\nThe number values in this column represent an exact second in time, in the form of a 'Unix timestamp'.\n\nThe Unix timestamp specifies the number of seconds that have elapsed since January 1, 1970.",
        'host_key':"Specifies the domain or subdomain that created and sent a cookie to your device.", #\n\nDetermines which website(s) can access and use that cookie. If the host_key contains a leading dot, then it can be accessed by various subdomains.\n\nFor example, a host key of '.example.com' allows the cookie to be used by www.example.com and www.sub.example.com.
        'top_frame_site_key':"Specifies the uppermost frame in a frame hierarchy. A 'frame' is created when a website's contents are opened within the bounds of another website using an embedding such as an iframe.\n\nFor example, if a domain 'example.com' embeds a youtube video in their website, youtube may send a cookie with the top frame site key as 'https://example.com.",
        'name':"Specifies the identifier for a cookie.\n\nCookie names can be used to identify the purpose of a cookie.\n\nTake for example the cookie name '_ga' in row 3.\n\nWe can use websites such as cookiepedia to see what the cookie name is associated with. '_ga' is a preformance cookie.\n\nhttps://cookiepedia.co.uk/cookies/_ga", 
        'value':"Specifies the data held within a cookie.\n\nDifferent types of cookies (essential vs non-essential) store different bits of information in this column, ranging from user preferences to browsing activity.\n\n Chrome now automatically encrypts values in the database, which is why the values aren't visible here. The values exist as plain text in the browser.",
        'encrypted_value':"Specifies the data held within a cookie that has been transformed into a secure form to prevent unauthorized access.\n\n Users can only decrypt the values on their own devices using a special keychain.", 
        'path':"Specifies the URL path that must be present for the cookie to be sent.\n\nFor example, take the website https://example.com\n\nIf the path for a cookie on this website is /something then it can be sent when the user is viewing https://example.com/something or https://example.com/something/else,\n\nbut not https://example.com/nothing", 
        'expires_utc':"Specifies the exact time that a cookie will expire from your computer. This date cannot be any later than 400 days after the cookie was set.\n\nThe number values in this column represent an exact second in time, in the form of a 'Unix timestamp'.\n\nThe Unix timestamp specifies the number of seconds that have elapsed since January 1, 1970.",
        'is_secure':"Specifies whether a cookie is only sent to the server over a secure (HTTPS) connection.\n\nHTTPS connections have enhanced security for sensitive data.\n\n1 means true, 0 means false.", 
        'is_httponly':"Specifies whether a cookie is inaccessible to client-side scripts such as JavaScript.\n\nSensitive cookies should have the value true for this column in order to prevent potential data theft.\n\n1 means true, 0 means false.", 
        'last_access_utc':"Specifies the exact time that a cookie was last accessed.\n\nThe number values in this column represent an exact second in time, in the form of a 'Unix timestamp'.\n\nThe Unix timestamp specifies the number of seconds that have elapsed since January 1, 1970.",
        'has_expires':"Specifies whether a cookie will expire or not.\n\nIf this column is true, the exact expiration time will be specified under 'expires_utc'.\n\n1 means true, 0 means false.",
        'is_persistent':"Specifies whether a cookie is persistent or a session cookie.\n\n If a cookie is persistent, it is saved for a period of time.\n\nIf a cookie is a session cookie, it expires when the browser is closed.\n\n1 means true (persistent), 0 means false (session).", 
        'priority':"Specifies the priority level assigned to a cookie.\n\n Priority level influences how likely the browser is to retain that cookie under memory pressure.\n\n2 corresponds to 'high', 1 corresponds to 'medium'", 
        'samesite':"Specifies if a cookie can be sent to another URL.\n\n0 means 'None'. The cookie can be sent anywhere.\n\n1 means 'lax'. The cookie can be sent to URLs with the same domain on which it is hosted, and safe external URLs.\n\n2 means 'strict'. The cookie can only be sent to URLs with the same domain on which it is hosted.", 
        'source_scheme':"Specifies the security protocol of the site that originally placed the cookie.\n\n0 means unset or unknown protocol.\n\n1 means HTTP (unencrypted, insecure).\n\n2 means HTTPS (encrypted, secure).\n\n3 means URL (local file).\n\n4 means FTP URL (unencrypted file transfer, very rare).",
        'source_port':"Specifies the TCP port that was used when a cookie was placed.\n\nA TCP port is a method of virtual endpoint used by online applications and services to 'communicate'.\n\n433 indicates HTTPS port (encrypted, secure).\n\n80 indicates HTTP port (unencrypted, insecure).\n\n0 or -1 indicates that the port was not recorded.\n\nAny other numbers may refer to a custom port.", 
        'last_update_utc':"Specifies the exact time that a cookie was last modified.\n\nThe number values in this column represent an exact second in time, in the form of a 'Unix timestamp'.\n\nThe Unix timestamp specifies the number of seconds that have elapsed since January 1, 1970.", 
        'source_type':"Specifies how a cookie was set or accessed.\n\nSimilar to samesite.\n\n1 means originating from a HTTP website.\n\n2 means originating from a HTTPS website.\n\n3 means originating from a nonstandard website.", 
        'has_cross_site_ancestor':"Specifies whether a cookie has a cross-site ancestor.\n\nWhen a cookie has a cross-site ancesor, it is being accessed by an external domain.\n\n1 means true, 0 means false."
        }
    
    
    return descriptions_dict[selection]

# headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36"}
 
# # request the target site with the User Agent
# response = requests.get("http://httpbin.io/user-agent", headers=headers)

# key = 'google'
# base_url = f'https://cookiepedia.co.uk/website/{key}'
# response = requests.get(base_url, headers=headers)
# print(response.text)
# if response.status_code == 200:
#     soup = BeautifulSoup(response.text, 'html.parser')
#     cookie = soup.find(class_='cookie-details clearfix')
#     cookie = cookie.find_all('li')
#     print(cookie[0])
#     cookie = str(cookie[0]).split(' ')[-1]
#     cookie = cookie.split('<')[0]
#     print(cookie)

#     response = requests.get(url)

#     print(response.text)
#     print('done')

# cookiebot()

def your_cookie_type(cookies):
    if isinstance(cookies, pd.DataFrame):
        with open('tasty cookies.csv',  newline='') as f:
            reader = csv.reader(f)
            tasty_cookies = list(reader)
        cookie = tasty_cookies[len(cookies['host_key']) % 100][0]
        num = random.randint(100, 999)
        # st.write(f'Your cookie is: {cookie}!')
        cookie_name = f"{cookie} {num}"
        return cookie_name
    
def get_tfsk_rows(cookies: pd.DataFrame) -> pd.DataFrame:
    """
    Returns something...
    """
    if isinstance(cookies, pd.DataFrame):
        cookies_filtered = cookies[cookies['top_frame_site_key'].notna() & (cookies['top_frame_site_key'] != '')]
        if cookies.empty:
            return None
        else:
            return cookies_filtered
    else:
        return None
    
def get_tfsk_domains(cookies:pd.DataFrame):
    cookies_filtered = get_tfsk_rows(cookies)
    if isinstance(cookies_filtered,pd.DataFrame):
        tfsk_dict = {}
        for _,cookie in cookies_filtered.iterrows():
                tfsk = get_domain_long(cookie['top_frame_site_key'])[0]
                hk = get_domain(cookie['host_key'])[0]
                if tfsk not in tfsk_dict:
                    tfsk_dict[tfsk] = {}
                
                if hk not in tfsk_dict[tfsk]:
                    tfsk_dict[tfsk][hk] = 1
                else:
                    tfsk_dict[tfsk][hk] = tfsk_dict[tfsk][hk] + 1
        return tfsk_dict

    else:
        return None
    
def tfsk_example(cookies:pd.DataFrame):
    tfsk_dict = get_tfsk_domains(cookies)
    keys = list(tfsk_dict.keys())
    tfsk = keys[0] if "*" not in keys[0] else keys[1]
    keys2 = list(tfsk_dict[tfsk].keys())
    host_key = keys2[0]
    st.write("An example from your database:")
    st.markdown(f"The domain **{tfsk}** contained a frame which left a cookie from :primary[{host_key}].")
    st.markdown(f"This means you have a cookie with the host_key value :primary[{host_key}] and the top_frame_site_key value **{tfsk}**.")

    
def sort_cookie_names(cookies: pd.DataFrame) -> dict:
    if isinstance(cookies, pd.DataFrame):
        names = cookies['name']
        name_dict = {}
        for key in names:
            domain = get_domain(key)
            if domain not in name_dict:
                name_dict[domain] = 1
            else:
                name_dict[domain] = name_dict[domain] +1

        df = pd.DataFrame(name_dict.items(), columns=["Name", "Number of Cookies"])
        sorted_df = df.sort_values(by=['Number of Cookies'], ascending=False)

        return sorted_df
    
    else:
        return
    
def get_num_names(cookies: pd.DataFrame) -> int:
    if isinstance(cookies, pd.DataFrame):
        names = cookies['name']
        names_list = []
        for name in names:
            if name not in names_list:
                names_list.append(name)

        return len(names_list)
    
    else:
        return