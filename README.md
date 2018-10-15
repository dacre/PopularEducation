# PopularEducation

This project aims to collect Swedish (first out Stockholm) public seminars in a easy to access and easy to search manner so that people easier can educate themselves in interesting topics.

Currently Stockholm University and Folkuniversitet are supported from a scraping point of view. The results are put in a HTML table. 

Some of the planned work:
- make the frontend
-- Ideas:
--- https://getbootstrap.com/docs/4.0/components/list-group/#custom-content 
--- https://foundation.zurb.com/building-blocks/blocks/dashboard-table.html
--- https://bootsnipp.com/snippets/peZX7
- add more sources (KTH and ABF for example)
-- ABF basis: curl --header "X-PJAX: true" "http://abfstockholm.se/kalendarium/?subject=Alla&when=1&event_tags=Alla&location=Alla&time=Alla&coorganizer=Alla&category=Alla&price=Alla&ref_date=2018-10-15&till=Alla&advanced_search=0&fav=0"
- deploy to a real domain (find good domain name!)
- setup with Let's Encrypt
- setup with Ansible or similar to simplify VPS switch in the future
- add analytics using access log analysis, possibly via https://goaccess.io/
