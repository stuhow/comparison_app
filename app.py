from flask import Flask, render_template, request, redirect, url_for
import re
from PyPDF2 import PdfFileReader

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

            # Find trip cost summaries from within text
            cost_parrern = re.compile('Total Holiday Cost   Average per person cost   Total Deposit required to confirm \nthese arrangements  \n \n(£.+)\n.+\n(£.+)\n(£.+)')
            costs = re.findall(cost_parrern, text)

            data = {'Breakdown': ['Total Holiday Cost', 'Average per person cost', 'Total Deposit required to confirm these arrangements'], 'Cost': [costs[0][0].split(' ')[0], costs[0][1], costs[0][2]]}

            return render_template('results.html', data=data)

        return 'Invalid file format'

    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
