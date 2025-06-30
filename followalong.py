import streamlit as st
import os 
import pandas as pd
import sqlite3
import db_methods as db
import methods as m
import visualization_methods as vm
import plotly.graph_objects as go
from datetime import time


st.html("""<style>
[data-testid="stSidebar"]> div:first-child{
background-image: url("https://thumbs.dreamstime.com/b/chocolate-chip-cookies-crumbs-forming-vertical-frame-white-background-scattered-create-visually-appealing-clean-surface-352442146.jpg");
background-size: cover;
}
</style>""")

st.header(":cookie: Follow Along")
st.subheader("Explore your cookies and learn about data privacy!")

st.header("Part 1: Upload your data")

# user = os.getlogin()
# st.write("Hello, ", user)

with st.expander("Instructions to find cookies with your operating system"):
    col1, col2 = st.columns((2))
    with col1:
        st.subheader("Windows")
        m.display_windows_filepath()
    with col2:
        st.subheader("Mac")
        m.display_mac_filepath()

with st.expander("I want to use the example cookies instead of my own"):
    st.write("If you want to use the example cookies database, download it from the following link and upload it to the streamlit below.")
    st.write("[Example Cookie Database](%s)" % "https://drive.google.com/file/d/1VIJxjrw6dsAGH5toMLRULxOVTVXDKreW/view?usp=sharing")

#upload cookies
cookies = m.upload_cookies()
with st.expander("Error: This file is in use"):
    st.write("This error occurs when you are currently logged into and using the account associated with that database.")
    st.write("Each chrome profile has it's own unique cookies database.")
    st.write("To work around this, you must have atleast 2 chrome profiles.")
    st.write("Simply choose 'Profile 1', 'Profile 2', (or 'Profile 3', etc...) instead of 'Default' in the filepath.")
    st.write(rf"**Windows**: C:\Users\🍪\AppData\Local\Google\Chrome\User Data\Profile 2\Network")
    st.write("**Mac**: ~/Library/Application Support/Google/Chrome/Profile 2/")

st.divider()
st.header("Part 2: View your raw data")
if isinstance(cookies, pd.DataFrame):
    col1, col2 = st.columns((2.5,1))
    with col1:
        m.display_raw_cookies(cookies)

    columns = ['creation_utc', 'host_key', 'top_frame_site_key', 'name', 
            'value', 'encrypted_value', 'path', 'expires_utc',
            'is_secure', 'is_httponly', 'last_access_utc', 'has_expires',
            'is_persistent', 'priority', 'samesite', 'source_scheme',
            'source_port', 'last_update_utc', 'source_type', 'has_cross_site_ancestor']

    selection = col2.selectbox(options=columns,label="**Choose a column to learn more about**")

    if selection:
        col2.write(m.display_description(selection))
    st.caption("Source: https://medium.com/@tushar_rs_/a-comprehensive-guide-to-cookie-attributes-3893787c4747")
else:
    st.warning("Please upload your cookies.")

st.divider()
st.header("Part 3: Visualize your data")

