import streamlit as st
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from analytics.charts import city_price_chart, price_distribution, make_analysis, city_inventory
from analytics.metrics import get_market_summary, get_city_rankings, get_make_stats

st.title("🚗 AutoScrape Analytics Dashboard")

# Market Summary
st.header("📊 Market Overview")
summary = get_market_summary()

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Listings", f"{summary['total_listings']:,}")
    st.metric("Average Price", f"${summary['avg_price']:,.0f}")

with col2:
    st.metric("Median Price", f"${summary['median_price']:,.0f}")
    st.metric("Average Mileage", f"{summary['avg_mileage']:,.0f}")

with col3:
    st.metric("Cities Analyzed", summary['cities_count'])
    st.metric("Top Make", summary['top_make'])

# Charts
st.header("📈 Price Analysis")
st.plotly_chart(city_price_chart(), use_container_width=True)

col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(price_distribution(), use_container_width=True)
with col2:
    st.plotly_chart(make_analysis(), use_container_width=True)

st.plotly_chart(city_inventory(), use_container_width=True)

# Rankings
st.header("🏆 City Rankings")
rankings = get_city_rankings()

col1, col2, col3 = st.columns(3)
with col1:
    st.subheader("Highest Prices")
    st.dataframe(rankings['highest_prices'])

with col2:
    st.subheader("Lowest Prices") 
    st.dataframe(rankings['lowest_prices'])

with col3:
    st.subheader("Most Inventory")
    st.dataframe(rankings['most_inventory'])

# Make Analysis
st.header("🚙 Analysis by Make")
make_stats = get_make_stats()
st.dataframe(make_stats)
