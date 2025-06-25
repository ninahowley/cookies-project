import streamlit as st
import os 
import pandas as pd
import sqlite3
import methods as m
import visualization_methods as vm
import plotly.graph_objects as go
from datetime import time

st.header(":cookie: An Introduction to Web Cookies")
st.subheader("Let's explore this interactive website to learn about cookies and data privacy!")

# user = os.getlogin()
# st.write("Hello, ", user)

with st.expander("**Instructions to find cookies with your operating system.**"):
    col1, col2 = st.columns((1,1))
    with col1:
        st.subheader("Windows")
        m.display_windows_filepath()
    with col2:
        st.subheader("Mac")
        m.display_mac_filepath()

#upload cookies
cookies = m.upload_cookies()

# if isinstance(cookies, pd.DataFrame):
#Button to show raw cookies db
if "show_db" not in st.session_state:
    st.session_state.show_db = False

def toggle_db():
    st.session_state.show_db = not st.session_state.show_db

button_label = "Collapse database" if st.session_state.show_db else "Click to see cookies database"

# Use the button to toggle
st.button(
    button_label,
    on_click=toggle_db
)


if st.session_state.show_db:
    m.display_raw_cookies(cookies)

st.subheader("After you upload, toggle through these topics to visualize your own cookies!")

if isinstance(cookies, pd.DataFrame):
    #creating selectbox for visualizations
    visualization = st.selectbox(
        "Click here to learn about each topic",
        ["Domain Exploration", "Cookie Security", "Third Party Cookies", "Persistent Cookies", "Size of Cookies"],
        index=None,
        placeholder="Select a topic to explore..."
    )

    #Cookie Security selection
    if visualization == "Cookie Security":
        st.header("Cookie Security")
        st.write("Let's explore the secure and samesite cookies! :cookie: ")
        #creating cookie security pie charts
        #col1, col2 = st.columns((1,1))
        #with col1:

        #with col2:
        st.subheader("Secure vs. insecure cookies")
        st.write("Let's learn about cookie security! Below is a pie chart showing the proportions of your secure and insecure cookies.")

        st.write("\n\n**Secure cookies** are designed to **only be transmitted over HTTPS**, which means they are encrypted only when sent from the domain to server and are less vulnerable to interception. " \
        "Web browsers (or user agents) will only include the cookie in an **HTTPS request**, only if it is transmitted over a secure channel (likely HTTPS). HTTPS is secure because it uses encryption to " \
        "protect data in transit between the user's browser to server." \
        "\n\nHowever, **insecure cookies** can be sent over **HTTP**, which transmits data in **plain text**, potentially exposing this information to attackers. ")
        vm.pie_chart(cookies)
        st.write("In the database, to see if cookies are secure or insecure, look at the *is_secure* attribute. ***is_secure* = 1** means it's secure and ***is_secure* = 0** means it's not secure. ")

        vm.double_bar(cookies)


        st.subheader("SameSite Cookies")
        st.write("The SameSite attribute is set in place to protect against Cross-Site Request Forgery (CSRF) attacks, where a malicious website tricks the browser into performing unwanted actions." \
        "For example, hackers can inherit the user's cookies and send unauthorized commands to another website, appearing as a 'trusted user'." \
        " SameSite is here to limit when cookies can be sent.")

        st.write("*You can hover above the pie chart to see the exact count for each attribute.*")

        c1, c2 = st.columns((1,1), gap = "large")
        with c1:
            vm.sameSite(cookies)
            st.caption("*: Chrome treats unspecified sameSite attributes as lax.")
        with c2:
            option = st.selectbox("Now, let's dive a little deeper into what each of these values means!", ("None", "Lax", "Strict"))
            if option == "None":
                st.write("Cookies will be shared between sites with all cross-site requests, but this requires that the cookie is a Secure one. This attribute can be used for Third Party cookies.")
            elif option == "Lax":
                st.write("Cookies will be shared across domains, meaning that they will be sent for top-level navigations. For example, when you click on a link leading to the site, the cookie will be sent.")
                st.write("Chrome's default is to treat the SameSite attribute as = Lax if it is missing.")
            else:
                st.write("Cookies will only be sent if the request originates from the same site. Examples of websites that use SameSite = Strict are financial service websites, where privacy of personal information is incredibly crucial.")
        
    if visualization == 'Persistent Cookies':
        st.header("Persistent Cookies")
        st.write("Add text")
        #creating cookie security pie charts
        col1, col2 = st.columns((1,1))
        with col1:
            vm.persistent_cookies(cookies)
        with col2:
            st.write("Add information")
        
    if visualization == "Third Party Cookies":
        st.subheader("Third Party Cookies")
        st.write("A third party cookie is a cookie that belongs to a different domain from the one shown in the address bar. It typically appears when webpages have content from external browsers, such as banner advertisements.")
        st.write("What distinguishes a first party cookie from a third party cookie?")
        df = pd.DataFrame(
            {
                "Aspect": ["Purpose", "Data Ownership", "Management"],
                "First Party Cookies": ["Store user data and preferences",
                            "Set by the website you're visintg",
                            "Supported by all browsers and can be blcoked or deleted by user"],
                "Third Party Cookies": ["Tracks user activity across multiple sites",
                            "Set by external servers",
                            "Supported by all browsers but increasingly blocked by default"]
            }
        )
        st.table(df)

        st.write("We can't access third-party cookies directly from our database, since it's not stored anywhere. However, we can inspect these in real-time on the websites we visit!")
        with st.expander("**Instructions to investigating your third-party cookies on a website**"):
            st.write("Here's a demonstration video of what third party cookies 'look like' on your browser:")
            st.video("3rdparty_demo1.mov", muted = True)
            st.write("**1.** Open any website.")
            st.write("**2.** Double right click and select Inspect at the bottom of the bar.")
            st.write("**3.** Don't be intimidated by the html code! Go to Applications > Cookies.")
            st.write("Tada! You can now see both first and third party cookies on your website in real time. If you can't see any third party cookies, it's likely that you already blocked it in settings.")
            st.video("3rdparty_demo2.mov", muted = True)
            st.caption("You can also refresh the webpage to see the cookies pop up...")
        # st.video() eventually include a demo clip of how to check your third party cookies in real time

    #creating some initial visualizations
    if visualization == "Domain Exploration":
        col1, col2 = st.columns((3,1))
        with col2:
            num = st.slider(label="Number of domains to display", min_value=1, max_value=m.get_num_domains(cookies), value=10)
        with col1:
            sorted_cookies = m.sort_cookie_domains(cookies)
            if num:
                vm.domain_breakdown(sorted_cookies, num)
            else:
                vm.domain_breakdown(sorted_cookies, 10)

    # m.categorize_cookies(cookies)

    # vm.last_accessed(cookies)

    m.your_cookie_type(cookies)

    if visualization == "Size of Cookies":
        vm.last_accessed(cookies)

    # Creating a form submission to count the number of cookies on a single website. 
    # We can use it for our wellesley college website demo.
    # unfortunately only fetches first party cookies...
    st.header("How many cookies does the Wellesley College website have?")

    cookie_count = st.form("cookies_count")

    with cookie_count:
        st.write("Paste https://www.wellesley.edu/ below to find out!")
        website = cookie_count.text_input('Enter a website:') 
        cookies_count = m.get_cookies(website)

    # st.write("No data yet. Please either upload your cookies or choose to use the example database to begin the follow along.")
else:
    st.warning("Please upload your cookies before starting the follow along.")