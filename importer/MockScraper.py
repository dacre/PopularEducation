#!/usr/bin/python
# -*- coding: UTF-8 -*-

# this creates 10 fake events

import datetime
import logging
import os

from importer import log_test


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


def log_setup():
    # create logger with 'importer'
    logger = logging.getLogger('importer')
    logger.setLevel(logging.DEBUG)
    # create file handler which logs even debug messages
    fh = logging.FileHandler('../log/importer.log')
    fh.setLevel(logging.DEBUG)
    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    # create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    # add the handlers to the logger
    logger.addHandler(fh)
    logger.addHandler(ch)


if __name__ == '__main__':
    log_setup()
    logger = logging.getLogger('importer.' + os.path.basename(__file__))
    log_test.test_log()
    events = get_events()

    logger.info(str(len(events)) + " events imported at " + str(datetime.date.today()))

