import os
import google.generativeai as genai
import json

# Konfigurasi API Key
GEMINI_API_KEY = os.getenv("AIzaSyCliDeFpsIaE8yfin9MJWSWgoV8zxMMgDE")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is not set. Please set it as an environment variable.")

genai.configure(api_key=GEMINI_API_KEY)

# Konfigurasi model
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 1024,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-2.0-flash-exp",
    generation_config=generation_config,
)

def generate_prompt(format_option):
    """Membuat prompt berdasarkan format pilihan pengguna."""
    user_input = input("Enter your input: ")
    return f"input ({format_option}): {user_input}\noutput:"

def save_output_to_file(output, file_path):
    """Menyimpan output ke file."""
    try:
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(output)
        print(f"Output saved to {file_path}")
    except Exception as e:
        print(f"Error saving output to {file_path}: {e}")

# Pilihan format data
format_mapping = {
    "1": {"format": "CSV", "extension": "csv"},
    "2": {"format": "JSON", "extension": "json"},
    "3": {"format": "TXT", "extension": "txt"},
}

# Tampilkan pilihan format
print("Choose a data format:")
for key, value in format_mapping.items():
    print(f"{key}. {value['format']}")

# Pilihan pengguna
format_choice = input("Enter the number of the desired format: ")
selected_format = format_mapping.get(format_choice)

if selected_format:
    # Buat prompt berdasarkan pilihan format
    prompt = generate_prompt(selected_format["format"])

    try:
        # Generate text dari model AI
        response = model.generate_content(prompt)
        generated_result = response.text  # Ambil teks hasil AI
        
        print("\nGenerated Result:")
        print(generated_result)

        # Simpan ke file
        file_name = input("Enter the desired file name: ")
        file_path = f"{file_name}.{selected_format['extension']}"
        save_output_to_file(generated_result, file_path)

    except Exception as e:
        print(f"Error generating text: {e}")
else:
    print("Invalid format choice. Please choose a valid format.")
