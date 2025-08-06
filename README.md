# CV Extraction Chatbot

This project is a CV Extraction Chatbot that uses a combination of large language models (LLMs) and optical character recognition (OCR) to extract structured information from resumes and CVs.
LLM model: Google Gemini
OCR model: DocTR

## Features

*   **PDF and Image Processing:** The chatbot can process both text-based PDFs and images of CVs.
*   **Information Extraction:** Extracts key information such as name, email, phone number, skills, education, and work experience.
*   **JSON Output:** The extracted information is returned in a structured JSON format.
*   **Validation:** The extracted data is validated to ensure accuracy and consistency.
*   **Extensible Workflow:** The project uses a graph-based workflow that can be easily extended to include new processing steps.

## Validate result

* **Check valid email and phone numbers:**: Check the format of extracted email and phone numbers information.
* **Validate missing and incorrect infomation:** Using LLM as a Judge to evaluate the results. Point out missing or incorrect information.

## Limitation:

* **Inconsistent results:** The model sometimes misses key information when extracting from long text fields such as description.
* **Lack of basic reasoning:** The model cannot infer basic information to fill in missing fields. For example, if a CV does not mention languages, it should attempt to detect them from the CV content or past projects. Similarly, it should extract relevant skills from projects even if they are not explicitly listed in the Skills field.

## Further improvements:

* **Better OCR model:** Fine-tune the OCR model for a better results.
* **Batch processing:** Process the PDF in batches to reduces the cost and waiting time.
* **Adopt Feedback:** Improve the extracted information by using feedbacks from another LLM.
* **Self-host LLM model (Optional):** Use a self-hosted LLM to gain independence from an LLM provider. This might increase costs or slightly reduce accuracy. However, it provides more clarity and ensures data privacy.

## Expected Output
```json
{   "Name":"Huynh Duc Thang",
    "Email":"huynhthang1108@gmail.com",
    "Phone":"+84988232749",
    "Skills":
        ["Python","Pytorch","Tensorflow","Keras","Unsloth","PEFT","LangChain","vLLM","Transformers","PineCone","ChromaDB","AWS","Azure","FastAPI","TensorRT","Docker","Numpy","Pandas","nltk","Legal research and writing","Computer Vision","Natural Language Processing (NLP)","Large Language Models (LLMs)","Image Generation"],
    "Education":
        [
            {
                "degree":"Bachelor Degree in Information Technology",
                "institution":"Ho Chi Minh City of Technology (Hutech)",
                "graduation_year":null},{"degree":"Master Degree in Artificial Inteligent",
                "institution":"Ho Chi Minh University of Science (HCMUS)",
                "graduation_year":null
            }
        ],
    "Experience":
        [   {
                "job_title":"Machine Learning Engineer",
                "company_name":"Moreh VietNam",
                "years_worked":"1 year 10 months",
                "description":"Deploy automation training scripts for various Hugging Face models. Training and fine-tuning model. Quantization model weights. Enhance the performance of diffusion-based models 20% faster. Visualize tensors flow of Stable Diffusion model architectures (SD3, SDXL)."
            },
            {
                "job_title":"AI Engineer",
                "company_name":"QAI, FPT Software",
                "years_worked":"1 year 6 months",
                "description":"Utilized the RASA NLU model to extract the product information in Vietnamese. Deployed models to Azure virtual machine and developed API to interact with the model."
            }
        ],
    "Certification":["TOEIC 895 (2021)"],
    "Languages":["English"]}
```

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
streamlit run main.py
```

This will run the UI on local host with port 8501, allow to upload and pdf file and extract the information.

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
