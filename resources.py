import streamlit as st

st.header("Resources")

one, two, three = st.columns(3)

b1 = one.button("Guide on Cookies", use_container_width=True)
if b1:
     st.write("https://docs.google.com/presentation/d/1ptwSa7iPPFH59lXnABAMPUpgtUXNqvT1JhtzTnBm1uE/edit?usp=sharing")

b2 = two.button("Managing Cookies")
if b2:
     st.markdown("**1.** Go to settings > privacy and security.")
     st.markdown("**2.** Delete browsing data (Cookies and other site data & Cached images and files) frequently to reduce tracking and remove outdated information.")
     st.markdown("**3.** Set your preferences for Third-party cookies. You can also choose to enable “send a ‘Do not track’ request with your browsing traffic”./" \
     "While this does not guarantee that your information will not be tracked, since the exact response depends on how the website interprets this request, it is still /" \
     "an extra protective guardrail against potential privacy violations.")

b3 = three.button("Browsing Websites")
if b3:
     st.markdown("Read cookie pop-ups and review your options before selecting your cookie preferences for each site you visit.")
     st.markdown("Only allow cookies on trusted websites.")
     st.markdown("Use browser extensions to manage cookies for you. These are particularly helpful for blocking third-party cookie /" \
     "pop-ups that may be more obscure.")
     
