from flask import Flask, render_template, request, redirect, url_for
import re
from PyPDF2 import PdfFileReader
from helperfunctions import select_company, get_data


app = Flask(__name__)


# @app.route('/')
# def index():
#     return render_template('index.html')


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Check if the POST request has a file part
        if 'file' not in request.files:
            return 'No file uploaded'

        file = request.files['file']

        # Check if the file is a PDF
        if file.filename.endswith('.pdf'):

            # Read PDF
            pdf_reader = PdfFileReader(file)

            # Extract text
            text =''
            for page in pdf_reader.pages:
                text += page.extract_text()

            # check name of company function
            company = select_company(text)

            # once we have the name of the company extract the data with the
            # correct functions returning dictionaries for the costs, flights and hotels
            quote_data = get_data(text, company)

            return render_template('results.html', company=company, hotel=quote_data[1], data=quote_data[0])

        return 'Invalid file format'

    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
