# -*- coding: utf-8 -*-
import scrapy
import pkgutil
import time
import json

from pprint import pprint
import BeautifulSoup

# "6": [
#     "2017-03-05",
#     "TK1971",
#     "<a href=\"http://flightdiary.net/airport/istanbul-ataturk-ltba\" class=\"show-hovercard\" data-hovercard-content=\"Istanbul / Ataturk\">IST</a>",
#     "<a href=\"http://flightdiary.net/airport/london-heathrow-egll\" class=\"show-hovercard\" data-hovercard-content=\"London / Heathrow\">LHR</a>",
#     "14:55",
#     "16:15",
#     "<a href=\"http://flightdiary.net/airline/turkish-airlines-thy\" class=\"show-hovercard\" data-hovercard-content=\"Turkish Airlines\">THY</a>",
#     "<a href=\"http://flightdiary.net/aircraft/airbus-a330-300-a333\" class=\"show-hovercard\" data-hovercard-content=\"Airbus A330-300\">A333</a>",
#     "TC-JNJ",
#     "11A <span class=\"show-hovercard\" data-hovercard-content=\"Window\">(W)</span>",
#     "",
#     "<img src=\"http://flightdiary.net/img/icon-economy.png\" class=\"show-hovercard\" data-hovercard-content=\"Economy\" />\r\n\t\t\t\t\t<img src=\"http://flightdiary.net/img/icon-leisure.png\" class=\"show-hovercard\" data-hovercard-content=\"Leisure\" />\r\n\t\t\t\t\t",
#     "1 563"
# ],

class FlightItem(scrapy.Item):
    user = scrapy.Field()
    page = scrapy.Field()

    date = scrapy.Field()
    flight_no = scrapy.Field()
    from_iata = scrapy.Field()
    to_iata = scrapy.Field()
    departure_time = scrapy.Field()
    arrival_time = scrapy.Field()
    airline = scrapy.Field()
    aircraft = scrapy.Field()
    aircraft_reg = scrapy.Field()
    seat = scrapy.Field()
    
    distance_mile = scrapy.Field()
    timestamp = scrapy.Field()
        

class FlightdiaryFlightsSpider(scrapy.Spider):
    name = "flightdiary-flights"
    allowed_domains = ["flightdiary.net"]
    start_urls = ()

    def getUser(self, url):
        return url.split('/')[-1]

    def newReq(self, user, page):
        template = 'http://flightdiary.net/public-scripts/flight-list/%s/%s/'
        target = template % (user, page*50+1)

        req = scrapy.Request(url=target, callback=self.parse)

        # pass additional meta information for reference
        req.meta['user'] = user
        req.meta['page'] = int(page)

        return req

    def getText(self, src):
        soup = BeautifulSoup.BeautifulSoup(src)
        return ''.join(soup.findAll(text=True))
    
    def start_requests(self):
        data_file = pkgutil.get_data("crawlers", "res/fd_profile_urls.json")
        for url in json.loads(data_file)["urls"]:
            user = self.getUser(url)
            yield self.newReq(user, 1)
            
    def parse(self, response):
        data = json.loads(response.body_as_unicode())
        user = response.meta['user']
        page = response.meta['page']

        if len(data) == 0:
            return

        yield self.newReq(user, page+1)

        for k in data:
            d = data[k]
            it = FlightItem()
            
            it['user'] = user
            it['page'] = page
            it['date'] = d[0]
            it['flight_no'] = d[1]
            it['from_iata'] = self.getText(d[2])
            it['to_iata'] = self.getText(d[3])
            it['departure_time'] = d[4]
            it['arrival_time'] = d[5]
            it['airline'] = self.getText(d[6])
            it['aircraft'] = self.getText(d[7])
            it['aircraft_reg'] = d[8]
            it['seat'] = self.getText(d[9]).replace(' ', '')
            it['distance_mile'] = d[-1].replace(' ', '')
            it['timestamp'] = int(time.time())

            # turns empty fields to None fields
            it = {k: None if v=='' else v for k, v in it.items()}
                    
            yield it
