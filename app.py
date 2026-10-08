import streamlit as st
import google.generativeai as genai

# --- Page Configuration ---
st.set_page_config(page_title="IELTS Evaluator", page_icon="📝", layout="centered")

st.title("📝 Cambridge IELTS Club Writing Evaluator")

st.markdown("Evaluate your IELTS Task 1 and Task 2 against official public band descriptors.")

# --- Sidebar / Configuration ---
st.sidebar.header("Configuration")
st.sidebar.markdown("This app uses Google's free Gemini API.")
api_key = st.sidebar.text_input("Enter Gemini API Key", type="password")
st.sidebar.markdown("[Get a free API key here](https://aistudio.google.com/app/apikey)")

# --- Main Interface ---
task_type = st.selectbox(
    "Select Task Type", 
    ["Task 1 (Academic - Graph/Chart)", "Task 1 (General - Letter)", "Task 2 (Essay)"]
)
question = st.text_area(
    "Prompt / Question (Highly Recommended):", 
    height=100, 
    placeholder="Paste the exact IELTS prompt you are responding to here..."
)
response_text = st.text_area(
    "Your Response:", 
    height=300, 
    placeholder="Paste your essay or report here..."
)

# --- Evaluation Engine ---
if st.button("Evaluate Writing", type="primary"):
    if not api_key:
        st.error("Please enter your Gemini API Key in the sidebar.")
    elif len(response_text.split()) < 50:
        st.warning("Please enter a valid response (minimum 50 words).")
    else:
        with st.spinner("Evaluating against IELTS public band descriptors..."):
            try:
                # Configure the API
                genai.configure(api_key=api_key)
                
                # Hardcoded strictly to the required gemini-3.8-flash model
                model = genai.GenerativeModel('gemini-3.8-flash')
                
                # The strict IELTS Examiner Prompt
                prompt = f"""
                You are an expert, strict IELTS examiner. Evaluate the following IELTS {task_type} based strictly on the official IELTS public writing band descriptors.
                
                Question/Prompt: {question}
                Candidate's Response: {response_text}
                
                Provide your evaluation formatted in Markdown exactly as follows:
                
                ### 1. Task Achievement / Task Response (TA/TR): [Band Score]
                - **Feedback:** [Provide 2-3 specific sentences referencing the rubric, e.g., overview clarity, argument development, or word count].
                
                ### 2. Coherence and Cohesion (CC): [Band Score]
                - **Feedback:** [Provide 2-3 specific sentences regarding paragraphing, linking devices, and logical flow].
                
                ### 3. Lexical Resource (LR): [Band Score]
                - **Feedback:** [Provide 2-3 specific sentences regarding vocabulary range, precision, collocations, and spelling errors].
                
                ### 4. Grammatical Range and Accuracy (GRA): [Band Score]
                - **Feedback:** [Provide 2-3 specific sentences regarding sentence structures, complexity, and punctuation/grammar errors].
                
                ---
                ### 🎯 Overall Band Score: [Score]
                *Calculation Rule: Calculate the exact average of the 4 criteria. Apply official IELTS rounding rules (e.g., 6.25 rounds up to 6.5; 6.75 rounds up to 7.0; 6.125 rounds down to 6.0).*
                
                ### 🛠️ Key Corrections & Suggestions:
                Provide a bulleted list of 3 to 5 specific grammatical corrections, better vocabulary alternatives, or structural improvements based directly on quotes from the candidate's text.
                """
                
                # Call the API and display the result
                response = model.generate_content(prompt)
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"An error occurred: {e}")
                
