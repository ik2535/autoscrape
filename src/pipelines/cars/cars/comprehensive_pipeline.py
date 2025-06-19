from dagster import job, schedule, DefaultScheduleStatus
from src.pipelines.cars.cars.comprehensive_scraping import scrape_car_listings

@job
def car_scraping_pipeline():
    """
    Car scraping pipeline for 50 major US cities
    
    Scrapes car listings from Craigslist across the top 50 US cities
    for comprehensive automotive market data.
    
    Expected output: 2,500-5,000+ car listings
    Estimated time: 1-2 hours
    
    Output file: car_listings_YYYYMMDD_HHMMSS.csv
    """
    scrape_car_listings()


@schedule(
    job=car_scraping_pipeline,
    cron_schedule="0 2 * * *",  # Daily at 2 AM
    default_status=DefaultScheduleStatus.RUNNING
)
def daily_car_scraping_schedule():
    """
    Schedule to run car scraping daily at 2 AM
    
    This will automatically scrape car listings from 50 US cities
    every day at 2 AM to capture fresh automotive market data.
    """
    return {}


# Alternative schedules you can use instead:

# @schedule(
#     job=car_scraping_pipeline, 
#     cron_schedule="0 6 * * 1",  # Weekly on Monday at 6 AM
#     default_status=DefaultScheduleStatus.STOPPED
# )
# def weekly_car_scraping_schedule():
#     """Weekly car scraping every Monday"""
#     return {}

# @schedule(
#     job=car_scraping_pipeline,
#     cron_schedule="0 8 * * 1,3,5",  # Mon, Wed, Fri at 8 AM  
#     default_status=DefaultScheduleStatus.STOPPED
# )
# def mwf_car_scraping_schedule():
#     """Car scraping Monday, Wednesday, Friday"""
#     return {}
