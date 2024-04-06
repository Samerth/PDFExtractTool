from flask import Flask, request, jsonify, render_template
import re
import os
from PyPDF2 import PdfReader
import tempfile

app = Flask(__name__)

def extract_data_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as file:
        pdf_reader = PdfReader(file)
        num_pages = len(pdf_reader.pages)

        # Initialize variables to store extracted data
        course_code = ""
        course_name = ""
        term_method = ""
        textbook_data = {
            "Raw_Text": ""  # Store the entire "Required Books or Materials" section
        }

        for page_num in range(num_pages):
            page = pdf_reader.pages[page_num]
            page_text = page.extract_text()

            # Extract Course Code and Course Name
            match_code = re.search(r'Prefix and Code\s*([^\n]+)', page_text)
            if match_code:
                course_code = match_code.group(1).strip()

            match_name = re.search(r'Title\s*([^\n]+)', page_text)
            if match_name:
                course_name = match_name.group(1).strip()

            # Extract Term/Method from file name
            if "HBD" in os.path.basename(pdf_path).upper():
                term_method = "Hybrid"
            else:
                term_method = "Online"

            # Extract Textbook Information
            match_textbook = re.search(r'Required Books or Materials([\s\S]+)', page_text)

            if match_textbook:
                textbook_data["Raw_Text"] = match_textbook.group(1).strip()

        return {
            "Course Code": course_code,
            "Term": "",
            "Course Name": course_name,
            "Term/Method": term_method,
            "Textbook Data": textbook_data
        }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/extract-pdf-data', methods=['POST'])
def extract_pdf_data():
    uploaded_files = request.files.getlist('files')
    extracted_data_list = []

    for uploaded_file in uploaded_files:
        if os.path.isdir(uploaded_file.filename):
            # If it's a directory, process all PDF files within it
            for root, dirs, files in os.walk(uploaded_file.filename):
                for filename in files:
                    if filename.endswith(".pdf"):
                        pdf_path = os.path.join(root, filename)
                        extracted_data = extract_data_from_pdf(pdf_path)
                        extracted_data_list.append(extracted_data)
        else:
            # If it's a file, save and process it
            temp_file = tempfile.NamedTemporaryFile(delete=False)
            uploaded_file.save(temp_file.name)
            extracted_data = extract_data_from_pdf(temp_file.name)
            extracted_data_list.append(extracted_data)
            temp_file.close()
            os.unlink(temp_file.name)

    return jsonify(extracted_data_list)

if __name__ == '__main__':
    app.run(debug=True)
