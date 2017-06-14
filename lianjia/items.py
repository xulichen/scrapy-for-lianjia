# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class LianjiaItem(Item):
    title = Field()
    condition1 = Field()
    condition2 = Field()
    condition3 = Field()
    room_compose = Field()
    room_spare = Field()
    subway = Field()
    floor = Field()
    direction = Field()
    price = Field()
    upload = Field()
    lookat_num =Field()



