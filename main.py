import os
import google.generativeai as genai
import pandas as pd
import json
import streamlit as st
from io import StringIO


# API Key setup for Google Generative AI
import google.generativeai as genai

# Directly assign the API key (for testing purposes only)
genai.configure(api_key="AIzaSyCLFuWZiNKwnScFFSplgAL_yhN3G2SOHzM")

# Default generation configuration
defaults = {
  'model': 'models/text-bison-001',
  'temperature': 0.7,
  'candidate_count': 1,
  'top_k': 40,
  'top_p': 0.95,
  'max_output_tokens': 1024,
  'stop_sequences': [],
  'safety_settings': [
    {"category": "HARM_CATEGORY_DEROGATORY", "threshold": "BLOCK_LOW_AND_ABOVE"},
    {"category": "HARM_CATEGORY_TOXICITY", "threshold": "BLOCK_LOW_AND_ABOVE"},
    {"category": "HARM_CATEGORY_VIOLENCE", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUAL", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_MEDICAL", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
  ],
}

def generate_prompt(format_option, user_input):
    """Construct the prompt based on format and user input."""
    return f"input ({format_option}): {user_input}\noutput:"

def save_output_to_file(output, file_path):
    """Save the generated content to a file."""
    try:
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(output)
        st.success(f"Output saved to {file_path}")
    except Exception as e:
        st.error(f"Error saving output to {file_path}: {e}")

def convert_df(df):
    """Convert DataFrame to CSV for downloading."""
    return df.to_csv().encode('utf-8')

def main():
    st.title("Text Generation Streamlit App")

    # Sidebar for user input
    st.sidebar.header("User Input")
    
    # Format choice
    format_option = st.sidebar.selectbox("Choose a data format:", ["CSV", "JSON", "TXT"])
    
    # User input
    user_input = st.sidebar.text_input("Enter your input:")

    # Submit button
    if st.sidebar.button("Submit"):
        # Generate the prompt based on format and input
        prompt = generate_prompt(format_option, user_input)

        # Generate text from the AI model
        try:
            response = genai.generate_text(
                **defaults,
                prompt=prompt
            )
            generated_result = response.result
            st.header("Generated Result:")
            
            if format_option == "CSV":
                # Process CSV formatted result
                df = pd.read_csv(StringIO(generated_result), sep="|", skipinitialspace=True)
                df.columns = df.columns.str.strip()  # Clean column names
                df = df.loc[:, ~df.columns.str.contains('Unnamed')]  # Remove unnamed columns

                st.table(df)

                # Provide option to download CSV
                csv = convert_df(df)
                st.sidebar.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name="generated_data.csv",
                    mime="text/csv"
                )

            elif format_option == "JSON":
                # Parse JSON and display it
                json_content = generated_result.replace('```json', '').replace('```', '').strip()
                try:
                    st.json(json.loads(json_content), expanded=True)
                except json.JSONDecodeError as e:
                    st.write("Invalid JSON syntax:", e)
                    st.write("Original content:")
                    st.write(generated_result)

                # Provide option to download JSON
                st.sidebar.download_button(
                    label="Download JSON",
                    data=generated_result,
                    file_name="generated_data.json",
                    mime="application/json"
                )

            elif format_option == "TXT":
                st.write(generated_result)

                # Provide option to download TXT
                st.sidebar.download_button(
                    label="Download TXT",
                    data=generated_result,
                    file_name="generated_data.txt",
                    mime="text/plain"
                )

        except Exception as e:
            st.error(f"Error generating text: {e}")

if __name__ == "__main__":
    main()
