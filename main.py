import re
import os
from PyPDF2 import PdfReader

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

def process_folder(folder_path):
    extracted_data_list = []

    for filename in os.listdir(folder_path):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(folder_path, filename)
            extracted_data = extract_data_from_pdf(pdf_path)
            extracted_data_list.append(extracted_data)

    return extracted_data_list

# Provide the path to the folder containing PDF files
folder_path = r"C:\Users\spsam\Desktop\Websites\4_PDFExtractTool\OneDrive_1_1-22-2024"
extracted_data_list = process_folder(folder_path)

# Print the extracted data for each PDF
for idx, data in enumerate(extracted_data_list, start=1):
    print(f"PDF {idx} Data:")
    print(data)
    print("\n" + "-"*50 + "\n")
