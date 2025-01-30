import streamlit
!pip install -q google-generativeai

import google.generativeai as genai 
import csv
import os

genai.configure(api_key="AIzaSyCLFuWZiNKwnScFFSplgAL_yhN3G2SOHzM")

defaults = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}
model = genai.GenerativeModel(
  model_name="gemini-2.0-flash-exp",
  generation_config=generation_config,
)

def generate_prompt(format_option):
        user_input = input("Enter your input: ")
        prompt = f"""input ({format_option}): {user_input}
        output:"""
        return prompt

def save_output_to_file(output, file_path):
    try:
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(output)
        print(f"Output saved to {file_path}")
    except Exception as e:
        print(f"Error saving output to {file_path}: {e}")


print("Choose a data format:")
print("1. CSV")
print("2. JSON")
print("3. TXT")

# Get user choice
format_choice = input("Enter the number of the desired format: ")

# Map user choice to format and file extension
format_mapping = {
    "1": {"format": "CSV", "extension": "csv"},
    "2": {"format": "JSON", "extension": "json"},
    "3": {"format": "TXT", "extension": "txt"},
}

selected_format = format_mapping.get(format_choice)

if selected_format:
    # Generate prompt based on the selected format
    prompt = generate_prompt(selected_format["format"])

    # Call your text generation function with the generated prompt
    response = model.generate_content(
        **defaults,
        prompt=prompt
    )

    # Get the generated result
    generated_result = response.result
    print("Generated Result:")
    print(generated_result)

    # Save the generated result to a file using the save_output_to_file function
    file_extension = selected_format["extension"]
    file_name = input("Enter the desired file name: ")
    file_path = f"{file_name}.{file_extension}"
    save_output_to_file(generated_result, file_path)
else:
    print("Invalid format choice. Please choose a valid format.")