if isinstance(cookies, pd.DataFrame):
    st.subheader("Toggle through these topics to visualize your own cookies!")
    #creating selectbox for visualizations
    visualization = st.selectbox(
        "Click here to learn about each topic",
        ["Cookie Duration", "Domain Exploration", "First Party Cookies & Cookie Security", "Third Party Cookies & Privacy"],
        index=None,
        placeholder="Select a topic to explore..."
    )

     # m.your_cookie_type(cookies)

    #Cookie Security selection
    if visualization == "First Party Cookies & Cookie Security":

        st.subheader("What are First-Party Cookies?")
        st.write("First-party cookies are cookies **set by the domain** and are only used within the domain (ie youtube.com). They are typically used to save **login information and UI settings**.")
        st.write("These cookies can also be used to track users as they move between intra-domain pages. With this information, a profile of a users behavior can be built within the site "
        "and tailored information or targeted ads can be presented to a user.")

        st.write("For first-party cookies, the biggest concern is **security**, since session IDs (stored in cookies) are used to provide user functionality (ie login credentials)" \
                 ", which would be problematic if intercepted by an attacker.")
        st.write("Below you will learn more about cookie security!")

        st.subheader("Secure vs. insecure cookies")
        st.write("Let's learn about cookie security! Below is a pie chart showing the proportions of your secure and insecure cookies.")

        st.write("\n\n**Secure cookies** are designed to **only be transmitted over HTTPS**, which means they are encrypted only when sent from the domain to server and are less vulnerable to interception. " \
        "Web browsers (or user agents) will only include the cookie in an **HTTPS request**, only if it is transmitted over a secure channel (likely HTTPS). HTTPS is secure because it uses encryption to " \
        "protect data in transit between the user's browser to server." \
        "\n\nHowever, **insecure cookies** can be sent over **HTTP**, which transmits data in **plain text**, potentially exposing this information to attackers. ")
        st.write("In the database, to see if cookies are secure or insecure, look at the *is_secure* attribute. ***is_secure* = 1** means it's secure and ***is_secure* = 0** means it's not secure. ")
        vm.pie_chart(cookies)
        st.write("The graph above shows the total number of domains that only have secure cookies, insecure cookies, and both secure and insecure." \
                " As you can see, most domains have both secure and insecure cookies. This may be the case because we aggregated all subdomains together.")
        
        col1, col2 = st.columns((3,1))
        with col2:
            num = st.slider(label="Number of domains to display", min_value=1, max_value=m.get_num_domains(cookies), value=10)
        with col1:
            if num:
                vm.double_bar(cookies, num)
            else:
                vm.double_bar(cookies, 10)
                
        st.write("This stacked bar graph breaks down the previous bar chart by domains. **Having insecure cookies today are not as " \
                "dangerous as before** because most browsers (ie Chrome) default to HTTPS. Still, these cookies are less secure than those with the Secure flag. ")
        
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
        
        st.subheader("You (or websites) can enhance cookie security using:")
        st.markdown("- Secure: Only send over HTTPS")
        st.markdown("- HttpOnly: JavaScript can’t access it (helps prevent XSS-based theft)")
        st.markdown("- SameSite=Strict or Lax: Limits cross-site access")
        st.markdown("- Domain/Path: Limits where cookies are valid")

    if visualization == 'Cookie Duration':
        st.header("Cookie Duration")
        st.write("Let's explore cookie durations!")
        st.subheader("Persistent vs session cookies")
        st.write("**Persistent cookies** are cookies that last beyond a single browsing session.")
        st.write("Reasons for this often include saving settings, login info, preferences, etc. in order "
        "to save time and create a more convenient web browsing experience. They can also be used "
        "for marketing/analytical purposes.")
        st.write("The web host of the cookie will set the expiration date. Once this date is "
        "reached, they will either renew the cookie automatically, ask for permission to renew, "
        "or simply delete itself, but this is all dependent of the initial user agreement.")
        st.write("Cookies that are not persistent are called **session cookies**, and they expire once "
        "the browser is closed.")
        #creating pie chart
        # vm.persistent_cookies(cookies)
        # st.write("In your cookie database, you may see that the is_persistent column has values of either "
        # "1 or 0. A score of one signifies a persistent cookie while a score of 0 means it is a session "
        # "cookie.")
        st.subheader("Average Expiration Date")
        st.write("Let's see the expiration dates for your persistent cookies!")
        st.write("Below, you will see a graph that shows a timeline of when your cookies will expire. " \
        "Hover over the graph to see specific details.")
        exp = vm.average_expiration_date(cookies).strftime("%m/%d/%Y")
        st.write(f"On average, your cookies will expire on {exp}")
        st.subheader("How many cookies have you accumulated over time?")
        st.write("Below you will see a graph that shows how your cookies have accumulated in your " \
        "Chrome database over time. Hover over the graph to see more details on their creation dates.")
        vm.last_accessed(cookies)
        
    if visualization == "Third Party Cookies & Privacy":
        st.header("Third Party Cookies")
        st.write("A **third party cookie** is a cookie that belongs to a different domain from the one shown in the address bar. It typically appears when webpages have content from external browsers, such as banner advertisements.")
        st.write("Here's a helpful visualization demonstrating how third-party cookies *retarget*.")
        st.image("3rd_retargeting.png", caption = "Source: https://www.performancemarketingworld.com/article/1800951/third-party-cookies")
        st.write("Third-party servers can combine information from their cookies set on multiple sites, creating a profile of the users. These are called **tracking cookies**." \
        " For example, if you were looking at a product on a site, they might set a third-party cookie on your browser. " \
        "You might see the same product advertised to you on a another site since the cookie recognizes your user ID.")
        st.write("As mentioned in the introduction, many browsers (aside from Google) now block third-party cookies by default. ")

        st.subheader("**What distinguishes a first party cookie from a third party cookie?**")
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
        st.dataframe(df, hide_index=True)

        
        st.write("**We can't access third-party cookies directly from our database, since it's not stored anywhere**. However, we can inspect these in real-time on the websites we visit!")
        with st.expander("**Instructions for inspecting your third-party cookies on a website**"):
            st.write("Here's a demonstration video of what third party cookies 'look like' on your browser:")
            st.video("3rdparty_DEMO.mov", muted = True)
            st.caption("You can also refresh the webpage to see the cookies pop up...")
            st.write("**1.** Open any website.")
            st.write("**2.** Double right click and select Inspect at the bottom of the bar.")
            st.write("**3.** Don't be intimidated by the html code! Go to Applications > Cookies.")
            st.write("Tada! You can now see both first and third party cookies on your website in real time. If you can't see any third party cookies, it's likely that you already blocked it in settings.")
       

    #creating some initial visualizations
    if visualization == "Domain Exploration":
        st.header("Domain Exploration")
        col1, col2 = st.columns((3,1))
        with col2:
            st.write("**What is a domain name?**")
            st.write("A domain name is the text that a user types into a browser window to reach a website. For example, Google's domain name is 'google.com'.")
            st.write("For the purposes of this visualization, we combined subdomains. For example, 'accounts.google.com' would belong to 'google.com'.")
            st.write("The domain that a cookie belongs to can be found as the value for the 'host_key' column.")
            st.write("")
            num1 = st.slider(label="**Number of domains to display**", min_value=1, max_value=m.get_num_domains(cookies), value=10)

        with col1:
            st.subheader(":cookie: Domain Breakdown")
            sorted_cookies = m.sort_cookie_domains(cookies)
            if num1:
                vm.domain_breakdown(sorted_cookies, num1, "Number of Cookies per Domain", "1")
            else:
                vm.domain_breakdown(sorted_cookies, 10, "Number of Cookies per Domain", "2")
        
        st.write("If you don't recognize some of these domain names, don't worry! Many of the cookies on your device will be 'third party' cookies. You will learn more about what this means later, and you can exlpore these cookies in the 'First vs Third Party Cookies' tab.")

        st.subheader(":cookie: Name Breakdown")
        col1, col2 = st.columns((3,1))
        with col2:
            st.write("**What is a cookie name?**")
            st.write("A cookie's name is the unique identifier for a cookie.")
            st.write("This identifier helps websites and browsers track the purpose of a cookie.")
            st.write("Some cookie names are very common, such as '_ga', which you likely see in your graph.")
            st.write("")
            num2 = st.slider(label="**Number of names to display**", min_value=1, max_value=m.get_num_domains(cookies), value=10, key="slide2")

        with col1:
            sorted_cookies = m.sort_cookie_names(cookies)
            if num2:
                vm.name_breakdown(sorted_cookies, num2, "Number of Cookies per Name", "3")
            else:
                vm.name_breakdown(sorted_cookies, 10, "Number of Cookies per Name", "4")
        
        col1, col2 = st.columns((2))
        with col1:
            st.dataframe(sorted_cookies, hide_index=True, )
        with col2:
            st.write("To the left are all of the cookie names in your database, sorted by how often they appear.")
            st.write("There are many online resources that can help us identify the purpose of a cookie, including one called 'cookiepedia'.")
            st.write("If you know the name of a cookie, you can use this website to learn more about it.")
            st.write("For example, below is cookiepedia's page on the cookie name '_ga', showing that it is associated with Google Analytics.")
            st.write("**[https://cookiepedia.co.uk/cookies/_ga](%s)**" %"https://cookiepedia.co.uk/cookies/_ga")
            st.write("Not all cookies will have such a complete description, or even a description at all. There so many cookie names out there, with many being untracked.")
            st.write("Does your database have 'uid' or 'OTZ'? Try looking these up!")



            
    # st.write(m.sort_cookie_domains(cookies))

    #m.categorize_cookies(cookies)

    # vm.last_accessed(cookies)

    # if visualization == "Cookies Over Time":
    #     st.subheader("How many cookies have you accumulated over time?")
    #     vm.last_accessed(cookies)
    #     st.write("This graph shows the number of persistent cookies that have accumulated over time. " \
    #     "Right now, all of these cookies exist in your cookies database and you can see on what date " \
    #     "they were created. You can see these values in the \"creation_utc\" column of your database, "
    #     "but these values need to be converted to standard datetimes, which we have done for you in " \
    #     "the graph.")

    # Creating a form submission to count the number of cookies on a single website. 
    # We can use it for our wellesley college website demo.
    # unfortunately only fetches first party cookies...
    # st.header("How many cookies does the Wellesley College website have?")

    # cookie_count = st.form("cookies_count")

    # with cookie_count:
    #     st.write("Paste https://www.wellesley.edu/ below to find out!")
    #     website = cookie_count.text_input('Enter a website:') 
    #     cookies_count = m.get_cookies(website)

else:
    st.warning("Please upload your cookies.")