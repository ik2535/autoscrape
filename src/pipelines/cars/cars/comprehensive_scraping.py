import requests
from bs4 import BeautifulSoup
from dagster import op, Out
from typing import List, NamedTuple
import csv
import time
from datetime import datetime
import re
import sys
import os

# Target cities for scraping
TARGET_CITIES = {
    "newyork": "New York, NY",
    "losangeles": "Los Angeles, CA", 
    "chicago": "Chicago, IL",
    "houston": "Houston, TX",
    "philadelphia": "Philadelphia, PA",
    "phoenix": "Phoenix, AZ",
    "sanantonio": "San Antonio, TX",
    "sandiego": "San Diego, CA",
    "dallas": "Dallas, TX",
    "miami": "Miami, FL",
    "atlanta": "Atlanta, GA",
    "boston": "Boston, MA",
    "detroit": "Detroit, MI",
    "seattle": "Seattle, WA",
    "denver": "Denver, CO",
    "lasvegas": "Las Vegas, NV",
    "portland": "Portland, OR",
    "nashville": "Nashville, TN",
    "baltimore": "Baltimore, MD",
    "milwaukee": "Milwaukee, WI",
    "albuquerque": "Albuquerque, NM",
    "tucson": "Tucson, AZ",
    "fresno": "Fresno, CA",
    "sacramento": "Sacramento, CA",
    "kansascity": "Kansas City, MO",
    "mesa": "Mesa, AZ",
    "virginiabeach": "Virginia Beach, VA",
    "omaha": "Omaha, NE",
    "colorado": "Colorado Springs, CO",
    "raleigh": "Raleigh, NC",
    "longbeach": "Long Beach, CA",
    "minneapolis": "Minneapolis, MN",
    "cleveland": "Cleveland, OH",
    "wichita": "Wichita, KS",
    "arlington": "Arlington, TX",
    "bakersfield": "Bakersfield, CA",
    "neworleans": "New Orleans, LA",
    "honolulu": "Honolulu, HI",
    "anaheim": "Anaheim, CA",
    "tampa": "Tampa, FL",
    "aurora": "Aurora, CO",
    "santaana": "Santa Ana, CA",
    "stlouis": "St. Louis, MO",
    "riverside": "Riverside, CA",
    "corpuschristi": "Corpus Christi, TX",
    "lexington": "Lexington, KY",
    "pittsburgh": "Pittsburgh, PA",
    "anchorage": "Anchorage, AK",
    "stockton": "Stockton, CA",
    "cincinnati": "Cincinnati, OH"
}


class CarListing(NamedTuple):
    year: str
    make: str
    model: str
    title: str
    price: str
    mileage: str
    dealer_type: str
    location: str
    link: str
    city: str
    scrape_date: str


def extract_car_details(title: str):
    """Extract year, make, model from title"""
    year_match = re.search(r'\b(19|20)\d{2}\b', title)
    year = year_match.group() if year_match else "N/A"
    
    makes = ['Mercedes-Benz', 'Land Rover', 'Chevrolet', 'Chevy', 'Toyota', 'Honda', 'Ford', 'BMW', 'Audi', 'Volkswagen', 'VW', 
             'Nissan', 'Hyundai', 'Kia', 'Subaru', 'Mazda', 'Lexus', 'Infiniti', 'Acura', 'Cadillac', 
             'Buick', 'GMC', 'Jeep', 'Dodge', 'Chrysler', 'Ram', 'Lincoln', 'Volvo', 'Porsche', 'Tesla',
             'Mitsubishi', 'Suzuki', 'Fiat', 'Mini', 'Jaguar', 'Maserati', 'Ferrari', 'Lamborghini']
    
    make = "N/A"
    for m in makes:
        if re.search(rf'\b{m}\b', title, re.IGNORECASE):
            make = m
            break
    
    model = "N/A"
    if make != "N/A":
        if make == "Mercedes-Benz":
            pattern = r'Mercedes-Benz\s+([A-Za-z0-9-]+(?:\s+[A-Za-z0-9-]+){0,2})'
        else:
            pattern = rf'{make}\s+([A-Za-z0-9-]+(?:\s+[A-Za-z0-9-]+){{0,2}})'
        
        model_match = re.search(pattern, title, re.IGNORECASE)
        if model_match:
            model = model_match.group(1).strip()
            model = re.sub(r'\s+(Touring|Low|miles|dvd|Navi|navigation|backup|camera|owner|since|new|original|AMG|4MATIC|Coupe).*', '', model, flags=re.IGNORECASE)
            model = model.strip()
    
    return year, make, model


