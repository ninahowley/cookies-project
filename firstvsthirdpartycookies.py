import streamlit as st
import pandas as pd
import methods as m
import visualization_methods as vm

st.header(":cookie: First vs. Third Party Cookies")
st.write("While it is difficult to identify cookies as first or third party based only on their attributes, if you have some time to look through all of the domains manually, you can identify which cookies are first vs third party!")

# Upload domain list
cookies = m.upload_cookies()

# Read and store domain list only once
if isinstance(cookies, pd.DataFrame):
    domains_dict = m.sort_cookie_domains_tld(cookies)
    domains = sorted(domains_dict.items())
    sorted_domains = dict(domains)

    domain_l = list(sorted_domains.keys())
    domain_list = [d for d in domain_l if "." in d]

    st.session_state.domain_list = domain_list
    # Also reset prior results if uploading a new file
    st.session_state.pop("visited_domains", None)
    st.session_state.pop("not_visited", None)
    st.session_state.pop("submitted", None)

    if "domain_list" in st.session_state:
        domain_list = st.session_state.domain_list

        st.markdown("### Select the websites you **have visited**:")
        st.markdown("Check the boxes for the ones you recognize. Leave unchecked if unknown.")

        cols_per_row = 4
        visited_domains = []

        for i in range(0, len(domain_list), cols_per_row):
            cols = st.columns(cols_per_row)
            for j in range(cols_per_row):
                if i + j < len(domain_list):
                    domain = domain_list[i + j]
                    if cols[j].checkbox(domain, key=f"ck_{domain}"):
                        visited_domains.append(domain)
        
        not_visited = [d for d in domain_list if d not in visited_domains]

        # if st.button(":cookie: Submit", type="primary"):
        #     st.session_state.visited_domains = visited_domains
        #     st.session_state.not_visited = [d for d in domain_list if d not in visited_domains]
        #     st.session_state.submitted = True

    # if st.session_state.get("submitted", False):
        # visited_domains = st.session_state.visited_domains
        # not_visited = st.session_state.not_visited

    st.divider()
    visited_d = {}
    unvisited_d = {}
    for key in domain_list:
        if key in visited_domains:
            visited_d[key] = domains_dict[key]
            df = pd.DataFrame(visited_d.items(), columns=["Domain", "Number of Cookies"])
            visited_df = df.sort_values(by=['Number of Cookies'], ascending=False)
        else:
            unvisited_d[key] = domains_dict[key]
            df = pd.DataFrame(unvisited_d.items(), columns=["Domain", "Number of Cookies"])
            unvisited_df = df.sort_values(by=['Number of Cookies'], ascending=False)

    
    col1, col2 = st.columns((1, 2))
    with col1:
        st.subheader(f"First-party domains ({len(visited_domains)})")
        if visited_domains:
            value = 10
            if len(visited_domains) < 10:
                value = len(visited_domains)
            num1 = st.slider(label="**Number of domains to display**", min_value=1, max_value=len(visited_domains), value=value)
            with st.expander("Show domains"):
                st.markdown("\n".join(f"- {d}" for d in visited_domains))
                st.download_button(
                    label="Download First-party list",
                    data="\n".join(visited_domains),
                    file_name="first_party_domains.txt",
                    mime="text/plain"
                )
            with col2:
                vm.domain_breakdown(visited_df, num1, "Number of Cookies per Known Domain", "3")
        else:
            st.markdown("*No websites marked as visited.*")


    col1, col2 = st.columns((1, 2))
    with col1:
        st.subheader(f"Third-party domains ({len(not_visited)})")
        if not_visited:
            value = 10
            if len(not_visited) < 10:
                value = len(not_visited)
            num2 = st.slider(label="**Number of domains to display**", min_value=1, max_value=len(not_visited), value=value)
            with st.expander("Show domains"):
                st.markdown("\n".join(f"- {d}" for d in not_visited))
                st.download_button(
                    label="Download Third-party list",
                    data="\n".join(not_visited),
                    file_name="third_party_domains.txt",
                    mime="text/plain"
                )
            with col2:
                vm.domain_breakdown(unvisited_df, num2, "Number of Cookies per Unknown Domain", "4")
        else:
            st.markdown("*No websites marked as unknown.*")
        



