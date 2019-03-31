#!/usr/bin/python
# -*- coding: UTF-8 -*-

# this handles the web site's paths
from datetime import datetime
from flask import send_file
from flask import render_template

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
                     'link': row['link'],
                     'starting_time': row['starting_time']}
            events.append(event)
    return events


@app.route('/')
def hello_world():
    site = """
    <html>
    <meta name="viewport" content="width=device-width"> 
    <!–– meta tag with viewport needed because: https://stackoverflow.com/questions/26888751/chrome-device-mode-emulation-media-queries-not-working ––>
    <head>
        <title>Öppna föreläsningar i Stockholm</title>
        <link rel="stylesheet" type="text/css" href="static/skeleton_and_responsive_table.css">
    </head>
    <h1>Kommande föreläsningar</h1></p>
    <div class="table">
    """

    # TODO filtrering (7 knappar (för alla veckodagar) och ett sifferformulär (för antal dagar framöver, förifyllt med 30). Knapparna laddar om sidan

    seminar_listing = """<table class="table">
                            <thead>
                                <tr>
                                    <th>Datum</th>
                                    <th>Vad och var</th> 
                                </tr>
                            </thead>
                            <tbody>
                            """
    events = get_events()

    for seminar in events:
        seminar_listing = seminar_listing + "<tr>"
        seminar_listing = seminar_listing + "<td>" + seminar['date'] + "</td>"
        seminar_listing = seminar_listing + "<td>" \
            "<a href='" + seminar['link'] + "'>" + seminar['title'] + "</a>" \
                        "<br>Var: " + get_location(seminar['location'])  + \
                        "<br>Starttid: " + seminar['starting_time'][:-3] + \
                                                              "</td>"
        seminar_listing = seminar_listing + "</tr>"

    seminar_listing = seminar_listing + "</tbody></table>"
    seminar_listing = seminar_listing + "</div></html>"

    return site + seminar_listing


@app.route('/file-downloads/')
def file_downloads():
    try:
        return render_template('downloads.html')
    except Exception as e:
        return str(e)


@app.route('/return-files/')
def return_files_tut():
    try:
        return send_file('images/favicon.png', attachment_filename='favicon.png')
    except Exception as e:
        return str(e)


def get_location(location):
    if location == "":
        return "Kolla evenemangets sida för info"
    else:
        return location


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
