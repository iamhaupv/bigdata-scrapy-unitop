# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class DemofullunitopItem(scrapy.Item):
    courseURL = scrapy.Field()
    title = scrapy.Field()
    desc = scrapy.Field()
    vote = scrapy.Field()
    total = scrapy.Field()
    mentor = scrapy.Field()
