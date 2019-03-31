#!/usr/bin/python
# -*- coding: UTF-8 -*-

# this gets all events including dates of open seminars at Stockholm University

import urllib.request as request
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
    html = request.urlopen(scrape_url).read()
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('ul', {"class": "generated-list big-calendar image-layout add-bullets"})
    rows = table.find_all('li')
    events = []
    for row in rows:
        day = row.contents[1].contents[1].next
        month = row.contents[1].contents[3].next
        date = datetime.date(datetime.datetime.now().year, convert_swedish_month(month), int(day))
        link = row.contents[3]['href']
        title = row.contents[3].contents[1].next
        description = row.contents[3].contents[2].strip()
        if description is '':
            description = row.contents[3].contents[3].next.strip()
        linked_html = request.urlopen(link).read()
        linked_soup = BeautifulSoup(linked_html, 'html.parser')
        location = linked_soup.find('span', {"class": "location"}).text
        start_of_time_tag = linked_soup.find('span', {"class": "dtstart"})
        time_tag = start_of_time_tag.find('span', {"class": "value-title"}).get('title')
        time_tag_without_timezone = time_tag[:-6] # 2019-03-26T18:00+01:00
        starting_time = datetime.datetime.strptime(time_tag_without_timezone, '%Y-%m-%dT%H:%M') # 2019-03-26T18:00

        seminar = {
            "date" : date,
            "starting_time": starting_time.time(),
            "title" : title,
            "description" : description,
            "link" : link,
            "location" : location
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
