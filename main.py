import streamlit as st
from src.wokrflow.workflow import Workflow
from src.validation.validator import ResultValidator

def main():
    
    def validate_cv(result):
        st.subheader("Validate CV")
        validator = ResultValidator(result["extracted_json"], result["cv_text"])
        validate_result, message = validator.run_validation()
        if validate_result:
            st.success(message)
        else:
            st.error(message)
    
    st.title("CV Extraction Chatbot")

    uploaded_file = st.file_uploader("Upload a CV (PDF)", type="pdf")

    if uploaded_file is not None:
        st.success(f"File uploaded successfully: {uploaded_file.name}")

        # Run the workflow
        with st.spinner("Extracting information from the CV..."):
            try:
                workflow = Workflow()
                result = workflow.run(uploaded_file)
            except Exception as e:
                st.error(f"An error occurred: {e}")
                result = None
        st.header("Extracted Information")
        if result and "extracted_json" in result:
            extracted_data = result["extracted_json"]
            st.json(extracted_data)
            
        if st.button("Validate CV"):
            validate_cv(result)
                
    else:
        st.warning("No data extracted from the CV.")

    
if __name__ == "__main__":
    main()
