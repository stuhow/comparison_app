import os
import openai
import pdftotext

openai.api_key = os.getenv("OPENAI_API_KEY")

quote = 'New England Self Drive - A&K Dec 19.pdf'

def generate_prompt(text):
    return f"""For each hotel on this page from an itinerary can you tell me the check-in date of each hotel, check-out date of each hotel, hotel names, room category, number of rooms and board basis from the below text?

{text}

format:
Check-in Date: day/month/year
Check-out Date: day/month/year
Hotel Name: if no name fill with N/A
Room Category:
Number of Rooms:
Board Basis:

All hotels:

"""


all_responses = []

with open(quote, "rb") as f:
    pdf = pdftotext.PDF(f)

# All pages
for text in pdf:
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=generate_prompt(text),
        temperature=0,
        max_tokens=2650,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
        )
    all_responses.append(response)
    print(response)
    print('................................')

print(all_responses)
