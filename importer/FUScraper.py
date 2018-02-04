#!/usr/bin/python
# -*- coding: UTF-8 -*-

# this gets all events including dates of open seminars at FolkUniversitetet

import urllib.request as request
from bs4 import BeautifulSoup
import datetime


scrape_url = "http://www.folkuniversitetet.se/Har-finns-vi/Stockholm/Forelasningar-och-seminarier/"
base_url = "http://www.folkuniversitetet.se"


def format_date(jumbled_date_string):
    separated_date_string = jumbled_date_string.split()
    date = datetime.date(int(separated_date_string[2]), convert_swedish_month(separated_date_string[1]),
                         int(separated_date_string[0]))
    return date


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
    html = request.urlopen(scrape_url).read()
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('div', {"class": "nfu-course-list"})
    rows = table.find_all('div', {"class": "medium-10 columns"})
    events = []
    for row in rows:
        link = row.find('a')
        event_link = base_url + link.attrs['href']
        title = link.contents[0]
        meta_data = row.find_all('span', {"class": "nfu-course-list-item__secondary-info-text"})
        for idx, date in enumerate(meta_data):
            if idx == 1:
                event_date = format_date(date.contents[0])
        seminar = {
            "date" : event_date,
            "title" : title,
            "link" : event_link,
            "location" : "Folkuniversitetet"
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


