import pandas as pd
import glob

def get_market_summary():
    """Basic market statistics"""
    silver_data = pd.concat([pd.read_parquet(f) for f in glob.glob("storage/silver/car_listings/**/*.parquet", recursive=True)])
    
    return {
        "total_listings": len(silver_data),
        "avg_price": silver_data['price_numeric'].mean(),
        "median_price": silver_data['price_numeric'].median(),
        "avg_mileage": silver_data['mileage_numeric'].mean(),
        "top_make": silver_data['make'].mode()[0],
        "cities_count": silver_data['city'].nunique()
    }

def get_city_rankings():
    """City rankings by price and inventory"""
    gold_data = pd.concat([pd.read_parquet(f) for f in glob.glob("storage/gold/city_analytics/**/*.parquet", recursive=True)])
    
    return {
        "highest_prices": gold_data.nlargest(5, 'avg_price')[['city', 'avg_price']],
        "lowest_prices": gold_data.nsmallest(5, 'avg_price')[['city', 'avg_price']],
        "most_inventory": gold_data.nlargest(5, 'listing_count')[['city', 'listing_count']]
    }

def get_make_stats():
    """Statistics by car make"""
    silver_data = pd.concat([pd.read_parquet(f) for f in glob.glob("storage/silver/car_listings/**/*.parquet", recursive=True)])
    
    return silver_data.groupby('make').agg({
        'price_numeric': ['mean', 'count'],
        'mileage_numeric': 'mean'
    }).round(2)
