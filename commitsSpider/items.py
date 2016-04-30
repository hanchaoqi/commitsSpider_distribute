# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose,TakeFirst

class CommitsspiderItem(scrapy.Item):
    # define the fields for your item here like:
    cve = scrapy.Field()
    url = scrapy.Field()
    
class CommitsspiderLoader(ItemLoader):
    default_item_class = CommitsspiderItem
    default_input_processor = MapCompose(lambda s:s.strip())
    default_output_processor = TakeFirst()
