from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from src.output_model.output_model import CVSchema, ValidationError
import re
import json
import logging

logger = logging.getLogger(__file__)

class ResultValidator:
    def __init__(self, predict_result, cv_text):
        self.predict_result = json.loads(predict_result)
        self.cv_text = cv_text
    
    def email_validation(self) -> bool:
        if self.predict_result.get("Email") is None:
            logger.error("Email is missing")
            return False
        
        email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if re.match(email_pattern, self.predict_result.get("Email", "")):
            return True
        else:
            logger.error("Invalid Email Format")
            return False
        
    def phone_validation(self) -> bool:
        if self.predict_result.get("Phone") is None:
            logger.error("Phone number is missing")
            return False
        
        phone_pattern = r"^\+?[1-9]\d{1,14}$"
        if re.match(phone_pattern, self.predict_result.get("Phone", "")):
            return True
        else:
            logger.error("Invalid Phone Format")
            return False
    
    def validate_by_llm(self) -> bool:
        extract_template = """
        You are an expert HR recruiter. Given a raw CV/resume text, and an JSON object with extracted fields, analyze any field appears to be incorrect or missing.
        If any field is incorrect or missing information, return as False, and point out missing and incorrect information. Otherwise return True, and no further information.
        The extracted JSON object should contain the following fields:
        - Name: Full name of the candidate.
        - Email: Valid email address.
        - Phone: Phone number including country code if available.
        - Skills: List of technical and professional skills. Is a list of strings.
        - Education: List with degree, institution name, graduation year. Wihh the format:
        -- 'degree': degree name (e.g., Bachelor of Science in Computer Science)
        -- 'institution': institution name (e.g., University of Technology) if not mentioned, return None.
        -- 'graduation_year': graduation year (e.g., 2020). If graduation year is not mentioned, return None.
        - Experience: List of jobs with job title, company name, years worked, and short description. With the format:
        -- 'job_title': job title (e.g., Software Engineer)
        -- 'company_name': company name (e.g., Tech Solutions Inc.)
        -- 'years_worked': years worked (e.g., 2 years). If years worked is not mentioned, return None.
        -- 'description': short description of the job (e.g., Developed web applications using Python and JavaScript). If description is not mentioned, return None.
        - Certification: List of certifications. With the format: 'Certification Name (Year)'. If year is not mentioned, return only the certification name.
        - Languages: Languages the candidate can speak or write. If not mentioned, return the language used in the CV, always return as a list.

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
        logger.error("LLM Validation Result:", result.content)
        return True if result.content.lower() == "true" else False, result.content
    
    def run_validation(self) -> bool:
        """
        Run all validation checks on the extracted CV data.
        
        Returns:
            bool: True if all validations pass, False otherwise.
        """
        if not self.email_validation():
            return False, "Email validation failed"
        if not self.phone_validation():
            return False,  "Phone validation failed"
        llm_val_result, msg = self.validate_by_llm()
        if not llm_val_result:
            return False,  msg
        
        return True, "All validations passed successfully"