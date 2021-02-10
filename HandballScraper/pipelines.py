# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import mysql.connector
# import connect

# class HandballscraperPipeline:
#     def process_item(self, item, spider):
#         return item
#  ############################################################################################
from HandballScraper.connect import connect_info


class CompetitionPipeline(object):

    def __init__(self):
        self.create_connection()
        self.ids_seen = set()
        # self.create_table()

    def create_connection(self):
        self.connexion = mysql.connector.connect(connect_info)
        self.cursor = self.connexion.cursor()

    def process_item(self, item, spider):
        self.store_db(item)
        return item

    def store_db(self, item):
        self.cursor.execute('''
        SET @cName = %s, @cCategory = %s, @cIdFfd = $s;''', (
            item['competition_name'],
            item['competition_category'],
            item['competition_id_ffh']
        ))
        # Insert competition_level
        self.cursor.execute('''
        INSERT INTO  category (label)
        SELECT * FROM (SELECT @cCategory) AS cTmp
        WHERE NOT EXISTS (
        SELECT label FROM category WHERE label = @hNom) LIMIT 1;''')

        self.connexion.commit()
