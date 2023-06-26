import re
import pdftotext

# here
import os
import openai
import pdftotext

with open('trailfinders.pdf', "rb") as f:
    pdf = pdftotext.PDF(f)

text =''
for page in pdf:
    text += page

date_pattern = re.compile('\s[A-Z]{3}\s[0-9]{2}\s[A-Z]{3}\s[0-9]{4}')


# create list of dates
matches1 = date_pattern.finditer(text)
dates_list=[]
for match1 in matches1:
    dates_list.append(match1.group().replace('\ue913 ',''))


# Create date ranges to find the paragraphs of text
tuple_dates_list = [(x,y) for x,y in zip(dates_list, dates_list[1:])]
tuple_dates_list.append((dates_list[-1],)) # finds text after the final date


for i in tuple_dates_list:
        # find's text between dates
        if len(i)==2:
            hotel_pattern2 = re.compile('(\s' + i[0]  + ')((.|\n)*)' + '(\s' + i[1] + ')')
            matches = hotel_pattern2.finditer(text)
            for match in matches:
                paragraph = match.group(2)
                print('..........')
                print(paragraph)
                regex = re.compile(r'ACCOMMODATION\s+(.*)\s+Location', re.DOTALL)
                match = regex.search(paragraph)
                if match:
                    hotel_name = match.group(1).strip()
                    print(hotel_name)

                regex = re.compile(r'for\s+(\d+)\s+night')
                match = regex.search(paragraph)
                if match:
                    num_nights = match.group(1)
                    print(num_nights)

        else:
            hotel_pattern2 = re.compile('( ' + i[0]  + ')((.|\n)*)')
            matches = hotel_pattern2.finditer(text)

            for match in matches:
                paragraph = match.group(2)
                regex = re.compile(r'ACCOMMODATION\s+(.*)\s+Location', re.DOTALL)
                match = regex.search(paragraph)
                if match:
                    hotel_name = match.group(1).strip()
                    print(hotel_name)

                regex = re.compile(r'for\s+(\d+)\s+night')
                match = regex.search(paragraph)
                if match:
                    num_nights = match.group(1)
                    print(num_nights)
