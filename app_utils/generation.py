# @markdown ## ▶️ Load file
import os
import json
import random
import streamlit as st
from datetime import datetime

from app_utils.openai_llm import generate_synthetic_data_batch, LANGUAGES

DOC1 = """
John Doe is a smart person. He is a doctor. He works at the clinic. He lives in New York."""
ENTS1 = ["John Doe", "doctor", "clinic", "New York"]
DOC2 = """
The company was founded in 1990. The company is located in London. The company has 100 employees."""
ENTS2 = ["1990", "London", "100 employees"]
DOC3 = """
Send the parcel to DigitalOcean, 101 Avenue of the Americas, New York, NY 10013, USA."""
ENTS3 = ["DigitalOcean", "101 Avenue of the Americas", "New York", "NY 10013", "USA"]


def load_examples():
    if "file_json" not in st.session_state:
        st.session_state["file_json"] = None
    if "random_example" not in st.session_state:
        st.session_state["random_example"] = ""
    if "data_file" not in st.session_state:
        st.session_state["data_file"] = None

    file_upload_placeholder = st.empty()
    form_placeholder = st.empty()
    info_placeholder = st.empty()

    if st.session_state["file_json"]:
        with file_upload_placeholder:
            reset = st.button("Reset")

        if reset:
            st.session_state["file_json"] = None
            st.session_state["random_example"] = ""
            st.session_state["data_file"] = None

    if st.session_state["file_json"] is None:
        st.write("""Please load a file with examples
        File should be a JSON file with the following structure:
        [
            {
                "text": "Example text",
                "entities": ["entity1", "entity2"]
            },
            ...
        ]
        If the keys are different, you can select them below.
        If you want to test the functionality, just check the box below 'Use test data' and click 'Submit'
        """)
        if st.checkbox("Use test data"):
            examples = [
                {"text": DOC1, "entities": ENTS1},
                {"text": DOC2, "entities": ENTS2},
                {"text": DOC3, "entities": ENTS3}
            ]
            st.session_state["file_json"] = {"examples": [item["text"] for item in examples],
                                             "entities": [item["entities"] for item in examples]}
            st.session_state["random_example"] = random.choice(st.session_state["file_json"]["examples"])
        else:
            st.session_state["file_json"] = None

        with file_upload_placeholder:
            file_json = st.file_uploader("Upload a JSON file", type=["json"])
            main_key_name = "text"
            entities_key_name = "entities"
            if file_json:
                data = json.load(file_json)
                data_keys = data[0].keys()

                with form_placeholder:
                    if main_key_name not in data_keys:
                        main_key_name = st.selectbox("Select the main key name", list(data_keys))

                    if entities_key_name not in data_keys:
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

    if st.session_state["file_json"]:
        with info_placeholder:
            ex = st.session_state["file_json"]["examples"][0:3]
            ent = st.session_state["file_json"]["entities"][0:3]
            st.write({"Examples": ex, "Entities": ent})


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
    aug12 = "Try to make the new document more complex than the original. Add more information"  # @param {type: "string"}

    default_augs = [aug1, aug2, aug3, aug4, aug5, aug6, aug7, aug8, aug9, aug10, aug11, aug12]
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

    # st.write({"Augmentations": user_augs})

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
    if "data_file" not in st.session_state or st.session_state["data_file"] is None:
        st.session_state["data_file"] = f"generated_data_{datetime.now().strftime('%Y-%m-%d_%H-%M')}.csv"

    examples = st.session_state["file_json"]["examples"]
    entities = st.session_state["file_json"]["entities"]

    with st.expander("Augmentations Settings"):
        augmentations = setup_augmentations()

    col1, col2 = st.columns((6, 1))

    with col1:
        st.text_area("Augmentations", value="\n".join(augmentations), height=200, max_chars=1000, disabled=True)

        # UI for generating synthetic data
        language = st.selectbox("Select language", LANGUAGES, index=0)
        data_size = st.slider("How many examples to generate",
                              min_value=1, value=4, max_value=10, step=1)
        gpt4_share = st.slider("GPT-4 share: select 0 for GPT-3.5 Turbo for all examples, 1 for GPT-4.0 for all",
                               min_value=0.0, max_value=1.0, value=0.5, step=0.1)

        # Default values
        save_every = 10  # st.number_input("Save every", min_value=1, value=10)
        data_file = st.session_state["data_file"]

    if st.button("Generate synthetic data"):
        st.info("Please wait while the data is being generated...")
        col1, col2 = st.columns((6, 1))
        with col2:
            status_placeholder = st.empty()
            progress = st.progress(0)

        with col1:
            with st.spinner("Generating synthetic data..."):
                for i in range(data_size):
                    with status_placeholder:
                        st.markdown(f"<p style='color: green;'>Generating example {i + 1} / {data_size}</p>",
                                    unsafe_allow_html=True)
                    progress.progress((i + 1) / data_size)
                    data = generate_synthetic_data_batch(examples,
                                                         1,
                                                         data_file,
                                                         gpt4_share,
                                                         save_every,
                                                         augmentations,
                                                         language)

                st.markdown(f"<p style='color: green;'>Data generated successfully with {data_size} examples.</p>",
                            unsafe_allow_html=True)

        st.success("Data generated successfully!")
        st.dataframe(data)

        st.download_button(
            label="Download data",
            data=data.to_csv(index=False),
            file_name=data_file,
            mime="text/csv"
        )
