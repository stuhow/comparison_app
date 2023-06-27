import pdftotext
import re

def load_text():
    with open('trailfinders.pdf', "rb") as f:
        pdf = pdftotext.PDF(f)

    text =''
    for page in pdf:
        text += page

    return text

def extract_date_tuples(text):
    date_pattern = re.compile('\s[A-Z]{3}\s[0-9]{2}\s[A-Z]{3}\s[0-9]{4}')

    # create list of dates
    matches1 = date_pattern.finditer(text)
    dates_list=[]
    for match1 in matches1:
        dates_list.append(match1.group().replace('\ue913 ',''))


    # Create date ranges to find the paragraphs of text
    tuple_dates_list = [(x,y) for x,y in zip(dates_list, dates_list[1:])]
    tuple_dates_list.append((dates_list[-1],)) # finds text after the final date

    return tuple_dates_list
