from flask import Flask, request, jsonify, render_template
import os
import tempfile
from pdf_utils import extract_data_from_pdf
from flask import send_from_directory

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/js/<path:filename>')
def serve_js(filename):
    return send_from_directory('js', filename)

@app.route('/extract-pdf-data', methods=['POST'])
def extract_pdf_data():
    uploaded_files = request.files.getlist('files')
    extracted_data_list = []

    for uploaded_file in uploaded_files:
        temp_file = tempfile.NamedTemporaryFile(delete=False)
        uploaded_file.save(temp_file.name)
        extracted_data = extract_data_from_pdf(temp_file.name)
        extracted_data_list.append(extracted_data)
        temp_file.close()
        os.unlink(temp_file.name)

    return jsonify(extracted_data_list)

if __name__ == '__main__':
    app.run(debug=True)
