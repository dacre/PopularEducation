#!/usr/bin/python
# -*- coding: UTF-8 -*-

# this gets all events including dates of open seminars at Stockholm University
import logging
import urllib.request as request
from bs4 import BeautifulSoup
import datetime
from importer import event_importer
import os

scrape_url = "http://www.su.se/om-oss/evenemang/%C3%B6ppna-f%C3%B6rel%C3%A4sningar/2.39658"

logger = logging.getLogger('importer.' + os.path.basename(__file__))


def get_likely_year(formatted_date):
    current_month = datetime.date.today().month
    current_year = datetime.date.today().year
    if formatted_date.month < current_month:
        return current_year+1
    else:
        return current_year


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
        try:
            link = row.contents[3]['href']
            title = row.contents[3].contents[1].next
            description = row.contents[3].contents[2].strip()
            if description is '' and len(row.contents[3].contents) > 3:
                description = row.contents[3].contents[3].next.strip()
            linked_html = request.urlopen(link).read()
            linked_soup = BeautifulSoup(linked_html, 'html.parser')
            location = linked_soup.find('span', {"class": "location"}).text
            start_of_time_tag = linked_soup.find('span', {"class": "dtstart"})
            time_tag = start_of_time_tag.find('span', {"class": "value-title"}).get('title')
            time_tag_without_timezone = time_tag[:-6] # 2019-03-26T18:00+01:00
            starting_time = datetime.datetime.strptime(time_tag_without_timezone, '%Y-%m-%dT%H:%M') # 2019-03-26T18:00

            seminar = {
                "date" : starting_time.date(),
                "starting_time": starting_time.time(),
                "title" : title,
                "description" : description,
                "link" : link,
                "location" : location
            }
            events.append(seminar)
        except Exception:
            logger.error("event could not be parsed", exc_info=True)
    logger.info("Imported " + str(len(events)))
    return events


if __name__ == '__main__':
    try:
        events = get_events()
        logger.info("Imported " + str(len(events)))

    except Exception:
        logger.error(exc_info=True)

