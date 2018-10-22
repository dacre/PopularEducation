#!/usr/bin/python
# -*- coding: UTF-8 -*-

# this handles the web site's paths
from datetime import datetime

import os
import csv
from flask import Flask
app = Flask(__name__)

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
database_filename = os.path.join(__location__, '/db/db.csv')


def get_events():
    events = []
    with open(database_filename, 'rt', encoding="utf-8") as csv_file:
        db_reader = csv.DictReader(csv_file)
        for row in db_reader:
            event = {'location': row['location'],
                     'date': row['date'],
                     'title': row['title'],
                     'link': row['link']}
            events.append(event)
    return events


@app.route('/')
def hello_world():
    site = "<title>Öppna föreläsningar i Stockholm</title><p><h1>Kommande föreläsningar: </h1></p>"

    seminar_listing = """<table style="width:100% id=seminar_listing_table">
                            <tr>
                                <th>Plats</th>
                                <th>Datum</th>
                                <th>Titel</th> 
                            </tr>
                            """
    events = get_events()

    for seminar in events:
        seminar_listing = seminar_listing + "<tr>"
        seminar_listing = seminar_listing + "<td>" + seminar['location'] + "</td>"
        seminar_listing = seminar_listing + "<td>" + seminar['date'] + "</td>"
        seminar_listing = seminar_listing + "<td><a href='" + seminar['link'] + "'>" + seminar['title'] + "</a></td>"
        seminar_listing = seminar_listing + "</tr>"
    return site + seminar_listing

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')

