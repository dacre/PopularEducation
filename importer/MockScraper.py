#!/usr/bin/python
# -*- coding: UTF-8 -*-

# this gets all events including dates of open seminars at FolkUniversitetet

import urllib.request as request
from bs4 import BeautifulSoup
import datetime


def format_date(jumbled_date_string):
    separated_date_string = jumbled_date_string.split()
    date = datetime.date(int(separated_date_string[0]), int(separated_date_string[1]),
                         int(separated_date_string[2]))
    return date


def get_events():
    events = []
    for row, idx in enumerate(range(1,10)):
        event_date = format_date("2018 1 " + str(idx))
        seminar = {
            "date":  event_date,
            "title": "mock_title_" + str(idx),
            "link": "http://mock_title_" + str(idx),
            "location": "Mock place, " + str(idx)
        }
        print("scraper: " + str(seminar))
        events.append(seminar)
    return events


if __name__ == '__main__':
    events = get_events()