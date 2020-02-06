# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AcaspiderItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    authors = scrapy.Field()
    year = scrapy.Field()
    typex = scrapy.Field()
    subjects = scrapy.Field()
    url = scrapy.Field()
    abstract = scrapy.Field()
    citation = scrapy.Field()

