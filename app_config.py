import streamlit as st

# Application Layout Configuration
def app_config():
    page_title = "HC MANAGER"
    page_icon = ":technologist:"
    layout = "wide"

    st.set_page_config(page_title=page_title, page_icon=page_icon,
                   layout=layout, initial_sidebar_state='expanded')
    st.markdown("<h2 style='text-align: center;'>HEADCOUNT MANAGEMENT DASHBOARD</h2>",
                    unsafe_allow_html=True)
    st.markdown("---")