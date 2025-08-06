from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from src.output_model.output_model import CVSchema, ValidationError
import re

class ResultValidator:
    def __init__(self, predict_result, cv_text):
        self.predict_result = predict_result
        self.cv_text = cv_text

    def schema_validation(self) -> bool:
        try:
            CVSchema(**self.predict_result)
            return True
        except ValidationError as e:
            print("Validation Error:", e)
            return False
    
    def email_validation(self) -> bool:
        if self.predict_result.get("Email") is None:
            print("Email is missing")
            return False
        
        email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if re.match(email_pattern, self.predict_result.get("Email", "")):
            return True
        else:
            print("Invalid Email Format")
            return False
        
    def phone_validation(self) -> bool:
        if self.predict_result.get("Phone") is None:
            print("Phone number is missing")
            return False
        
        phone_pattern = r"^\+?[1-9]\d{1,14}$"
        if re.match(phone_pattern, self.predict_result.get("Phone", "")):
            return True
        else:
            print("Invalid Phone Format")
            return False
    
    def validate_by_llm(self) -> bool:
        extract_template = """
        You are an expert HR recruiter. Given a raw CV/resume text, and an JSON object with extracted fields, analyze any field appears to be incorrect or missing.
        If any field is incorrect or missing information, return as False, and point out missing and incorrect information. Otherwise return True, and no further information.

        raw CV/resume text:
        {raw_cv_text}

        Extracted CV TEXT:
        {cv_text}
        """

        prompt = PromptTemplate(
            input_variables=["cv_text", "raw_cv_text"],
            template=extract_template
        )

        # Initialize Gemini LLM via LangChain
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=0.3,
        )
        # Chain the prompt and parser
        chain = prompt | llm
        result = chain.invoke({"raw_cv_text": self.cv_text, "cv_text": self.predict_result})
        print("LLM Validation Result:", result.content)
        return True if result.content.lower() == "true" else False
    