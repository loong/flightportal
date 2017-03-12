# -*- coding: utf-8 -*-
#      http://flightdiary.net/public-scripts/comments/airport/{airport_id}/{page}/popularity
# Scraping the following pattern:
#      
# run this spider via
#      scrapy crawl flightdiary-comments -t csv -o flightdiary-airports.csv

import scrapy
import json
import pkgutil
import time

from pprint import pprint

# {
#     "reviewID": "1342180",
#     "name": "Pedro Augusto Marques de",
#     "url": "http://flightdiary.net/PedroAugustoMarques",
#     "facebook_id": "",
#     "content": "Um Aeroporto Bacana Limpo e Organizado, Porem Muito Sem Informa&ccedil;&otilde;es, Saindo de L&aacute; as 04:00 da Manha, e Chegando em Guarulhos as 07:40, Uma Opni&atilde;o Minha e que Tinha que ter mais Informa&ccedil;&otilde;es no Aeroporto de Natal.",
#     "time": "3 years ago",
#     "reported": null,
#     "extra": "",
#     "isVoted": false,
#     "overallRating": "4",
#     "totalReviewsByUser": "1",
#     "helpfulPercentage": 100,
#     "totalYes": "1",
#     "totalNo": "0",
#     "subRatings": {...},
#     "currentPage": "1",
#     "sortBy": "popularity",
#     "totalPages": 1,
#     "totalReviews": "3"
# }

class CommentItem(scrapy.Item):
    id = scrapy.Field()
    airport_id = scrapy.Field()
    page = scrapy.Field()
    
    name = scrapy.Field()
    url = scrapy.Field()
    facebook = scrapy.Field()
    content = scrapy.Field()
    time = scrapy.Field()
    reported = scrapy.Field()
    extra = scrapy.Field()
    is_voted = scrapy.Field()
    rating = scrapy.Field()
    helpful_percentage = scrapy.Field()
    total_yes = scrapy.Field()
    total_no = scrapy.Field()
    timestamp = scrapy.Field()
    
class FlightdiaryCommentsSpider(scrapy.Spider):
    name = "flightdiary-comments"
    allowed_domains = ["flightdiary.net"]
    start_urls = ()

    def newReq(self, airport_id, page):
        template = 'http://flightdiary.net/public-scripts/comments/airport/%s/%s/popularity'
        target = template % (airport_id, page)

        req = scrapy.Request(url=target, callback=self.parse)

        # pass additional meta information for reference
        req.meta['airport_id'] = airport_id
        req.meta['page'] = int(page)

        return req

    def start_requests(self):
        data_file = pkgutil.get_data("crawlers", "res/fd_airport_ids.json")
        for id in json.loads(data_file)["ids"]:
            yield self.newReq(id, 1)

    def parse(self, response):
        if len(response.body) == 0:
            return
        
        data = json.loads(response.body_as_unicode())
        airport_id = response.meta['airport_id']
        current_page = response.meta['page']
        
        # If this is the first page, add all subsequent pages until
        # totalPages reached to the crawling queue
        if current_page == 1:
             totalPages = int(data[0]['totalPages'])
             for page in range(2, totalPages+1):
                 yield self.newReq(airport_id, page)

        for d in data:
            it = CommentItem()
            it['id'] = d['reviewID']
            it['airport_id'] = airport_id
            it['page'] = current_page
            it['name'] = d['name']
            it['url'] = d['url']
            it['facebook'] = d['facebook_id']
            it['content'] = d['content']
            it['time'] = d['time']
            it['reported'] = d['reported']
            it['extra'] = d['extra']
            it['is_voted'] = d['isVoted']
            it['rating'] = d['totalReviewsByUser']
            it['helpful_percentage'] = d['helpfulPercentage']
            it['total_yes'] = d['totalYes']
            it['total_no'] = d['totalNo']
            it['timestamp'] = time.time()

            yield it
