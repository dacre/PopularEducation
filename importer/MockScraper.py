#!/usr/bin/python
# -*- coding: UTF-8 -*-

# this creates 10 fake events

import datetime


def format_date(jumbled_date_string):
    separated_date_string = jumbled_date_string.split()
    date = datetime.date(int(separated_date_string[0]), int(separated_date_string[1]),
                         int(separated_date_string[2]))
    return date


def get_events():
    events = []
    for outer in range(0,10):
        for row, idx in enumerate(range(10,20)):
            event_date = format_date("2019 7 " + str(idx))
            seminar = {
                "date": event_date,
                "starting_time": datetime.time(19, 0),
                "title": "mock_title_" + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S' + " - " + str(idx)),
                "link": "http://mock_title_" + str(idx),
                "location": "Mock place, " + str(idx)
            }
            events.append(seminar)
    return events


if __name__ == '__main__':
    events = get_events()