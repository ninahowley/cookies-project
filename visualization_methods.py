import streamlit as st
import pandas as pd 



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




