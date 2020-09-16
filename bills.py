"""A script for scraping together a list of bills
currently before parliament
"""

import codecs
from datetime import date
from bs4 import BeautifulSoup
import requests



def cache_request(url: str) -> str:
    """Handles requests for web pages and saves them
    locally, enabling the script to be run repeatedly offline

    Args:
        url (str): A url to be requested

    Returns:
        str: The text of the response to the request e.g. a html file
    """
    cache = "html-cache/"
    url_hash = str(hash(url))
    enc = 'utf-8'
    try:
        with codecs.open(cache + url_hash, mode='r', encoding=enc) as file:
            html = file.read()
    except FileNotFoundError:
        html = requests.get(url).text
        with codecs.open(cache + url_hash, mode='w', encoding=enc) as file:
            file.write(html)
    return html

def dop(datestr: str) -> int:
    """Takes a date and returns the nth day of the
    current parliament on which the date falls

    Args:
        datestr (str): A date in DD/MM/YYYY format

    Returns:
        int: The value n, where datestr is n days after the last election
    """
    # Reference value
    start = date(2019, 12, 12) # Election was 12th Dec 2019

    # Create new date object
    day, month, year = (int(val) for val in datestr.split('.'))
    day = date(year, month, day)

    # Return difference
    return (day - start).days




# Generate the total soup
URL = "https://services.parliament.uk"
HTML = cache_request(URL + "/Bills/")
soup = BeautifulSoup(HTML, 'html5lib')

# Find all bills and categorise them accordingly
bills = [bill for bill in soup('tr')
        if any(x in bill.get('class', [])
                for x in ['tr1', 'tr2'])]

commons, lords, ras = [], [], []
for bill in bills:
    cat = bill.td.img['alt']
    if cat == "Commons":
        commons.append(bill)
    elif cat == "Lords":
        lords.append(bill)
    elif cat == "Royal Assent":
        ras.append(bill)

print(f"{len(commons)} bills in the Commons,")
print(f"{len(lords)} bills in the Lords,")
print(f"{len(ras)} bills granted Royal Assent.")

# Record links to a page with info about the stages of the bill
commons_stages = {}
for bill in commons:
    data = bill('td', 'bill-item-description')[0].a
    commons_stages[data.text.strip()] = data['href'][:-5] + '/stages.html'
    print(f"{data.text.strip():100}{data['href']}")

print("Page titles")
# Load up stages.html pages into cache
for url_end in commons_stages.values():
    page = URL + url_end
    html_stage = cache_request(page)
    print(page)
    soup = BeautifulSoup(html_stage, "html5lib")
    print(soup.title.text.strip())
