# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Pro2Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class programmable(scrapy.Item):
    """docstring for ClassName"""
    API_Name = scrapy.Field()
    API_ID = scrapy.Field()
    Description = scrapy.Field()
    Primary_Category = scrapy.Field()
    Secondary_Categories = scrapy.Field()
    Followers_Number = scrapy.Field()
    Followers_Id = scrapy.Field()
    API_Homepage=scrapy.Field()


class followers(scrapy.Item):
    API_ID = scrapy.Field()
    Followers_Name = scrapy.Field()


class mushup(scrapy.Item):
    API_ID = scrapy.Field()
    mushup_name = scrapy.Field()
