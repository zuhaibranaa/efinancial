# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class EfinancialItem(scrapy.Item):
    # define the fields for your item here like:
    _id = scrapy.Field()
    url = scrapy.Field()
    Company = scrapy.Field()
    date = scrapy.Field()
    work = scrapy.Field()
    price = scrapy.Field()
