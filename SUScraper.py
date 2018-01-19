#!/usr/bin/python
# -*- coding: UTF-8 -*-

# this gets all events including dates of open seminars at Stockholm University

from urllib.request import urlopen
from bs4 import BeautifulSoup
import datetime

scrape_url = "http://www.su.se/om-oss/evenemang/%C3%B6ppna-f%C3%B6rel%C3%A4sningar/2.39658"


def convert_swedish_month(month):
    return {
        'jan': 1,
        'feb': 2,
        'mar': 3,
        'apr': 4,
        'maj': 5,
        'jun': 6,
        'jul': 7,
        'aug': 8,
        'sep': 9,
        'okt': 10,
        'nov': 11,
        'dec': 12,
    }[month]


def get_events():
    html = urlopen(scrape_url).read()
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('ul', {"class": "generated-list big-calendar image-layout add-bullets"})
    rows = table.find_all('li')
    events = []
    for row in rows:
        day = row.contents[1].contents[1].next
        month = row.contents[1].contents[3].next
        date = datetime.date(2018, convert_swedish_month(month), int(day))
        link = row.contents[3]['href']
        title = row.contents[3].contents[1].next
        description = row.contents[3].contents[2].strip()
        if description is '':
            description = row.contents[3].contents[3].next.strip()
        seminar = {
            "date" : date,
            "title" : title,
            "description" : description,
            "link" : link,
            "location" : "Stockholms Universitet"
        }
        events.append(seminar)
    return events


if __name__ == '__main__':
    try:
        events = get_events()
        if events == "":
            print("No events found!")
        else:
            for event in events:
                print("Event: " + ''.join(str(event)) + ")")
    except LookupError as le:
        print(le.message)
