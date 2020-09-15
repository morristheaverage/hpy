"""A script for scraping together a list of bills
currently before parliament
"""

from bs4 import BeautifulSoup
import requests

# Generate the total soup
URL = "https://services.parliament.uk/Bills/"
HTML = requests.get(URL).text
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

for bill in commons:
    print(bill('td', 'bill-item-description')[0].a.text.strip())
