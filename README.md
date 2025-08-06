# CV Extraction Chatbot

This project is a CV Extraction Chatbot that uses a combination of large language models (LLMs) and optical character recognition (OCR) to extract structured information from resumes and CVs.

## Features

*   **PDF and Image Processing:** The chatbot can process both text-based PDFs and images of CVs.
*   **Information Extraction:** Extracts key information such as name, email, phone number, skills, education, and work experience.
*   **JSON Output:** The extracted information is returned in a structured JSON format.
*   **Validation:** The extracted data is validated to ensure accuracy and consistency.
*   **Extensible Workflow:** The project uses a graph-based workflow that can be easily extended to include new processing steps.

## Getting Started

### Prerequisites

*   Python 3.10+
*   [Poetry](https://python-poetry.org/) for dependency management.

### Installation

1.  Clone the repository:
    ```bash
    git clone https://github.com/gaster08nan/CV_info_extracted.git
    ```
2. Install the dependencies:
    ```bash
    poetry install
    ```
    or:
    ```bash
    pip install -r requirements.txt
    ```
3.  Create a `.env` file in the root directory and add your Google API key:
    ```
    GOOGLE_API_KEY="your-api-key"
    ```

### Usage

To run the chatbot, you can use the following command:

```bash
python main.py
```

This will process the sample CV located in `datasets/data/INFORMATION-TECHNOLOGY/10089434.pdf` and print the extracted information to the console.

## Project Structure

```
.
├── datasets
│   └── data
│       └── INFORMATION-TECHNOLOGY
├── src
│   ├── output_model
│   ├── process_image
│   ├── process_pdf
│   ├── validation
│   └── wokrflow
├── .gitignore
├── main.py
├── output.json
├── poetry.lock
├── pyproject.toml
└── README.md
```

*   **`datasets`**: Contains the sample CVs used for testing and development.
*   **`src`**: Contains the source code for the chatbot.
    *   **`output_model`**: Defines the data model for the extracted information.
    *   **`process_image`**: Handles the OCR processing of image-based CVs.
    *   **`process_pdf`**: Handles the text extraction from PDF-based CVs.
    *   **`validation`**: Validates the extracted information.
    *   **`wokrflow`**: Defines the main workflow for processing CVs.
*   **`main.py`**: The main entry point for the application.
*   **`output.json`**: An example of the JSON output produced by the chatbot.
*   **`poetry.lock`**: The dependency lock file.
*   **`pyproject.toml`**: The project configuration file.

## Technologies Used

*   [LangChain](https://python.langchain.com/v0.2/docs/introduction/)
*   [Google Gemini](https://deepmind.google/technologies/gemini/)
*   [LangGraph](https://langchain-ai.github.io/langgraph/)
*   [Pydantic](https://docs.pydantic.dev/)
*   [PyMuPDF](https://pymupdf.readthedocs.io/en/latest/)
*   [DocTR](https://mindee.github.io/doctr/)

## Contributing

Contributions are welcome! Please feel free to open an issue or submit a pull request.
