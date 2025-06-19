from dagster import job
from src.transformations.bronze_layer import bronze_layer_ingestion
from src.transformations.silver_layer import silver_layer_transformation, save_silver_data
from src.transformations.gold_layer import gold_layer_aggregation, save_gold_data

@job
def data_processing_pipeline():
    """Process raw CSV data through Bronze → Silver → Gold layers"""
    
    # Bronze: Ingest raw CSV data
    bronze_df = bronze_layer_ingestion()
    
    # Silver: Clean and validate data
    silver_df = silver_layer_transformation(bronze_df)
    silver_path = save_silver_data(silver_df)
    
    # Gold: Create aggregated analytics
    gold_df = gold_layer_aggregation(silver_df)
    gold_path = save_gold_data(gold_df)
