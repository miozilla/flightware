# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class FlightscrapeItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    flightNumber = scrapy.Field()
    airLine = scrapy.Field()
    origin = scrapy.Field()
    destination = scrapy.Field()
    status = scrapy.Field()
    dStatus = scrapy.Field()
    departure = scrapy.Field()
    arrival = scrapy.Field()
    timestamp = scrapy.Field()
    # pass
