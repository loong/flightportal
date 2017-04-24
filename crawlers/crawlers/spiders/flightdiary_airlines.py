# -*- coding: utf-8 -*-
import scrapy
import json

# [  
#    {  
#       "id":"239",
#       "label":"Lufthansa (LH/DLH)",
#       "value":"Lufthansa (LH/DLH)",
#       "country":"de",
#       "url":"lufthansa-dlh",
#       "iata":"LH",
#       "name":"Lufthansa"
#    },

class AirlineItem(scrapy.Item):
    id = scrapy.Field()
    label = scrapy.Field()
    value = scrapy.Field()
    country = scrapy.Field()
    url = scrapy.Field()
    iata = scrapy.Field()
    name = scrapy.Field()

class FlightdiaryAirlinesSpider(scrapy.Spider):
    name = "flightdiary-airlines"
    allowed_domains = ["flightdiary.net"]
    start_urls = ()

    def start_requests(self):
        with open('airlines.txt') as f:
            lines = f.readlines()

            for l in lines:
                cols = l.split(',')
                code = cols[3][1:-1] # note need to remove ""
                if code == '-' or len(code) == 0:
                    continue

                target = 'http://flightdiary.net/add-flight/search/airline/?term='+code
                yield scrapy.Request(url=target, callback=self.parse)

    def parse(self, response):
        data = json.loads(response.body_as_unicode())

        for d in data:
            if d['label'] == 'No matches':
                continue

            it = AirlineItem()
            it['id'] = d['id']
            it['label'] = d['label']
            it['value'] = d['value']
            it['country'] = d['country']
            it['url'] = d['url']
            it['iata'] = d['iata']
            it['name'] = d['name']

            yield it

