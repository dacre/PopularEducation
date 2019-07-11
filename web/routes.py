#!/usr/bin/python
# -*- coding: UTF-8 -*-

# this file handles the web site's paths

from flask import send_file, render_template, Flask, request
import csv
import datetime

app = Flask(__name__)
default_number_of_events_to_show = 5
database_filename = 'db/db.csv'


def filtered_in(date, days_in_filter):
    datetime_date = datetime.datetime.strptime(date, '%Y-%m-%d')
    converted_date_to_day_type = datetime_date.isoweekday()
    if str(converted_date_to_day_type) in days_in_filter or len(days_in_filter) is 0:
        return True
    else:
        return False


def get_events(days_in_filter):
    events = []
    with open(database_filename, 'rt', encoding="utf-8") as csv_file:
        db_reader = csv.DictReader(csv_file)
        for row in db_reader:
            if filtered_in(row['date'], days_in_filter):
                event = {'location': row['location'],
                         'date': row['date'],
                         'title': row['title'],
                         'link': row['link'],
                         'starting_time': row['starting_time']}
                events.append(event)
    return events


def checkbox_days_checked(day_of_week, filter_days):
    if len(filter_days) is 0:
        return "checked"
    for day in filter_days:
        if day == day_of_week:
            return "checked"
    else:
        return ""


def checkbox_all(filter_days):
    for idx in range(0, 7):
        checkbox_days_checked(str(idx), filter_days)


def get_filter_day_for_POST(filter_days):
    post_string = ""
    for day in filter_days:
        post_string = post_string + """<input type="hidden" name="day_group[]" value=""" + day + """>"""
    return post_string


@app.route('/')
def hello_world():
    # print("Example print statement to show that Flush is required for logging to Flask:", flush=True)
    number_of_results = request.args.get('number_of_results')
    if number_of_results is not None:
        events_to_show = int(number_of_results)
    else:
        events_to_show = default_number_of_events_to_show
    shown_so_far = request.args.get('shown_so_far')
    if shown_so_far is not None:
        shown_so_far = int(shown_so_far)
    else:
        shown_so_far = int(0)

    filter_days = request.args.getlist('day_group[]')

    html_top = """
    <!DOCTYPE html>
    <!–– meta tag with viewport needed because: https://stackoverflow.com/questions/26888751/chrome-device-mode-emulation-media-queries-not-working ––>
    <head>
        <meta name="viewport" content="width=device-width"> 
        <title>Öppna föreläsningar i Stockholm</title>
        <link rel="stylesheet" type="text/css" href="static/skeleton_and_responsive_table.css">
        <h1 id="#"><a href="/">Bildningstid</a></h1>
        <h2>Öppna föreläsningar i Stockholm</h2>
    </head>
    <body>
    <br>
    <form method="get">
        
        <legend>Välj vilka dagar du vill filtrera fram.<br></legend>
        
        <input type="checkbox" name="day_group[]" value="1" id="1" """ + checkbox_days_checked("1", filter_days) + """> Måndagar
        <br>
        <input type="checkbox" name="day_group[]" value="2" id="2" """ + checkbox_days_checked("2", filter_days) + """> Tisdagar
        <br>
        <input type="checkbox" name="day_group[]" value="3" id="3" """ + checkbox_days_checked("3", filter_days) + """> Onsdagar
        <br>
        <input type="checkbox" name="day_group[]" value="4" id="4" """ + checkbox_days_checked("4", filter_days) + """> Torsdagar
        <br>
        <input type="checkbox" name="day_group[]" value="5" id="5" """ + checkbox_days_checked("5", filter_days) + """> Fredagar
        <br>
        <input type="checkbox" name="day_group[]" value="6" id="6" """ + checkbox_days_checked("6", filter_days) + """> Lördagar
        <br>
        <input type="checkbox" name="day_group[]" value="7" id="7" """ + checkbox_days_checked("7", filter_days) + """> Söndagar
        <br><input type="submit" value="Filtrera!">    <a href="/">Nollställ</a>
        
    </form>"""
    # TODO gör lista av knapparna
    # TODO filtrering (7 knappar (för alla veckodagar) och ett sifferformulär (för antal dagar framöver, förifyllt med 30). Knapparna laddar om sidan
    html_seminar_table = """<div>
                            <table>
                            <thead>
                                <tr>
                                    <th>Datum</th>
                                    <th>Vad och var</th> 
                                </tr>
                            </thead>
                            <tbody>
                            """
    events = get_events(filter_days)
    html_seminar_listing = ""
    html_end = ""
    idx = 0
    for idx, seminar in enumerate(events):
        if idx+1 > events_to_show:
            html_end = html_end + """<br>
                            
                                <form method="get" action="/#continue_listing">
                                    <input type="hidden" name="shown_so_far" id=shown_so_far value=""" + str(idx) + """>
                                    <input type="hidden" name="number_of_results" id=number_of_results value=""" + \
                                    str(events_to_show*2) + """>""" + get_filter_day_for_POST(filter_days) + """
                                    <button>Visa mer</button>
                                    </form>
                            """
            break
        if idx >= shown_so_far:
            html_seminar_listing = html_seminar_listing + "<tr id='continue_listing'>"
        else:
            html_seminar_listing = html_seminar_listing + "<tr>"
        html_seminar_listing = html_seminar_listing + "<td>" + seminar['date'] + "</td>"
        html_seminar_listing = html_seminar_listing + "<td>" \
            "<a href='" + seminar['link'] + "'>" + seminar['title'] + "</a>" \
                        "<br>Var: " + get_location(seminar['location'])  + \
                        "<br>Starttid: " + seminar['starting_time'][:-3] + \
                                                              "</td>"
        html_seminar_listing = html_seminar_listing + "</tr>"

    html_seminar_end = "</tbody></table></div>"


    html_end = html_end + """<form method="get" action="/">
                                        <input type="hidden" name="shown_so_far" id=shown_so_far value=""" + str(idx) + """>
                                        <input type="hidden" name="number_of_results" id=number_of_results value=""" + \
               str(events_to_show) + """>""" + get_filter_day_for_POST(filter_days) + """<button>Till toppen på sidan</button></form>"""
    html_end = html_end + "</body></html>"

    return html_top + html_seminar_table + html_seminar_listing + html_seminar_end + html_end


@app.route('/file-downloads/')
def file_downloads():
    try:
        return render_template('downloads.html')
    except Exception as e:
        print(str(e))


@app.route('/return-files/')
def return_files_tut():
    try:
        return send_file('images/favicon.png', attachment_filename='favicon.png')
    except Exception as e:
        print(str(e))


def get_location(location):
    if location == "":
        return "Kolla evenemangets sida för info"
    else:
        return location


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
