# -*- coding: utf-8 -*-
import scrapy


class FlightdiarySpider(scrapy.Spider):
    name = "flightdiary"
    allowed_domains = ["flightdiary.net"]
    start_urls = (
        'http://www.flightdiary.net/',
    )

    def parse(self, response):
        pass
