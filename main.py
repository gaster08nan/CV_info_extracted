from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langgraph.graph import StateGraph, START, END
from dotenv import load_dotenv
from src.process_pdf import pdf_reader
from src.validation.validator import ResultValidator
import json

load_dotenv(override=True)

def main():


    # Build the structured output parser
    parser = JsonOutputParser()

    # Define the prompt template
    extract_template = """
    You are an expert HR recruiter. Given a raw CV/resume text, extract the following fields:

    - Name: Full name of the candidate.
    - Email: Valid email address.
    - Phone: Phone number including country code if available.
    - Skills: List of technical and professional skills.
    - Education: List with degree, institution name, graduation year.
    - Experience: List of jobs with job title, company name, years worked, and short description.
    - Certification: List of certifications.
    - Languages: Languages the candidate can speak or write. If not mentioned, return the language used in the CV.

    Return ONLY a valid JSON object in the following format:
    {format_instructions}

    CV TEXT:
    {cv_text}
    """

    prompt = PromptTemplate(
        input_variables=["cv_text"],
        partial_variables={"format_instructions": parser.get_format_instructions()},
        template=extract_template
    )

    # Initialize Gemini LLM via LangChain
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0.3 ,
    )
    # Chain the prompt and parser
    chain = prompt | llm | parser
    
    cv_text = pdf_reader.extract_text_from_pdf("datasets/data/INFORMATION-TECHNOLOGY/16186411.pdf")
    
    json_result  = chain.invoke({"cv_text": cv_text})
    
    print(json_result)
    
    json_data = json.dumps(json_result)
    with open("output.json", "w") as f:
        f.write(json_data)
        
    validator = ResultValidator(predict_result=json_result, cv_text=cv_text)
    print("Schema Validation:", validator.schema_validation())
    print("Email Validation:", validator.email_validation())
    print("Phone Validation:", validator.phone_validation())
    print("LLM Validation:", validator.validate_by_llm())


if __name__ == "__main__":
    main()
