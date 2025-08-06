from langchain_google_genai import ChatGoogleGenerativeAI

from dotenv import load_dotenv
from src.wokrflow import workflow
from src.validation.validator import ResultValidator
import json

load_dotenv(override=True)

def main():

    workflow_instance = workflow.Workflow()
    cv_file_path = 'datasets/data/INFORMATION-TECHNOLOGY/10089434.pdf'
    result = workflow_instance.run(cv_file_path)
    
    json_result = json.loads(result["extracted_json"])
    cv_text = result["cv_text"]
    if not json_result:
        print("No data extracted from the CV.")
        return
    else:
        validator = ResultValidator(predict_result=json_result, cv_text=cv_text)
        print("Schema Validation:", validator.schema_validation())
        print("Email Validation:", validator.email_validation())
        print("Phone Validation:", validator.phone_validation())


if __name__ == "__main__":
    main()
