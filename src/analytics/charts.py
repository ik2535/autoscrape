import pandas as pd
import plotly.express as px
import glob

def load_silver_data():
    """Load clean car data"""
    silver_files = glob.glob("storage/silver/car_listings/**/*.parquet", recursive=True)
    return pd.concat([pd.read_parquet(f) for f in silver_files])

def load_gold_data():
    """Load city analytics data"""
    gold_files = glob.glob("storage/gold/city_analytics/**/*.parquet", recursive=True)
    return pd.concat([pd.read_parquet(f) for f in gold_files])

def city_price_chart():
    """Bar chart of average prices by city"""
    gold_data = load_gold_data()
    fig = px.bar(gold_data.head(15), x='city', y='avg_price', 
                 title='Average Car Prices by City')
    fig.update_xaxes(tickangle=45)
    return fig

def price_distribution():
    """Histogram of car prices"""
    silver_data = load_silver_data()
    valid_prices = silver_data[silver_data['price_numeric'] > 0]
    fig = px.histogram(valid_prices, x='price_numeric', nbins=50,
                       title='Car Price Distribution')
    return fig

def make_analysis():
    """Pie chart of car makes"""
    silver_data = load_silver_data()
    make_counts = silver_data['make'].value_counts().head(10)
    fig = px.pie(values=make_counts.values, names=make_counts.index,
                 title='Car Listings by Make')
    return fig

def city_inventory():
    """Scatter plot of inventory vs price by city"""
    gold_data = load_gold_data()
    fig = px.scatter(gold_data, x='listing_count', y='avg_price',
                     size='listing_count', hover_name='city',
                     title='City Inventory vs Average Price')
    return fig
