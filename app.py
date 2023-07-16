import time
from PyPDF2 import PdfFileReader
import pdftotext
from flask import Flask, render_template, request, redirect, session
from api.helperfunctions import select_company, get_data #, add_iata_code, add_flight_cost, add_hotel_details, add_multistop_flight_cost
# from prototyping import get_flight_dict, get_hotel_dict
from companies.trailfinders import trailfinders_dictionaries

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

    full_pdf = pdftotext.PDF(pdf_file)

    text =''
    for page in full_pdf:
        text += page

    # check name of company function
    company = select_company(text)

    # once we have the name of the company extract the data with the
    # correct functions returning dictionaries for the costs, flights and hotels
    quote_data = get_data(text, company)


    # statement to add max number of seats to carhire dict based on number of pax
    if quote_data[0]['Number of people'][0] >= 2:
        quote_data[3]['Max seats'].append(5)

    # car_hire_dict = quote_data[3]['Max seats'].append('5')
    # car_hire_dict['Max seats'].append('5')

    # # get hotel costs
    # hotel_dict = add_hotel_details(quote_data[1])

    # # add iatacode to flight dict
    # flight_dict = add_iata_code(quote_data[2])

    # flight_dict = add_multistop_flight_cost(flight_dict)

    pdf_file.close()

    # Store the extracted data in session
    session['flight_dict'] = quote_data[2]
    session['company'] = company
    session['cost_data'] = quote_data[0]['Total price'][0]
    session['hotel_dict'] = quote_data[1] # quote_data[1]
    session['car_hire_dict'] = quote_data[3]
    session['excursion_dict'] = quote_data[4]


    # Redirect to the results page
    return redirect('/results')

@app.route('/results')
def results():
    # Retrieve the extracted lines from session
    flight_dict = session.get('flight_dict', [])
    cost_data = session.get('cost_data', [])
    company = session.get('company', [])
    hotel_dict = session.get('hotel_dict', [])
    car_hire_dict = session.get('car_hire_dict', [])
    excursion_dict = session.get('excursion_dict', [])

    # Render the results page with the extracted lines
    return render_template('results.html', company=company,
                                            flight=flight_dict,
                                            hotel=hotel_dict,
                                            costs=cost_data,
                                            carhire=car_hire_dict,
                                            excursion=excursion_dict)

if __name__ == '__main__':
    app.run(debug=True)
