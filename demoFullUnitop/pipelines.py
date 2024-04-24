# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class DemofullunitopPipeline:
    def process_item(self, item, spider):
        return item

import json

class JsonDBUnitopPipeline:
    def process_item(self, item, spider):
        self.file = open('jsondataunitop.json','a',encoding='utf-8')
        line = json.dumps(dict(item), ensure_ascii=False) + '\n'
        self.file.write(line)
        self.file.close
        return item

import mysql.connector

class MySQLNoDuplicatesPipeline:

    def __init__(self):
        self.conn = mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            password = '123456789',
            database = 'unitop'
        )

        ## Create cursor, used to execute commands
        self.cur = self.conn.cursor()
        
        ## Create quotes table if none exists
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS unitop(
            id int NOT NULL auto_increment, 
            courseURL text,
            title text,
            description text,
            vote text,
            total text,
            mentor text,
            PRIMARY KEY (id)
        )
        """)



    def process_item(self, item, spider):

        ## Check to see if courseURL is already in database 
        self.cur.execute("select * from unitop where courseURL = %s", (item['courseURL'],))
        result = self.cur.fetchone()

        ## If it is in DB, create log message
        if result:
            spider.logger.warn("Item already in database: %s" % item['courseURL'])


        ## If text isn't in the DB, insert data
        else:

            ## Define insert statement
            self.cur.execute(""" insert into unitop (courseURL, title, description, vote, total, mentor) values (%s,%s,%s,%s,%s,%s)""", (
            item["courseURL"],
            item["title"],
            item["description"],
            item["vote"],
            item["total"],
            item["mentor"],
        ))

            ## Execute insert of data into database
            self.conn.commit()
        return item

    
    def close_spider(self, spider):

        ## Close cursor & connection to database 
        self.cur.close()
        self.conn.close()

