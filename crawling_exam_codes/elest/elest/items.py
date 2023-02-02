# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ElestItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    #pass
    main_category= scrapy.Field()
    sub_category = scrapy.Field()
    ranking= scrapy.Field()
    title= scrapy.Field()
    price= scrapy.Field()
    seller= scrapy.Field()
    link= scrapy.Field()
