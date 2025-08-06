import streamlit as st
from src.wokrflow.workflow import Workflow
from src.validation.validator import ResultValidator

def main():
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
        else:
            st.warning("No data extracted from the CV.")
    
    def validate_cv():
        st.subheader("Validate CV")
        validate_result = ResultValidator.run_validation(result)
        if validate_result:
            st.success("CV validation completed successfully.")
        else:
            st.error("CV validation failed or no data to validate.")
    
    st.button("Validate CV", on_click=validate_cv())
    
if __name__ == "__main__":
    main()
