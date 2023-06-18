import os
import openai


openai.api_key = os.getenv("OPENAI_API_KEY")

text = 'svljbkadlvbalc'

def generate_prompt(text):
    return f"""For each of the hotels in this page from an itinerary can you tell me the check-in date of each hotel, check-out date of each hotel, hotel names, room category, number of rooms and board basis from the below text? If there is no hotel return no hotel

            {text}

            format:
            Check-in Date:
            Check-out Date:
            Hotel Name:
            Room Category:
            Number of Rooms:
            Board Basis:

            All hotels:

            No hotel"""

response = openai.Completion.create(
  model="text-davinci-003",
  prompt=generate_prompt(text),
  temperature=0,
  max_tokens=2649,
  top_p=1,
  frequency_penalty=0,
  presence_penalty=0
  )
