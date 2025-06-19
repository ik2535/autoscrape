# AutoScrape - Automotive Data Engineering Pipeline

A comprehensive data engineering project for scraping, processing, and analyzing automotive marketplace data from 50 major US cities.

## 🎯 Project Overview

AutoScrape implements a complete data lakehouse architecture for automotive market intelligence, following the Bronze → Silver → Gold data processing pattern.

## 🏗️ Architecture

```
Phase 1: Data Extraction ✅
├── Web scraping from Craigslist (50 cities)
├── Scheduled daily collection (Dagster)
└── Raw CSV output

Phase 2: Data Lake Architecture ✅  
├── Bronze Layer: Raw data → Parquet format
├── Silver Layer: Cleaned, validated data
└── Gold Layer: Aggregated city analytics

Phase 3: Analytics & BI (Next)
├── Interactive dashboards
├── Time series analysis
└── Geographic insights
```

## 📊 Data Pipeline

**Extraction:**
- 50 major US cities
- Car listings (year, make, model, price, mileage)
- Owner/Dealer classification
- Geographic metadata

**Processing:**
- Data validation and cleaning
- Price standardization ($15,000 → 15000)
- Mileage normalization (74k → 74000)
- Duplicate removal

**Analytics:**
- City-level aggregations
- Market price analysis
- Inventory insights

## 🚀 Quick Start

### Prerequisites
```bash
pip install -r requirements.txt
```

### Run Data Pipeline

**1. Extract car data (50 cities):**
```bash
dagster job execute -f definitions.py -j car_scraping_pipeline
```

**2. Process data (Bronze → Silver → Gold):**
```bash
dagster job execute -f definitions.py -j data_processing_pipeline
```

**3. Set up daily automation:**
```bash
start_scheduler.bat
```

## 📁 Project Structure

```
AutoScrape/
├── src/
│   ├── pipelines/cars/cars/           # Data extraction
│   └── transformations/               # Data processing
├── storage/                           # Data lake
│   ├── bronze/                       # Raw data
│   ├── silver/                       # Clean data
│   └── gold/                         # Analytics
├── config/                           # Configuration
└── requirements.txt                  # Dependencies
```

## 🔧 Technologies

- **Orchestration:** Dagster
- **Data Processing:** Pandas, PyArrow
- **Storage:** Parquet (Columnar format)
- **Scraping:** BeautifulSoup, Requests
- **Infrastructure:** Python, CSV → Parquet

## 📈 Expected Output

- **2,500-5,000+ car listings** per run
- **City-level analytics** (avg price, inventory count)
- **Clean, structured data** ready for ML/BI tools
- **Daily automated collection**

## 🎯 Use Cases

- Automotive market research
- Price trend analysis
- Geographic market insights
- Inventory optimization
- Competitive intelligence

## 📋 Status

- ✅ Phase 1: Data Extraction (Complete)
- ✅ Phase 2: Data Lake Architecture (Complete)  
- 🚧 Phase 3: Analytics & BI (In Progress)

## 🔄 Data Flow

```
Raw CSV → Bronze (Parquet) → Silver (Clean) → Gold (Analytics)
```

**Sample Output:**
```
City Analytics (Gold Layer):
- New York, NY: Avg $18,500, 250 listings
- Los Angeles, CA: Avg $16,200, 180 listings  
- Chicago, IL: Avg $15,800, 165 listings
```
