import os
import json
import random
import openai
import streamlit as st
import pandas as pd
import numpy as np
from openai import OpenAI
from tqdm import tqdm
from time import time

DEFAULT_AUGMENTATIONS = [
    "Add more information about the topic.",
    "Add more details",
    "Add more statistics",
    "Add more facts",
    "Add more references",
    "Add more quotes",
    "Add more sources",
]

LANGUAGES = {
    "RU": "RUSSIAN",
    "EN": "ENGLISH",
    "DE": "GERMAN",
    "FR": "FRENCH",
    "ES": "SPANISH",
    "IT": "ITALIAN",
    "PT": "PORTUGUESE",
    "NL": "DUTCH",
    "PL": "POLISH",
    "TR": "TURKISH",
}


def set_openai_api_key(from_secrets: bool = True, from_env: bool = True):
    if from_secrets:
        try:
            openai.api_key = st.secrets["OPENAI_API_KEY"]  # @param {type: "string"}
        except Exception as e:
            openai.api_key = None
            print(f"\033[091mError: {e}\033[0m")
    if from_env and not openai.api_key:
        openai.api_key = os.getenv("OPENAI_API_KEY")  # @param {type: "string"}
    if not openai.api_key:
        raise ValueError("OpenAI API key is not set. Please set the 'OPENAI_API_KEY' environment variable.")
    return openai.api_key


def check_available_models(model_id: str = "gpt-4", print_all: bool = False):
    available_models = openai.models.list()
    model_id_available = any(model.id == model_id for model in available_models.data)

    if model_id_available:
        print(f"\033[092m{model_id} is available for use.\033[0m")
    else:
        print(f"\033[091m{model_id} is not available for use.\033[0m")

    if print_all:
        print("\n\033[096mAvailable models: \033[0m")
        for model in available_models.data:
            print(model.id)


def get_client(api_key: str = None):
    if api_key:
        openai.api_key = api_key
    else:
        set_openai_api_key(from_secrets=True, from_env=True)
    return OpenAI(api_key=openai.api_key)


def generate_synthetic_data(
        template: str,
        api_key: str = None,
        model: str = "gpt-4o",
        use_random_augmentation: bool = True,
        augmentations: list = None,
        language: str = "RU"
):
    # @markdown ## ▶️ Initialize openai functions
    client = get_client(api_key=api_key)
    augmentations = DEFAULT_AUGMENTATIONS if not augmentations else augmentations
    augmentation = random.choice(augmentations) if use_random_augmentation else ''
    language = LANGUAGES.get(language, "RUSSIAN")
    prompt = f"""
    TASK:
    Generate a new document from the given template. Use the similar structure. Change all the personal data (name, phone, email), dates, organizations, urls and numbers to generated data.
    - Generated data should be similar to real. Do not use numbers like this: 'phone 555-555-555' or very general names like 'Ivanov'. Use various names, surnames, etc.
    - The main language of the new document is {language}. Translate all the text to the {language} if needed.
    - Try to make the new document more complex than the original. Add more information.
    {augmentation} in the final document, this should look natural.

    TEMPLATE:
    {template}

    NEW_DOCUMENT:
    """
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": f"You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ]
    )
    return process_result(response), augmentation


def process_result(response):
    result = response.json()
    result = json.loads(result)
    return result['choices'][0]['message']['content']


def test_generation(use_index: int | None = None,
                    model: str = "gpt-4o",
                    examples: list = None):
    random_examples = [
        "my name is John Doe. I live in New York. My phone number is 555-555-5555. My email is john-john.jj@jon.com",
        "I am a student. I study at the University of New York. My name is Victor.",
        "This company is the best. We have the best products. Our website is www.bestproducts.com",
        "Send the parcel to DigitalOcean, 101 Avenue of the Americas, New York, NY 10013, USA."
    ]

    if not examples:
        examples = random_examples
    random_index = random.randint(0, len(examples) - 1)
    index_to_use = min(use_index, len(examples) - 1) if use_index else random_index
    original_text = examples[index_to_use]

    print(f"\033[090mOriginal Text:\n", original_text, "\033[0m\n")
    print("-" * 50)

    new_document, aug = generate_synthetic_data(original_text, model=model)
    print(f"\033[095mRandom Index: {random_index} | Augmentation: {aug}\033[0m\n")
    print(new_document)
    return new_document


def generate_synthetic_data_batch(
        examples: list,
        data_size: int = 200,
        data_file: str = "generated_data.csv",
        gpt4_share: float = 0.5,
        save_every: int = 10,
        augmentations: list = None,
        language: str = "RU"
):
    augmentations = DEFAULT_AUGMENTATIONS if not augmentations else augmentations
    language = language.upper()

    # Create csv for a new dataset or append to the existing one
    data_folder = os.path.join(os.getcwd(), "gen_data")
    if not os.path.exists(data_folder):
        os.makedirs(data_folder)
    generated_file = os.path.join(data_folder, data_file)
    if os.path.exists(generated_file):
        generated_data = pd.read_csv(generated_file)
    else:
        generated_data = pd.DataFrame(columns=['original_index',
                                               'original_text',
                                               'new_document',
                                               'augmentation',
                                               'model'])

    def pretty_print(iteration, data_size, augmentation, model, elapsed_time):
        iteration_str = f"\033[095mIteration {iteration:03d} / {data_size}\033[0m"
        augmentation_str = f"\033[096mAugmentation: {augmentation}\033[0m"
        model_str = f"\033[090mModel: {model}\033[0m"
        time_str = f"\033[090m{elapsed_time:.2f} seconds\033[0m"
        print(f"{iteration_str} | {augmentation_str} | {model_str} | {time_str}")

    # Create new datapoints

    for i in tqdm(range(data_size)):
        start_time = time()
        random_index = random.randint(0, len(examples) - 1)
        random_model = np.random.choice(["gpt-3.5-turbo", "gpt-4o"],
                                        p=[1 - gpt4_share, gpt4_share])
        original_text = examples[random_index]
        new_document, augmentation = generate_synthetic_data(
            original_text,
            model=random_model,
            augmentations=augmentations,
            language=language
        )
        generated_data = pd.concat([generated_data,
                                    pd.DataFrame({'original_index': [random_index],
                                                  'original_text': [original_text],
                                                  'new_document': [new_document],
                                                  'augmentation': [augmentation],
                                                  'model': [random_model]})],
                                   ignore_index=True)
        pretty_print(i, data_size, augmentation, random_model, time() - start_time)

        # save data each N iterations
        if i % save_every == 0:
            generated_data.to_csv(generated_file, index=False)

    generated_data.to_csv(generated_file, index=False)
    return generated_data


if __name__ == "__main__":
    from dotenv import load_dotenv

    # Set root directory to the parent-parent directory of the current file
    ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    load_dotenv(os.path.join(ROOT_DIR, ".env"))

    set_openai_api_key(from_secrets=False, from_env=True)
    check_available_models(model_id="gpt-4o", print_all=False)

    # Test the generation
    test = test_generation(use_index=0)
    print(test)
