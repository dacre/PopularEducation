#!/usr/bin/python
# -*- coding: UTF-8 -*-

# this stores events from all event sites in a file
import csv
import os

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
database_filename = os.path.join(__location__, 'db/db.csv')


def store_events(events):
    with open(database_filename, 'w') as csv_file:
        fieldnames = ['location', 'date', 'title', 'link']
        db_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        db_writer.writeheader()
        for event in events:
            db_writer.writerow({'location': event['location'], 'date': event['date'],
                                'title': event['title'], 'link': event['link']})


def main():
    events = SUScraper.get_events() + FUScraper.get_events()
    #events = MockScraper.get_events()
    from operator import itemgetter
    sorted_events = sorted(events, key=itemgetter('date'))

    store_events(sorted_events)


if __name__ == "__main__":
    if __name__ == '__main__':
        if __package__ is None:
            import sys
            from os import path

            sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
            from importer import SUScraper, FUScraper, MockScraper
        else:
            from ..importer import SUScraper, FUScraper, MockScraper
    main()
