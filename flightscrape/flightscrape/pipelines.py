# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymongo


# mirror result to mongodb
class FlightscrapePipeline:

    def __init__(self):
        self.conn = pymongo.MongoClient('localhost', 27017)        
        db = self.conn['myconndb1']
        self.collection = db['mycoll1']

    # inset items document into collection in db
    def process_item(self, item, spider):
        print(str("***** Debug Pipeline ***** : ") + str(type(item)))
        self.collection.insert_one(dict(item))
        return item

