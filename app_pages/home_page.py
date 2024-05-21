import streamlit as st
from app_utils.openai_llm import set_openai_api_key
from app_utils.generation import load_examples, setup_augmentations, generate_synthetic_data_ui


def main(admin=None):
    set_openai_api_key(from_secrets=True, from_env=True)

    st.markdown("<h4 style='text-align: center; color: green;'>⬇️ Load File with Templates</h4>", unsafe_allow_html=True)
    load_examples()

    st.markdown("<h4 style='text-align: center; color: green;'>⚙️ Synthetic Data Settings</h4>", unsafe_allow_html=True)
    generate_synthetic_data_ui()