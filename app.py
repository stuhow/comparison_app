import time
from PyPDF2 import PdfFileReader
from flask import Flask, render_template, request, redirect, session
from helperfunctions import select_company, get_data, add_iata_code, add_flight_cost, add_hotel_details
from prototyping import get_flight_dict, get_hotel_dict

app = Flask(__name__)
app.secret_key = 'your_secret_key'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get the uploaded file
        file = request.files['file']

        # Save the file to disk
        file.save('uploaded_file.pdf')

        # Redirect to the loading page
        return redirect('/loading')

    return render_template('index.html')

@app.route('/loading')
def loading():
    return render_template('loading.html')

@app.route('/extract')
def extract():
    # Extract the first 10 lines from the PDF
    pdf_file = open('uploaded_file.pdf', 'rb')
    # Read PDF
    pdf_reader = PdfFileReader(pdf_file)

    # Extract text
    text =''
    for page in pdf_reader.pages:
        text += page.extract_text()

    # check name of company function
    company = select_company(text)

    # once we have the name of the company extract the data with the
    # correct functions returning dictionaries for the costs, flights and hotels
    quote_data = get_data(text, company)

    # get prototyping hotel example
    hotel_dict = get_hotel_dict()

    # get hotel costs
    hotel_dict = add_hotel_details(hotel_dict)

    # get prototyping filght example
    flight_dict = get_flight_dict()

    # add iatacode to flight dict
    flight_dict = add_iata_code(flight_dict)

    flight_dict = add_flight_cost(flight_dict)

    pdf_file.close()

    # Store the extracted data in session
    session['flight_dict'] = flight_dict
    session['company'] = company
    session['quote_data'] = quote_data
    session['hotel_dict'] = hotel_dict


    # Redirect to the results page
    return redirect('/results')

@app.route('/results')
def results():
    # Retrieve the extracted lines from session
    flight_dict = session.get('flight_dict', [])
    quote_data = session.get('quote_data', [])
    company = session.get('company', [])
    hotel_dict = session.get('hotel_dict', [])

    # Render the results page with the extracted lines
    return render_template('results.html', company=company,
                                            flight=flight_dict, #quote_data[2]
                                            hotel=hotel_dict, #quote_data[1]
                                            data=quote_data[0])

if __name__ == '__main__':
    app.run(debug=True)
