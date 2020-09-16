"""A script for scraping together a list of bills
currently before parliament
"""

from bs4 import BeautifulSoup
import requests


def cache_request(url: str) -> str:
    """Handles requests for web pages and saves them
    locally, enabling the script to be run repeatedly offline
    """
    cache = "html-cache/"
    url_hash = str(hash(url))
    try:
        with open(cache + url_hash, 'r') as fp:
            html = fp.read()
    except FileNotFoundError:
        html = requests.get(url).text
        with open(cache + url_hash, 'w') as fp:
            fp.write(html)
    return html

# Generate the total soup
URL = "https://services.parliament.uk/"
HTML = cache_request(URL + "Bills/")
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
    commons_stages[data.text.strip()] = data['href'][:-5] + 'stages.html'
    print(f"{data.text.strip():100}{data['href']}")
