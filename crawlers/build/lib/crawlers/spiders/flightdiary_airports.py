# -*- coding: utf-8 -*-

# Scraping the following pattern:
#      http://flightdiary.net/add-flight/search/airport/?term={IATA CODE}
# run this spider via
#      scrapy crawl flightdiary-airports -t csv -o flightdiary-airports.csv

import scrapy
import json
from pprint import pprint

# "id":"1135",
# "label":"Hong Kong / Hong Kong International (HKG/VHHH)",
# "value":"Hong Kong / Hong Kong International (HKG/VHHH)",
# "country":"hk",
# "url":"hong-kong-hong-kong-international-vhhh",
# "icao":"VHHH",
# "iata":"HKG",
# "lat":"22.308889",
# "lon":"113.914722",
# "name":"Hong Kong / Hong Kong International"

class AirportItem(scrapy.Item):
    id = scrapy.Field()
    label = scrapy.Field()
    value = scrapy.Field()
    country = scrapy.Field()
    url = scrapy.Field()
    icao = scrapy.Field()
    iata = scrapy.Field()
    lat = scrapy.Field()
    lon = scrapy.Field()
    name = scrapy.Field()

class FlightdiaryAirportsSpider(scrapy.Spider):
    name = "flightdiary-airports"
    allowed_domains = ["flightdiary.net"]
    start_urls = ()
    
    def start_requests(self):
        with open('iata_codes.json') as data_file:
            data = json.load(data_file)

            for iata in data["codes"]:
                target = 'http://flightdiary.net/add-flight/search/airport/?term='+iata
                yield scrapy.Request(url=target, callback=self.parse)

    def parse(self, response):
        data = json.loads(response.body_as_unicode())

        for d in data:
            it = AirportItem()
            it['id'] = d['id']
            it['label'] = d['label']
            it['value'] = d['value']
            it['country'] = d['country']
            it['url'] = d['url']
            it['icao'] = d['icao']
            it['iata'] = d['iata']
            it['lat'] = d['lat']
            it['lon'] = d['lon']
            it['name'] = d['name']

            yield it
        
