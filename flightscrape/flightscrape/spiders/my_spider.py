import scrapy
import sys
from datetime import datetime
from ..items import FlightscrapeItem


# main spider class
class MySpider(scrapy.Spider):
    name = 'my_spider'

     # Custom pipeline settings specific to this spider
    custom_settings = {
        'ITEM_PIPELINES': {
            'flightscrape.flightscrape.pipelines.FlightscrapePipeline': 300,
        },
    }

    # initialize args
    def __init__(self, arg1=None, arg2=None, arg3=None, *args, **kwargs):
        super(MySpider, self).__init__(*args, **kwargs)
        self.arg1 = arg1
        self.arg2 = arg2
        self.arg3 = arg3 if arg3 else datetime.now().strftime('%Y%m%d')

        # Extract year, month, and date from arg3
        self.year = self.arg3[:4]
        self.month = self.arg3[4:6]
        self.date = self.arg3[6:8]

    # flighstats url init
    def start_requests(self):
        url = f'https://www.flightstats.com/v2/flight-tracker/{self.arg1}/{self.arg2}?year={self.year}&month={self.month}&date={self.date}'
        yield scrapy.Request(url=url, callback=self.parse)

    # scrape fligstats page
    def parse(self, response):
        # Implement your parsing logic here
        self.log(f'Arg1: {self.arg1}, Arg2: {self.arg2}, Arg3: {self.arg3}')
        self.log(f'Response body: {response.body}')
        # Example: extracting data
        # title = response.xpath('//title/text()').get()
        # yield {'title': title}

        # Extract flight status information
        status_available = response.css('div.text-helper__TextHelper-sc-8bko4a-0::text').getall()
        status_na = response.css('h2.layout-row__Title-sc-1uoco8s-4::text').get()

        if status_available:
            print("########## Available ##########")
            print(str("Status: ") + str(status_available))
            print("##########  end1  ##########")
            item_count = len(status_available)
            print(f"ItemCount: {item_count}")
            print("##########  end1  ##########")

        elif status_na:
            print("########## N/A ##########")
            print(str("Status NA: ") + str(status_na))
            print("########## Debug2 ##########")
            print(str("Status Avail: ") + str(status_available))
            print("##########  Debug2  ##########")
            print("##########  end2  ##########")
            return
        else:
            print("########## No Flight Status ##########")
            print(str("Status NA: ") + str(status_na))
            print(str("Status Avail: ") + str(status_available))
            print("!!! THIS FLIGHT COULD NOT BE LOCATED IN OUR SYSTEM OR DATE IS OUT OF RANGE !!!")
            print("##########  end3  ##########")
            self.log('No <div> found with the specified criteria.')
            return

        keys1 = ["flightNumber", "airLine", "origin", "destination", "status", "dStatus"]

        # Combine the lists into a dictionary
        data_dict = dict(zip(keys1, status_available))

        print(str("data_dict type : ") + str(type(data_dict.get('flightNumber'))))

        # Create an instance of TutorialItem
        items = FlightscrapeItem()
        items['flightNumber'] = data_dict.get('flightNumber')
        items['airLine'] = data_dict.get('airLine')
        items['origin'] = data_dict.get('origin')
        items['destination'] = data_dict.get('destination')
        items['status'] = data_dict.get('status')
        items['dStatus'] = data_dict.get('dStatus')
        # Departure/Arrival information
        departure_info = {
            'location': status_available[6],
            'airport': status_available[7],
            }
        # Extend the departure_info dictionary with dynamically created pairs
        for i in range(8, 14, 2):
            departure_info[status_available[i]] = status_available[i+1]
        items['departure'] = departure_info

        arrival_info = {
        'location': status_available[18],
        'airport': status_available[19]
        }
        for i in range(20, len(status_available), 2):
            arrival_info[status_available[i]] = status_available[i+1]
        items['arrival'] = arrival_info
        sekarang = str(datetime.now())
        print(str("Now is: ")+str(datetime.now()))
        items['timestamp'] = sekarang

        print("DEBUG : Yield")
        # Yield the item
        yield items
