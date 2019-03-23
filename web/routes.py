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
                     'link': row['link']}
            events.append(event)
    return events


@app.route('/')
def hello_world():
    site = """
    <html>
    <head>
        <title>Öppna föreläsningar i Stockholm</title>
        <link rel="stylesheet" type="text/css" href="static/test.css">
    </head>
    <h1>Kommande föreläsningar</h1></p>
    <div class="table">
    """

    seminar_listing = """<table class="u-full-width"">
                            <thead>
                                <tr>
                                    <th>Källa</th>
                                    <th>Datum</th>
                                    <th>Titel</th> 
                                </tr>
                            </thead>
                            <tbody>
                            """
    events = get_events()

    for seminar in events:
        seminar_listing = seminar_listing + "<tr>"
        seminar_listing = seminar_listing + "<td>" + seminar['location'] + "</td>"
        seminar_listing = seminar_listing + "<td>" + seminar['date'] + "</td>"
        seminar_listing = seminar_listing + "<td><a href='" + seminar['link'] + "'>" + seminar['title'] + "</a></td>"
        seminar_listing = seminar_listing + "</tr>"

    seminar_listing = seminar_listing + "</tbody></table>"\

    seminar_listing = seminar_listing + """<table class="u-full-width">
                                              <thead>
                                                <tr>
                                                  <th>Name</th>
                                                  <th>Age</th>
                                                  <th>Sex</th>
                                                  <th>Location</th>
                                                </tr>
                                              </thead>
                                              <tbody>
                                                <tr>
                                                  <td>Dave Gamache</td>
                                                  <td>26</td>
                                                  <td>Male</td>
                                                  <td>San Francisco</td>
                                                </tr>
                                                <tr>
                                                  <td>Dwayne Johnson</td>
                                                  <td>42</td>
                                                  <td>Male</td>
                                                  <td>Hayward</td>
                                                </tr>
                                              </tbody>
                                            </table>"""
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


if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')

