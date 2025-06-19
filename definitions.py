from dagster import Definitions
from src.pipelines.cars.cars.comprehensive_pipeline import car_scraping_pipeline, daily_car_scraping_schedule
from src.transformations.data_processing_pipeline import data_processing_pipeline

defs = Definitions(
    jobs=[car_scraping_pipeline, data_processing_pipeline],
    schedules=[daily_car_scraping_schedule]
)
