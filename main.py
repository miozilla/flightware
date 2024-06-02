import asyncio
from scrapy.utils.project import get_project_settings
from datetime import datetime
import sys, subprocess
from fastapi import FastAPI, Query, HTTPException, Depends
from qmongo import MongoDBClient
from pydantic import constr
from bson import ObjectId  # Import ObjectId
import re

# api instance
app = FastAPI(
    docs_url="/api/v2/docs",
    redoc_url="/api/v2/redocs",
    title="FlightwareAPI Platform",
    description="A middleware platform that interacts with the Flightstats website.",
    version="2024.5.31",
    openapi_url="/api/v2/openapi.json"
)

# main project class
class FlightScraper:
    def __init__(self):
        self.settings = get_project_settings()

    # input parameter
    def parse_flight_query_params(self, code: str, num: str, date: str):
        # Check if date parameter is provided
        date_string = None
        if date:
            print("# If provided, parse the date parameter")
            try:
                date_string = datetime.strptime(date, "%Y%m%d").strftime("%Y%m%d")
            except ValueError:
                # If the provided date parameter is not in the correct format, return None
                return None, None, None
        else:
            print("# If not provided, default to current date")
            date_string = datetime.now().strftime("%Y%m%d")
        print(f"Init Arguments: {code} {num} {date_string}")
        return code, num, date_string

    # Async function for stable loose coupling scraping process
    async def async_function(self, flight_code, flight_number, date_string):
        print("2. Triggered async scrapy start task")
        # Simulate a non-blocking I/O operation using asyncio.sleep
        script_path = 'asyncscrapy.py'
        arguments = (flight_code, flight_number, date_string)
        command = [sys.executable, script_path] + list(arguments)
        result = subprocess.run(command, capture_output=True, text=True)
        print(f"Subprocess command: {result}")
        print(result.stdout)
        print(result.stderr, file=sys.stderr)
        await asyncio.sleep(1)  # This will pause the execution for 1 second without blocking
        print("3. Async scrapy task Completed")

# Create an instance of FlightScraper
flight_scraper = FlightScraper()


# --- API endpoint decorator ---

@app.get("/", tags=["Welcome"])
async def home():
    return {"Title": "Hello, Cargobase!", "message": "API is Working!"}

@app.get("/flightware/", tags=["Try Our Services"])
async def read_flight_information(code: str = Query(...), num: str = Query(...), date: str = Query(None)):
    # Parse the query parameters
    flight_code, flight_number, date_string = flight_scraper.parse_flight_query_params(code, num, date)

    # simple input handler
    pattern1 = re.compile(r'\d')
    pattern2 = re.compile(r'[!@#$%^&*(),.?":{}|<>] ')
    pattern3 = re.compile(r'\s')
        
    # Validate the flight code input
    if pattern1.search(flight_code):
        raise HTTPException(status_code=400, detail="Invalid argument")

    if pattern2.search(flight_code):
        raise HTTPException(status_code=501, detail="Symbols are not supported yet in the argument")

    if pattern3.search(flight_code):
        raise HTTPException(status_code=400, detail="Spaces are not allowed in the argument")
    
    # Run the asynchronous function without waiting for it to complete
    print("0. Async API invoked")
    task = asyncio.create_task(flight_scraper.async_function(flight_code, flight_number, date_string))
    print(f"Creating task: {task}")
    print("1. Continuing main without waiting for async task")    
    # Async fixed delay
    await asyncio.sleep(9)
    
    # MongoDB Result Integration
    print("4. Invoke synchronous MongoDB query and wait for returned result")
    
    # Initialize the MongoDBClient object
    db_client = MongoDBClient('myconndb1', 'mycoll1')
    print(str("Debug mior : ") + str(date_string))
    
    # Format the flight departure time
    flight_departure_time = date_string
    if "-" not in date_string: 
        date_obj = datetime.strptime(date_string, "%Y%m%d")
        flight_departure_time = date_obj.strftime("%d-%b-%Y")

    # Construct the flight number
    flightNo = flight_code.upper() + str(" ") + flight_number

    # Construct the query to find documents by flight departure time
    query = {"flightNumber": flightNo, "departure.Flight Departure Times": flight_departure_time}
    
    print(str("DB Query: db_client.find_documents_sorted_by_timestamp(") + str(query) + str(")"))
    mongo_query_result = db_client.find_documents_sorted_by_timestamp(query)

    print(str("Result from db : " + str(mongo_query_result)))
    print(str("Result type : " + str(type(mongo_query_result))))

    # Convert cursor to list to return as JSON
    result_list = []
    for document in mongo_query_result:
        # Convert ObjectId to string for serialization
        document['_id'] = str(document['_id'])
        result_list.append(document)
    print(f"Result from db: {result_list}")
    print(f"Result type: {type(result_list)}")

    if result_list == []:
        result_list = ["No Flight Information : Flight Status Not Available"]
    
    # Close the MongoDB connection
    db_client.close_connection()
    return result_list

@app.put("/integration/", tags=["Try Our Services"])
async def read_root():
    return {"TODO": "Future Enhancement!"}

@app.post("/developer/", tags=["Try Our Services"])
async def read_root():
    return {"TODO": "Future Enhancement!"}

@app.delete("/administration/", tags=["Try Our Services"])
async def read_root():
    return {"TODO": "Future Enhancement!"}

@app.get("/analytics/", tags=["New!"])
async def read_root():
    return {"TODO": "Future Enhancement!"}
