from flask import Flask, request, jsonify
import re
import os
from PyPDF2 import PdfReader
import tempfile

app = Flask(__name__)

def extract_data_from_pdf(pdf_data):
    # Create a temporary file to write the PDF data
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(pdf_data)

        # Read the PDF data from the temporary file
        pdf_path = temp_file.name
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

        # Delete the temporary file
        os.unlink(pdf_path)

        return {
            "Course Code": course_code,
            "Term": "",
            "Course Name": course_name,
            "Term/Method": term_method,
            "Textbook Data": textbook_data
        }

@app.route('/extract-pdf-data', methods=['POST'])
def extract_pdf_data():
    # Read the PDF data from the request body
    pdf_data = request.get_data()

    # Extract data from the PDF data
    extracted_data = extract_data_from_pdf(pdf_data)

    return jsonify(extracted_data)

if __name__ == '__main__':
    app.run(debug=True)
