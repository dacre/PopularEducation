#!/usr/bin/python
# -*- coding: UTF-8 -*-

# this handles the web site's paths

import SUScraper
import FUScraper
from flask import Flask
app = Flask(__name__)


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
    events = SUScraper.get_events() + FUScraper.get_events()
    from operator import itemgetter
    sorted_events = sorted(events, key=itemgetter('date'))

    for seminar in sorted_events:
        seminar_listing = seminar_listing + "<tr>"
        seminar_listing = seminar_listing + "<td>" + seminar['location'] + "</td>"
        seminar_listing = seminar_listing + "<td>" + seminar['date'].strftime("%y-%m-%d") + "</td>"
        seminar_listing = seminar_listing + "<td><a href='" + seminar['link'] + "'>" + seminar['title'] + "</a></td>"
        seminar_listing = seminar_listing + "</tr>"
    return site + seminar_listing

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')

