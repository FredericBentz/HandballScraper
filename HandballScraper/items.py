# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CompetitionItem(scrapy.Item):
    competition_name = scrapy.Field()
    competition_level = scrapy.Field()
    competition_id_ffh = scrapy.Field()


class HandballscraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    team_name = scrapy.Field()

    pass
