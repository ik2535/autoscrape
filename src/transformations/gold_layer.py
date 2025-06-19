import pandas as pd
from dagster import op, In, Out
import os

@op(ins={"silver_df": In(pd.DataFrame)}, out=Out(pd.DataFrame))
def gold_layer_aggregation(silver_df: pd.DataFrame) -> pd.DataFrame:
    """Create aggregated analytics data for Gold layer"""
    
    # City-level aggregations
    city_stats = silver_df.groupby('city').agg({
        'price_numeric': ['mean', 'median', 'count'],
        'mileage_numeric': 'mean',
        'year': 'mean'
    }).round(2)
    
    city_stats.columns = ['avg_price', 'median_price', 'listing_count', 'avg_mileage', 'avg_year']
    city_stats = city_stats.reset_index()
    
    return city_stats

@op(ins={"gold_df": In(pd.DataFrame)}, out=Out(str))
def save_gold_data(gold_df: pd.DataFrame) -> str:
    """Save aggregated data to Gold layer"""
    
    date_str = pd.Timestamp.now().strftime('%Y-%m-%d')
    output_path = f"storage/gold/city_analytics/date={date_str}/data.parquet"
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    gold_df.to_parquet(output_path, index=False)
    
    return output_path
