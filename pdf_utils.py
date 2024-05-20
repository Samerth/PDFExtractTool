import re
import os
from PyPDF2 import PdfReader

def extract_data_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as file:
        pdf_reader = PdfReader(file)
        num_pages = len(pdf_reader.pages)

        course_code = ""
        course_name = ""
        term_method = ""
        textbook_data = {
            "Raw_Text": ""
        }

        for page_num in range(num_pages):
            page = pdf_reader.pages[page_num]
            page_text = page.extract_text()

            match_code = re.search(r'Prefix and Code\s*([^\n]+)', page_text)
            if match_code:
                course_code = match_code.group(1).strip()

            match_name = re.search(r'Title\s*([^\n]+)', page_text)
            if match_name:
                course_name = match_name.group(1).strip()

            if "HBD" in os.path.basename(pdf_path).upper():
                term_method = "Hybrid"
            else:
                term_method = "Online"

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
