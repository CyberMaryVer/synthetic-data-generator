import os
import csv
import streamlit as st

from utils.api_requests import get_ai_assistant_response
from utils.html_chat_tk import st_create_html_chat, st_create_html_info
from utils.update_sources import enrich_sources
from utils.metadata import EXAMPLES_B, LOGS
from dotenv import load_dotenv

load_dotenv('.env')


def main(admin=None):
    """
    This function is a main program function
    
    :return: None
    """

    col1, col2 = st.columns([5, 2])
    with col2:
        pass
    with col1:
        pass


if __name__ == "__main__":
    main(admin=False)
