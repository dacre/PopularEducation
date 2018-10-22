#!/usr/bin/python
# -*- coding: UTF-8 -*-

# this gets all events including dates of open seminars at Stockholm University

import urllib.request as request
from bs4 import BeautifulSoup
from datetime import datetime



scrape_url = "http://abfstockholm.se/kalendarium/?subject=Alla&when=1&event_tags=Alla&location=Alla&time=Alla&coorganizer=Alla&category=Alla&price=Alla&ref_date=2018-10-15&till=Alla&advanced_search=0&fav=0"
extra_header = "X-PJAX: true"

def get_events():
    #html = request.urlopen(scrape_url).read()
    html = """
    <span id="search-total" data-total="14"></span>
        <h2 class="published-date">Måndag 15 okt.</h2><div  data-event_id="24274" class="calendar-search-list post-24274 event type-event status-publish has-post-thumbnail hentry category-forelasning category-forelasning-samtal subject-ekonomi subject-politik-debatt location-abf-huset price-free coorganizer-6f coorganizer-abf-stockholm coorganizer-katalys event_tags-flagged">
	<div class="calendar-right">
     	<div class="calendar-right-box">
     		<div class="cost-title">KOSTNAD</div>
          	<p>Fri entré </p>
        </div>
        <div class="tag-title">TAGGAR</div>
        <p><a class="" href="http://abfstockholm.se?subject=ekonomi">Ekonomi</a>, <a class="" href="http://abfstockholm.se?subject=politik-debatt">Politik och debatt</a></p>
	</div>
	<div class="calendar-list-left">
     	<div class="calendar-list-left-top">
            <div class="calendar-list-head">
                <span class="date">Måndag 15 oktober 2018 13.30</span>
                <span class="link-home">ABF-huset</span>           </div>
        </div>
		<div class="calendar-list-left-body">
        	<div class="calendar-list-left-body-content">
            <div class="calendar-list-left-body-content-top">
			<img src="http://abfstockholm.se/wp-content/themes/abf-stockholm/library/timthumb.php?src=http://abfstockholm.se/wp-content/uploads/2018/10/ibrahim-rifath-789914-unsplash-e1536828991800.jpg&w=134&q=100&zc=1" alt="Lönebildning i en ny tid? &raquo; ABF" />
			<h3><a href="http://abfstockholm.se/event/2018/10/lonebildning-i-en-ny-tid/?back=http://abfstockholm.se/kalendarium/?when=1&subject=Alla&category=Alla&location=Alla&coorganizer=Alla">Lönebildning i en ny tid?</a></h3><p>Om lönenormeringens samhällsekonomiska konsekvenser</p>
            </div>
            <div class="calendar-list-footer">
		        		        <p class="author">Lars Calmfors, Åsa Olli Segendorf, Juhana Vartiainen, Annika Winsth, Mattias Dahl, Susanna Gideonsson, Mikael Johansson, Veli-Pekka Säikkälä, Enna Gerin</p><p>Fri entré med föranmälan här. Sedan avtalsrörelsen 1998 har de centralt avtalade lönekostnadsökningarna i den svenska ekonomin styrts av industrins...</p></div>
        	</div>
		</div>
		<div class="calendar-list-left-btm">

		</div>
	</div>
</div>
<div  data-event_id="24042" class="calendar-search-list no-image multipleIcons post-24042 event type-event status-publish hentry category-forelasning subject-historia subject-internationellt subject-litteratur location-abf-huset price-27 coorganizer-abf-stockholm coorganizer-pro-kultur activity_group-eftermiddagsforelasningar-med-pro">
	<div class="calendar-right">
     	<div class="calendar-right-box">
     		<div class="cost-title">KOSTNAD</div>
          	<p>60 kr. 40 kr för medlemmar i PRO. </p>
        </div>
        <div class="tag-title">TAGGAR</div>
        <p><a class="" href="http://abfstockholm.se?subject=historia">Historia</a>, <a class="" href="http://abfstockholm.se?subject=internationellt">Internationellt</a>, <a class="" href="http://abfstockholm.se?subject=litteratur">Litteratur</a></p>
	</div>
	<div class="calendar-list-left">
     	<div class="calendar-list-left-top">
            <div class="calendar-list-head">
                <span class="date">Måndag 15 oktober 2018 14.00</span>
                <span class="link-home">ABF-huset</span><span class="lecture">Serie</span>           </div>
        </div>
		<div class="calendar-list-left-body">
        	<div class="calendar-list-left-body-content">
            <div class="calendar-list-left-body-content-top">
			<h3><a href="http://abfstockholm.se/event/2018/10/1968/?back=http://abfstockholm.se/kalendarium/?when=1&subject=Alla&category=Alla&location=Alla&coorganizer=Alla">1968</a></h3><p>Om efterkrigstidens mest mytomspunna år</p>
            </div>
            <div class="calendar-list-footer">
		        		        <p class="author">Henrik Berggren</p><p>1968 är efterkrigstidens mest mytomspunna år – det uppfattas av många som avgörande i västvärldens historia och efter ett halvt...</p></div>
        	</div>
		</div>
		<div class="calendar-list-left-btm">

		</div>
	</div>
</div>
            """
    soup = BeautifulSoup(html, 'html.parser')
    #table = soup.find_all('div', {"class": "calendar-search-list"})
    rows = soup.find_all('div', {"class": "calendar-search-list"})
    #rows = table.find_all('h3')
    events = []
    for row in rows:
        date_string = row.find("span", {"class": "date"})
        import locale
        locale.setlocale(locale.LC_ALL, "sv_SE")
        date = datetime.strptime(date_string.string, '%A %d %B %Y %H.%M')

        title = row.find("h3")
        link = row.find("h3").find(href = True)

        description = soup.find('div', {"class": "calendar-list-footer"}).find_all("p")[1]
        if description is '':
            description = row.contents[3].contents[3].next.strip()
        seminar = {
            "date" : date,
            "title" : title,
            "description" : description,
            "link" : link,
            "location" : "Stockholms Universitet"
        }
        events.append(seminar)
    return events


if __name__ == '__main__':
    try:
        events = get_events()
        if events == "":
            print("No events found!")
        else:
            for event in events:
                print("Event: " + ''.join(str(event)) + ")")
    except LookupError as le:
        print(le.message)