def extract_mileage(title: str) -> str:
    """Extract mileage from title"""
    patterns = [
        r'(\d{1,3}[kK])\s*(?:miles?|mi)?',
        r'(\d{1,3},\d{3})\s*(?:original\s+)?(?:miles?|mi)',
        r'(\d{4,6})\s*(?:original\s+)?(?:miles?|mi)',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, title, re.IGNORECASE)
        if match:
            return match.group(1)
    return "N/A"


def extract_price_from_text(text: str) -> str:
    """Extract price from listing text"""
    price_match = re.search(r'\$[\d,]+', text)
    if price_match:
        price = price_match.group()
        clean_price = price.replace('$', '').replace(',', '')
        try:
            float(clean_price)
            return price
        except ValueError:
            pass
    return "N/A"


def extract_location_from_text(text: str) -> str:
    """Extract location from listing text"""
    lines = text.split('\n')
    found_price = False
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        if found_price and '$' not in line and len(line) > 2:
            return line
        
        if '$' in line and re.search(r'\$[\d,]+', line):
            found_price = True
    
    return "N/A"


@op(out=Out(List[CarListing]))
def scrape_car_listings() -> List[CarListing]:
    target_cities = TARGET_CITIES
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    all_listings = []
    scrape_date = datetime.now().strftime("%Y-%m-%d")
    
    for i, (city_code, city_name) in enumerate(target_cities.items(), 1):
        print(f"[{i}/{len(target_cities)}] {city_name}")
        
        try:
            url = f"https://{city_code}.craigslist.org/d/cars-trucks/search/cta"
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.content, "html.parser")
            listings = soup.select("li.cl-static-search-result")
            
            for listing in listings[:100]:
                try:
                    title_tag = (listing.select_one("a[href*='/cto/']") or 
                                listing.select_one("a[href*='/ctd/']") or 
                                listing.select_one("a[href*='/ctp/']") or 
                                listing.select_one("a.cl-app-anchor"))
                    
                    if not title_tag:
                        continue
                        
                    title = title_tag.text.strip()
                    link = title_tag.get("href", "")
                    if link.startswith("/"):
                        link = f"https://{city_code}.craigslist.org" + link
                    
                    year, make, model = extract_car_details(title)
                    mileage = extract_mileage(title)
                    
                    full_text = listing.get_text()
                    
                    price_tag = listing.select_one("span.result-price")
                    if price_tag:
                        price = price_tag.text.strip()
                    else:
                        price = extract_price_from_text(full_text)
                    
                    if "/cto/" in link:
                        dealer_type = "Owner"
                    elif "/ctd/" in link:
                        dealer_type = "Dealer"
                    else:
                        dealer_type = "Private"
                    
                    location_tag = listing.select_one("span.result-hood")
                    if location_tag:
                        location = location_tag.text.strip().replace('(', '').replace(')', '')
                    else:
                        location = extract_location_from_text(full_text)
                    
                    all_listings.append(CarListing(
                        year=year,
                        make=make,
                        model=model,
                        title=title,
                        price=price,
                        mileage=mileage,
                        dealer_type=dealer_type,
                        location=location,
                        link=link,
                        city=city_name,
                        scrape_date=scrape_date
                    ))
                    
                except Exception:
                    continue
            
            time.sleep(1)
            
        except Exception:
            continue
    
    filename = f"car_listings_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["year", "make", "model", "title", "price", "mileage", "dealer_type", "location", "link", "city", "scrape_date"])
        for listing in all_listings:
            writer.writerow(list(listing))
    
    print(f"Saved {len(all_listings)} listings to {filename}")
    return all_listings
