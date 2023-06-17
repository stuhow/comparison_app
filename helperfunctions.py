from companies.abercrombie import abercrombie_dictionaries

def select_company(text):
    if 'abercrombie' in text:
        return 'Abercrombie & Kent'

def get_data(text, company):
    if company == "Abercrombie & Kent":
        return abercrombie_dictionaries(text)
