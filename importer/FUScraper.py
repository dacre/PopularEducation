#!/usr/bin/python
# -*- coding: UTF-8 -*-

# this gets all events including dates of open seminars at FolkUniversitetet

import urllib.request as request
from bs4 import BeautifulSoup
import datetime
import bs4

scrape_url = "http://www.folkuniversitetet.se/Har-finns-vi/Stockholm/Forelasningar-och-seminarier/"
base_url = "http://www.folkuniversitetet.se"


def test_format_date():
    test_string = "                24 aug 2020            "
    result = format_date(test_string)
    if result == "":
        pass


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


def test_format_time():
    test_string = "Må 18:00 - 19:00 "
    result = format_time(test_string)
    assert result, "18:00"


def format_time(jumbled_time_string):
    separated_date_string = jumbled_time_string[3:-9]
    return separated_date_string


def get_events():
    import requests

    headers = {
        'authority': 'www.folkuniversitetet.se',
        'pragma': 'no-cache',
        'cache-control': 'no-cache',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'accept-language': 'sv-SE,sv;q=0.9,en-US;q=0.8,en;q=0.7,da;q=0.6',
        'cookie': 'cityId=option_0; nearbyCities=true; distanceCourses=false; ASP.NET_SessionId=z3pd5wpe030of4h0kxkcefdy; cookieinfo-closed=true',
        'dnt': '1',
    }

    params = (
        ('ll', '10924'),
        ('t', ''),
        ('d', ''),
        ('td', ''),
        ('p', '1'),
        ('s', '3'),
    )

    response = requests.get('https://www.folkuniversitetet.se/kurstyper/forelasningar/', headers=headers, params=params)

    soup = BeautifulSoup(response.text, 'html.parser')
    rows = soup.find_all('a', {"class": "card mb-3 js-card"})
    events = []
    for row in rows:
        if isinstance(row, bs4.element.Tag):
            event_link = base_url + row.attrs['href']
            title = row.find('h2', {"class": "card-title mb-0"})
            meta_data = row.find_all('span', {"class": "p-0 mt-3 mr-3 badge badge-transparent badge-with-icon"})

            for metadata in enumerate(meta_data):
                if "Startdatum" in metadata[1].text:
                    event_date = format_date(metadata[1].contents[5].text)
                if "Tid" in metadata[1].text:
                    time_stamp = format_time(metadata[1].contents[5].text)
                    starting_time = datetime.datetime.strptime(time_stamp, '%H:%M')
            seminar = {
                "date" : event_date,
                "starting_time": starting_time.time(),
                "title" : title.text.strip(),
                "link" : event_link,
                "location" : "Kungstensgatan 45, 102 39 Stockholm"
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


