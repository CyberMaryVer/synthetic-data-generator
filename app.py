from st_on_hover_tabs import on_hover_tabs
import streamlit as st
# import base64

from app_pages.home_page import main as generate
from app_utils.login import main as login_user
from app_utils.st_constants import PAGE_CONFIG

st.set_page_config(**PAGE_CONFIG)

st.markdown('<style>' + open('./style.css').read() + '</style>', unsafe_allow_html=True)


with st.sidebar:
    tabs = on_hover_tabs(tabName=[ 'Chat', 'Login'],
                         iconName=['create', 'login'],
                         default_choice=0,
                         styles={'navtab': {'background-color': '#111',
                                            'color': '#d3d3d3',
                                            'font-size': '18px',
                                            'transition': '.3s',
                                            'white-space': 'nowrap',
                                            'text-transform': 'uppercase'},
                                 'tabOptionsStyle': {':hover :hover': {'color': 'green',
                                                                       'cursor': 'pointer'}},
                                 'iconStyle': {'position': 'fixed',
                                               'left': '7.5px',
                                               'text-align': 'left'},
                                 'tabStyle': {'list-style-type': 'none',
                                              'margin-bottom': '30px',
                                              'padding-left': '30px'}},
                         key="1")

if tabs == 'Chat':
    st.markdown("## Synthetic Data Generation")
    generate(admin=True)

elif tabs == 'Login':
    st.markdown("## Admin Page")
    login_user()
