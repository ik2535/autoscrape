import pandas as pd
import numpy as np
from dagster import op, In, Out
import os
import re

@op(ins={"bronze_df": In(pd.DataFrame)}, out=Out(pd.DataFrame))
def silver_layer_transformation(bronze_df: pd.DataFrame) -> pd.DataFrame:
    """Clean and standardize data for Silver layer"""
    
    df = bronze_df.copy()
    
    # Clean price column
    df['price_numeric'] = df['price'].str.replace('$', '').str.replace(',', '')
    df['price_numeric'] = pd.to_numeric(df['price_numeric'], errors='coerce')
    
    # Clean mileage column
    df['mileage_numeric'] = df['mileage'].str.replace('k', '000').str.replace('K', '000').str.replace(',', '')
    df['mileage_numeric'] = pd.to_numeric(df['mileage_numeric'], errors='coerce')
    
    # Remove duplicates
    df = df.drop_duplicates(subset=['link'])
    
    # Filter valid data
    df = df[df['year'] != 'N/A']
    df = df[df['make'] != 'N/A']
    df = df[df['price_numeric'] > 500]
    
    return df

@op(ins={"silver_df": In(pd.DataFrame)}, out=Out(str))
def save_silver_data(silver_df: pd.DataFrame) -> str:
    """Save cleaned data to Silver layer"""
    
    date_str = pd.Timestamp.now().strftime('%Y-%m-%d')
    output_path = f"storage/silver/car_listings/date={date_str}/data.parquet"
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    silver_df.to_parquet(output_path, index=False)
    
    return output_path
