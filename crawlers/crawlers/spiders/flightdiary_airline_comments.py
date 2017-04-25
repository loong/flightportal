# -*- coding: utf-8 -*-
import scrapy
import pkgutil
import json
import time

# "reviewID": "1439471",
# "name": "LasseL",
# "url": "http://flightdiary.net/lepolal",
# "facebook_id": "928117843898428",
# "content": "Used to",
# "time": "2 years ago",
# "reported": null,
# "extra": "",
# "isVoted": false,
# "overallRating": "3",
# "totalReviewsByUser": "12",
# "helpfulPercentage": 84,
# "totalYes": "3",
# "totalNo": "1",
# "subRatings": [
# {
# "id": "640791",
# "review_id": "1439471",
# "sub_rating_id": "15",
# "rating": "3"
# }, ...
# ],
# "currentPage": "1",
# "sortBy": "popularity",
# "totalPages": 7,
# "totalReviews": "31

class ReviewItem(scrapy.Item):
    id = scrapy.Field()
    airline_id = scrapy.Field()
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

class SubReviewItem(scrapy.Item):
    id = scrapy.Field()
    review_id = scrapy.Field()
    sub_rating_id = scrapy.Field()
    rating = scrapy.Field()
    timestamp = scrapy.Field()

class FlightdiaryAirlineCommentsSpider(scrapy.Spider):
    name = "flightdiary-airline-comments"
    allowed_domains = ["flightdiary.net"]
    start_urls = ['http://flightdiary.net/']

    def newReq(self, airline_id, page):
        template = 'http://flightdiary.net/public-scripts/comments/airline/%s/%s/popularity'
        target = template % (airline_id, page)

        req = scrapy.Request(url=target, callback=self.parse)

        # pass additional meta information for reference
        req.meta['airline_id'] = airline_id
        req.meta['page'] = int(page)

        return req

    def start_requests(self):
        data_file = pkgutil.get_data("crawlers", "res/fd-airline-ids.txt")
        for id in data_file.split('\n'):
            yield self.newReq(id, 1)

    def parse(self, response):
        if len(response.body) == 0:
            return
        
        data = json.loads(response.body_as_unicode())
        airline_id = response.meta['airline_id']
        current_page = response.meta['page']
        
        # If this is the first page, add all subsequent pages until
        # totalPages reached to the crawling queue
        if current_page == 1:
             totalPages = int(data[0]['totalPages'])
             for page in range(2, totalPages+1):
                 yield self.newReq(airline_id, page)

        for d in data:
            it = ReviewItem()
            it['id'] = d['reviewID']
            it['airline_id'] = airline_id
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

            # for s in d['subRatings']:
            #     sit = SubReviewItem()
            #     sit['id'] = s['id']
            #     sit['review_id'] = s['review_id']
            #     sit['sub_rating_id'] = s['sub_rating_id']
            #     sit['rating'] = s['rating']
            #     sit['timestamp'] = time.time()

            yield it
