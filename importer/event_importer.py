#!/usr/bin/python
# -*- coding: UTF-8 -*-

# this stores events from all event sites in a file
import csv
import datetime

database_filename = '../db/db.csv'


def store_events(events):
    with open(database_filename, 'w+') as csv_file:
        fieldnames = ['location', 'date', 'starting_time', 'title', 'link']
        db_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        db_writer.writeheader()
        for event in events:
            db_writer.writerow({'location': event['location'],
                                'date': event['date'],
                                'starting_time': event['starting_time'],
                                'title': event['title'],
                                'link': event['link']})


def main():
    events = ABFScraper.get_events() + SUScraper.get_events() + FUScraper.get_events()
    from operator import itemgetter
    sorted_events = sorted(events, key=itemgetter('date'))
    store_events(sorted_events)

    print(str(len(sorted_events)) + " events imported at "+ str(datetime.date.today()))


if __name__ == "__main__":
    if __name__ == '__main__':
        if __package__ is None:
            import sys
            from os import path

            sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
            from importer import ABFScraper, SUScraper, FUScraper
        else:
            from ..importer import ABFScraper, SUScraper, FUScraper
    main()
