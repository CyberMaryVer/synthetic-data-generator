# @markdown ## ▶️ Load file
import os
import json
import random
import streamlit as st

from app_utils.openai_llm import generate_synthetic_data_batch


def load_examples():
    if "file_json" not in st.session_state:
        st.session_state["file_json"] = None
    if "random_example" not in st.session_state:
        st.session_state["random_example"] = ""

    file_upload_placeholder = st.empty()
    form_placeholder = st.empty()

    if st.session_state["file_json"]:
        with file_upload_placeholder:
            reset = st.button("Reset")

        if reset:
            st.session_state["file_json"] = None
            st.session_state["random_example"] = ""

    if st.session_state["file_json"] is None:
        with file_upload_placeholder:
            file_json = st.file_uploader("Upload a JSON file", type=["json"])
            main_key_name = "text"
            entities_key_name = "entities"
            if file_json:
                data = json.load(file_json)
                data_keys = data[0].keys()

                with form_placeholder:
                    if main_key_name not in data_keys or entities_key_name not in data_keys:
                        main_key_name = st.selectbox("Select the main key name", list(data_keys))
                        entities_key_name = st.selectbox("Select the entities key name", list(data_keys))

                    submitted = st.button("Submit")

                if submitted and main_key_name in data_keys:
                    examples = []
                    entities = []

                    for item in data:
                        example = item[main_key_name]
                        entity_list = item[entities_key_name]
                        examples.append(example)
                        entities.append(entity_list)

                    st.markdown(f"<p style='color: green;'>File loaded successfully with {len(examples)} examples.</p>",
                                unsafe_allow_html=True)
                    st.session_state["file_json"] = {"examples": examples, "entities": entities}

                elif submitted:
                    st.warning("Please select the main key name")

    if st.session_state["file_json"] and not st.session_state["random_example"]:
        st.session_state["random_example"] = random.choice(st.session_state["file_json"]["examples"])

    if st.session_state["file_json"]:
        with form_placeholder:
            example = st.session_state["random_example"]
            html = _generate_html_with_random_example(example)
            st.markdown(html, unsafe_allow_html=True)


def setup_augmentations():
    # @markdown ## ▶️ Add augmentations below
    # @markdown  - Leave the field blank if you want to disable the augmentation
    # @markdown
    # @markdown  - Disable checkbox `USE_USER_AUGS` if you are willing to use default augmentaions

    # UI for adding augmentations
    aug1 = "Add some misprints"  # @param {type: "string"}
    aug2 = "Write all names and surnames in upper case"  # @param {type: "string"}
    aug3 = "Write all names in title case and surnames in upper case"  # @param {type: "string"}
    aug4 = "Add some dates"  # @param {type: "string"}
    aug5 = "Add one more person"  # @param {type: "string"}
    aug6 = "Add mention of a person name in the middle of the document"  # @param {type: "string"}
    aug7 = "Rearrange paragraphs"  # @param {type: "string"}
    aug8 = "Add a few new paragraphs"  # @param {type: "string"}
    aug9 = "Add few more phone numbers, emails, etc."  # @param {type: "string"}
    aug10 = "Add one more organization (clinic, company, university, etc.)"  # @param {type: "string"}
    aug11 = "Add one more location (city, country, etc.)"  # @param {type: "string"}

    default_augs = [aug1, aug2, aug3, aug4, aug5, aug6, aug7, aug8, aug9, aug10, aug11]
    user_augs = []

    for i, aug in enumerate(default_augs):
        col1, col2 = st.columns((6, 1))
        with col1:
            aug_key = f"aug_{i + 1}"
            user_aug = st.text_input(f"Augmentation {i + 1}", aug, key=aug_key, max_chars=1000,
                                     label_visibility="collapsed")
        with col2:
            is_enabled_key = f"is_enabled_{i + 1}"
            is_enabled = st.checkbox(f"checkbox {i + 1}", value=True, key=is_enabled_key)

        if is_enabled:
            user_augs.append(user_aug)

    st.write({"Augmentations": user_augs})

    use_default_augs = False  # st.checkbox("Use default augmentations", value=True)
    augs = [a for a in default_augs if len(a) > 0] if use_default_augs else user_augs

    return augs


def _generate_html_with_random_example(example):
    html = f"<p style='color: green;'>📌 Random example:</p><p>{example}</p>"
    return html


def generate_synthetic_data_ui():
    if "file_json" not in st.session_state or st.session_state["file_json"] is None:
        st.warning("Please load a file with examples first")
        return
    examples = st.session_state["file_json"]["examples"]
    entities = st.session_state["file_json"]["entities"]
    augmentations = setup_augmentations()

    col1, col2 = st.columns((6, 1))

    with col1:
        # UI for generating synthetic data
        data_size = st.slider("How many examples to generate",
                              min_value=1, value=4, max_value=10, step=1)
        gpt4_share = st.slider("GPT-4 share: select 0 for GPT-3.5 Turbo for all examples, 1 for GPT-4.0 for all",
                               min_value=0.0, max_value=1.0, value=0.5, step=0.1)

        # Default values
        save_every = 10  # st.number_input("Save every", min_value=1, value=10)
        data_file = "generated_data.csv"  # st.text_input("Data file", value="generated_data.csv")

    if st.button("Generate synthetic data"):
        progress = st.progress(0)
        with st.spinner("Generating synthetic data..."):
            for i in range(data_size):
                progress.progress((i + 1) / data_size)
                data = generate_synthetic_data_batch(examples,
                                                     1,
                                                     data_file,
                                                     gpt4_share,
                                                     save_every,
                                                     augmentations)

            st.markdown(f"<p style='color: green;'>Data generated successfully with {data_size} examples.</p>",
                        unsafe_allow_html=True)
            st.dataframe(data)

            st.download_button(
                label="Download data",
                data=data.to_csv(index=False),
                file_name=data_file,
                mime="text/csv"
            )