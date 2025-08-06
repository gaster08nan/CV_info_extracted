from langgraph.graph import StateGraph, START, END
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from src.process_pdf import pdf_reader
from src.output_model.output_model import CVSchema
from src.process_image import image_processor
from typing import TypedDict, Optional
import json
import logging

logger = logging.getLogger(__file__)
load_dotenv(override=True)

EXTRACT_PROMPT_TEMPLATE = """
    You are an expert HR recruiter. Given a raw CV/resume text, extract the following fields:

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

    Return ONLY a valid JSON object in the following format:
    {format_instructions}

    CV TEXT:
    {cv_text}
    """

    
class CVState(TypedDict):
    cv_file: object
    cv_text: Optional[str]
    extracted_json: Optional[str]

class Workflow:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=0.1 ,
        )
        self.parser = JsonOutputParser()
        self.prompt = PromptTemplate(
            input_variables=["cv_text"],
            partial_variables={"format_instructions": self.parser.get_format_instructions()},
            template=EXTRACT_PROMPT_TEMPLATE
        )
        self.chain = self.prompt | self.llm | self.parser
        self.ocr_model = image_processor.define_model()
        self.workflow = self._build_workflow()
        
    def _build_workflow(self):
        graph = StateGraph(CVState)
        # Add nodes
        graph.add_node("read_pdf", self._read_pdf_node)
        graph.add_node("image_processor", self._process_image_node)
        graph.add_node("extract", self._extract_info_node)
        graph.add_node("modify_response", self._map_and_serialize_cv_data)

        # Flow
        graph.add_edge(START, "read_pdf")
        graph.add_conditional_edges("read_pdf", self._should_use_image, {
            "extract": "extract",
            "image_processor": "image_processor"
        })
        graph.add_edge("image_processor", "extract")
        graph.add_edge("extract", "modify_response")
        graph.add_edge("modify_response", END)

        # Build the app
        logger.log(msg="Build workflow successfull.", level=logging.INFO)
        return graph.compile()
        
    def _extract_cv_info(self, cv_text: str) -> dict:
            
        json_result  = self.chain.invoke({"cv_text": cv_text})
        
        json_data = json.dumps(json_result)
        return json_data
        
    def _read_pdf_node(self, state: CVState) -> CVState:
        text = pdf_reader.pdf_preprocess(state["cv_file"])
        return {**state, "cv_text": text}
    
    def _process_image_node(self, state: CVState) -> CVState:
        logger.log(msg="Using image processor instead", level=logging.INFO)
        text = image_processor.ocr_image(state["file_path"], model=self.ocr_model)
        return {**state, "cv_text": text}
    
    def _extract_info_node(self, state: CVState) -> CVState:
        response = self._extract_cv_info(state["cv_text"])
        # serialized = self.map_and_serialize_cv_data(response)
        return {**state, "extracted_json": response}

    def _should_use_image(self, state: CVState) -> str:
        text = state.get("cv_text", "")
        return "image_processor" if not text or text.strip() == "" else "extract"
    
    def _map_and_serialize_cv_data(self, state: CVState) -> str:
        """
        Maps the extracted CV data to the CVSchema and serializes it to JSON.
        
        Args:
            response (dict): The extracted data from the CV.
        
        Returns:
            str: The serialized JSON string of the mapped data.
        """
        
        # Convert graduation_year to str in Education
        response = json.loads(state["extracted_json"])
        email = response.get("Email", [])
        if email and isinstance(email, str):
            response["Email"] = email.strip()
        else:
            response["Email"] = 'sample_email@sample.com'
                
        for edu in response.get("Education", []):
            if "graduation_year" in edu and edu["graduation_year"] is not None:
                edu["graduation_year"] = str(edu["graduation_year"])

        # Convert years_worked to str in Experience
        for exp in response.get("Experience", []):
            if "years_worked" in exp and exp["years_worked"] is not None:
                exp["years_worked"] = str(exp["years_worked"])
        cv_data = CVSchema(**response)
        response =  cv_data.model_dump_json(indent=2)
        return {**state, "extracted_json": response}
    
    def run(self, cv_file: object) -> dict:
        """
        Run the workflow to extract information from a CV file.
        
        Args:
            cv_file (object): The uploaded CV file.
        
        Returns:
            dict: The extracted information in JSON format.
        """
        state = CVState(cv_file=cv_file, cv_text=None, extracted_json=None)
        result = self.workflow.invoke(state)
        
        return result