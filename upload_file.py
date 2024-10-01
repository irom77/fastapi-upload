import requests
import sys
import os

# API endpoint and API key
url = "http://127.0.0.1:8000/upload-file/"  # Adjust the endpoint if necessary
api_key = "abc"  # Replace with the actual API key

# Check if a file path is passed as an argument
if len(sys.argv) < 2:
    print("Usage: python upload_file.py <file_path>")
    sys.exit(1)

# File path to upload
file_path = sys.argv[1]

# Check if the file exists
if not os.path.isfile(file_path):
    print(f"File '{file_path}' does not exist.")
    sys.exit(1)

# Determine the file type (CSV or JSON)
file_extension = os.path.splitext(file_path)[1].lower()

if file_extension == ".csv":
    content_type = "text/csv"
elif file_extension == ".json":
    content_type = "application/json"
else:
    print(f"Unsupported file type: {file_extension}. Only CSV and JSON are supported.")
    sys.exit(1)

# Open the file and upload it
with open(file_path, "rb") as file:
    files = {"file": (os.path.basename(file_path), file, content_type)}
    headers = {"X-API-KEY": api_key}

    response = requests.post(url, headers=headers, files=files)

    # Check if the upload was successful
    if response.status_code == 200:
        print("File uploaded successfully.")
        print("Response:", response.json())
    else:
        print(f"Failed to upload file. Status code: {response.status_code}")
        print("Response:", response.text)
