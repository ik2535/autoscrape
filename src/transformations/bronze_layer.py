import pandas as pd
import os
from dagster import op, Out
import glob
from datetime import datetime

@op(out=Out(pd.DataFrame))
def bronze_layer_ingestion() -> pd.DataFrame:
    """Convert latest CSV to Parquet in Bronze layer and return DataFrame"""
    
    latest_csv = max(glob.glob("car_listings_*.csv"), key=os.path.getctime)
    df = pd.read_csv(latest_csv)
    
    # Handle both old (capitalized) and new (lowercase) column formats
    date_col = 'scrape_date' if 'scrape_date' in df.columns else 'Scrape_Date'
    
    df['ingestion_timestamp'] = datetime.now()
    df['data_date'] = pd.to_datetime(df[date_col]).dt.date
    
    # Standardize column names to lowercase
    df.columns = df.columns.str.lower()
    
    # Save to Bronze storage
    date_str = df['data_date'].iloc[0].strftime('%Y-%m-%d')
    output_path = f"storage/bronze/car_listings/date={date_str}/data.parquet"
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_parquet(output_path, index=False)
    
    return df  # Return the DataFrame directly

@op(out=Out(pd.DataFrame))
def load_bronze_data() -> pd.DataFrame:
    """Load all Bronze data"""
    parquet_files = glob.glob("storage/bronze/car_listings/**/*.parquet", recursive=True)
    dfs = [pd.read_parquet(f) for f in parquet_files]
    return pd.concat(dfs, ignore_index=True) if dfs else pd.DataFrame()
