import sys
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from flightscrape.flightscrape.spiders.my_spider import MySpider

settings = get_project_settings()

'''
# if __name__ == "__main__":
#     print("Start process.crawl")
#     process = CrawlerProcess(settings)
#     process.crawl(MySpider, arg1="HA", arg2="68", arg3="20240529")
#     process.start()
#     print("End process.crawl")
'''

class singletonThread():
    def run_spider(arg1, arg2, arg3):
        print(str("Start process.crawl + ")+ str(arg1) + str(" ") + str(arg2) + str(" ") + str(arg3))
        settings = get_project_settings()
        process = CrawlerProcess(settings)
        process.crawl(MySpider, arg1=arg1, arg2=arg2, arg3=arg3)
        process.start()
        print(str("End process.crawl"))


if __name__ == "__main__":
    # Check if three arguments are provided
    if len(sys.argv) != 4:
        print("Usage: asyncscrapy.py <arg1> <arg2> <arg3>")
        sys.exit(1)
    
    arg1 = sys.argv[1]
    arg2 = sys.argv[2]
    arg3 = sys.argv[3]

    print(str("asyncscrapy start"))
    singletonThread.run_spider(arg1, arg2, arg3)
    print(str("asyncscrapy finished"))

