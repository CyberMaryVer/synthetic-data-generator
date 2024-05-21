[//]: # (# Project: streamlit app)
[//]: # (# File: readme.md)
[//]: # (# Created Date: 2024-05-21 11:00:00 pm)

[![MIT License][license-shield]][license-url]


<!-- ABOUT THE PROJECT -->
## About The Project

### Demo Page
[![Demo][Demo]][demo-url]

This app allows to generate synthetic data for the task of NER. 
With the UI you can create your own dataset with the entities you need.
The app uses LangChain library to generate the data.
You can choose the LLM API you want to use.

You can define the following parameters:
* Number of samples
* Entities and their descriptions
* Augmentation techniques
* LLM API

The app will generate the data based on the provided examples and show it in the table. 

Examles can be loaded from the file or added manually.

You can download the data in the csv format.

<p align="right">(<a href="#readme-top">back to top</a>)</p>


### Built With

Major frameworks/libraries used in the project. 

* [![Streamlit][Streamlit]][Streamlit-url]
* [![Langchain][Langchain]][Langchain-url]
* [![Snowflake][Snowflake]][Snowflake-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running follow these simple example steps.

### Installation

* requirements
  ```sh
  pip install -r requirements.txt
  ```
* streamlit app
* ```sh
  streamlit run app.py
  ```

<!-- USAGE EXAMPLES -->
## Usage

Now you can open the app in your browser by typing `localhost:8501` in the address bar.



<!-- LICENSE -->
## License

Distributed under the APACHE License. See `LICENSE.txt` for more information.




<!-- CONTACT -->
## Contact
[![Maria][Linkedin]](https://www.linkedin.com/in/maria-startseva/)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[license-shield]: https://img.shields.io/badge/License-APACHE-yellow.svg?style=for-the-badge
[license-url]: https://github.com/CyberMaryVer/ad_labelling/blob/main/LICENSE.txt
[Streamlit]: https://img.shields.io/badge/Streamlit-1.21-red?style=for-the-badge&logo=streamlit&logoColor=white
[Streamlit-url]: https://streamlit.io/
[Langchain]: https://img.shields.io/badge/LangChain-1.01-FF0000?style=for-the-badge&logo=fastapi&logoColor=white
[Langchain-url]: https://python.langchain.com/docs/get_started/introduction
[Linkedin]: https://img.shields.io/badge/Linkedin-0077B5?style=for-the-badge&logo=linkedin&logoColor=white
[Snowflake]: https://img.shields.io/badge/Snowflake-1.00-FF0000?style=for-the-badge&logo=snowflake&logoColor=white
[Snowflake-url]: https://www.snowflake.com/en/

[Demo]: https://img.shields.io/badge/Demo-0077B5?style=for-the-badge&logo=github&logoColor=white
[demo-url]: https://synthetic-data-llm-generator.streamlit.app/
