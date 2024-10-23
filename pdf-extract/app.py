import uuid
from flask import Flask, request, jsonify, render_template
import os
from ocr_module import extract_text_from_pdf
from tempfile import NamedTemporaryFile


app = Flask(__name__)

# A simple dictionary to store API keys
api_keys = {}

def generate_api_key():
    return str(uuid.uuid4())

# Generate a new API key and store it (you would normally do this in a setup script or admin interface)
new_api_key = generate_api_key()
api_keys[new_api_key] = "active"
print(f"Generated API Key: {new_api_key}")


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        response_format = request.form['format']
        api_key = request.form.get('api_key', None)

        if api_key not in api_keys or api_keys[api_key] != "active":
            return jsonify({"error": "Invalid API key"}), 403

        extracted_text = extract_text_from_pdf(file)

        if response_format == 'json':
            return jsonify({"data": extracted_text})
        elif response_format == 'xml':
            return f"<data>{extracted_text}</data>"
        else:
            return extracted_text

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)




'''
import uuid
from flask import Flask, request, jsonify, render_template
import fitz  # PyMuPDF library for PDF handling
import os
from tempfile import NamedTemporaryFile

app = Flask(__name__)

# A simple dictionary to store API keys
api_keys = {}

def generate_api_key():
    return str(uuid.uuid4())

# Generate a new API key and store it (you would normally do this in a setup script or admin interface)
new_api_key = generate_api_key()
api_keys[new_api_key] = "active"
print(f"Generated API Key: {new_api_key}")


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Check for the file and format parameters in form-data
        if 'file' not in request.files or 'format' not in request.form:
            return jsonify({"error": "Missing file or format parameter"}), 400
        
        file = request.files['file']
        response_format = request.form['format']
        api_key = request.form.get('api_key', '')  # Use .get() to avoid KeyError
        
        result = extract_data_from_pdf(file, response_format, api_key)
        return result

    # Render the initial form if GET request
    return render_template('index.html')



def extract_data_from_pdf(file, response_format, api_key):
    # Check if the API key is valid
    if api_key not in api_keys or api_keys[api_key] != "active":
        return jsonify({"error": "Invalid API key"}), 403

    # Save the uploaded file to a temporary location
    temp_file = NamedTemporaryFile(delete=False)
    file.save(temp_file.name)
    temp_file.close()

    # Read the PDF file and extract text
    doc = fitz.open(temp_file.name)
    extracted_text = ""
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        extracted_text += page.get_text()

    # Close and remove the temporary file
    doc.close()
    os.unlink(temp_file.name)

    # Return the extracted text based on the response format
    if response_format == 'json':
        return jsonify({"data": extracted_text})
    else:
        return extracted_text


def extract_data_from_pdf(file, response_format, api_key):
    # Check if the API key is valid
    if api_key not in api_keys or api_keys[api_key] != "active":
        return jsonify({"error": "Invalid API key"}), 403

    # Read the PDF file and extract text
    doc = fitz.open(file)
    extracted_text = ""
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        extracted_text += page.get_text()

    # Close the document
    doc.close()

    # Return the extracted text based on the response format
    if response_format == 'json':
        return jsonify({"data": extracted_text})
    else:
        return extracted_text

if __name__ == '__main__':
    app.run(debug=True)


import uuid
import requests
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# A simple dictionary to store API keys
api_keys = {}

def generate_api_key():
    return str(uuid.uuid4())

# Generate a new API key and store it (you would normally do this in a setup script or admin interface)
new_api_key = generate_api_key()
api_keys[new_api_key] = "active"
print(f"Generated API Key: {new_api_key}")

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        file = request.files['file']
        response_format = request.form['format']
        api_key = request.form['api_key']
        result = extract_data_from_pdf(file, response_format, api_key)
    return render_template('index.html', result=result)

def extract_data_from_pdf(file, response_format, api_key):
    # Check if the API key is valid
    if api_key not in api_keys or api_keys[api_key] != "active":
        return f"Invalid API key"

    # Simulate data extraction (you would use your actual extraction logic here)
    extracted_data = f"Extracted data from {file.filename}"

    if response_format == 'json':
        return jsonify({"data": extracted_data})
    else:
        return extracted_data

@app.route('/extract', methods=['POST'])
def extract_data():
    # Check for API key in the Authorization header
    api_key = request.headers.get('Authorization')
    if not api_key or not api_key.startswith("Bearer "):
        return jsonify({"error": "API key missing or incorrect"}), 401

    api_key = api_key.split("Bearer ")[1]

    if api_key not in api_keys or api_keys[api_key] != "active":
        return jsonify({"error": "Invalid API key"}), 403

    # Check for the file and format parameters
    if 'file' not in request.files or 'format' not in request.form:
        return jsonify({"error": "Missing file or format parameter"}), 400

    file = request.files['file']
    response_format = request.form['format']

    # Simulate data extraction (you would use your actual extraction logic here)
    extracted_data = f"Extracted data from {file.filename}"

    if response_format == 'json':
        return jsonify({"data": extracted_data})
    else:
        return extracted_data

if __name__ == '__main__':
    app.run(debug=True)
'''
