import sys
sys.stdout.reconfigure(encoding='utf-8')  # Force UTF-8 encoding for console output

import requests
from bs4 import BeautifulSoup

# Define the Car class
class Car:
    def __init__(self, make, model, mileage, seller_type, fuel_type, transmission, engine_size, horsepower, warranty, drive_type, condition, price, link, description=None):
        self.make = make
        self.model = model
        self.mileage = mileage
        self.seller_type = seller_type
        self.fuel_type = fuel_type
        self.transmission = transmission
        self.engine_size = engine_size
        self.horsepower = horsepower
        self.warranty = warranty
        self.drive_type = drive_type
        self.condition = condition
        self.price = price
        self.link = link
        self.description = description

    def __repr__(self):
        return (
            f"\n"
            f"------------------------------------------------------------\n"
            f"Car Details:\n"
            f"  Make: {self.make}\n"
            f"  Model: {self.model}\n"
            f"  Mileage: {self.mileage}\n"
            f"  Seller Type: {self.seller_type}\n"
            f"  Fuel Type: {self.fuel_type}\n"
            f"  Transmission: {self.transmission}\n"
            f"  Engine Size: {self.engine_size}\n"
            f"  Horsepower: {self.horsepower}\n"
            f"  Warranty: {self.warranty}\n"
            f"  Drive Type: {self.drive_type}\n"
            f"  Condition: {self.condition}\n"
            f"  Price: {self.price}\n"
            f"  Link: {self.link}\n"
            f"  Description: {self.description}\n"
            f"------------------------------------------------------------\n"
        )

# Function to construct the URL based on parameters
def construct_url(make, model, transmission, fuel_type, min_price=None, max_price=None, min_year=None, max_year=None, min_km=None, max_km=None, body_type=None):
    base_url = "https://www.arabam.com/ikinci-el/otomobil"
    
    # Add search text for the model (if present)
    search_text = model if model else ""
    
    # Start constructing query parameters
    query_params = {
        "currency": "TL",
        "minPrice": min_price,
        "maxPrice": max_price,
        "minYear": min_year,
        "maxYear": max_year,
        "minkm": min_km,
        "maxkm": max_km,
        "bodytype": body_type,
        "searchText": search_text,
        "view": "Detailed",
        "take": 10,
        "sort": "km.asc",
    }
    
    # Remove parameters with values None or 0
    valid_params = {key: value for key, value in query_params.items() if value not in [None, 0]}
    
    # Create the query string
    query_string = "&".join(f"{key}={value}" for key, value in valid_params.items())
    
    # Handle make and model in the URL's path only if transmission and fuel_type are given
    if transmission and fuel_type:
        return f"{base_url}-{transmission}-{fuel_type}?{query_string}"
    else:
        return f"{base_url}?{query_string}"

# Function to fetch the "Açıklama" section from a car link
def fetch_description(link):
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        response = requests.get(link, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Locate the "Açıklama" section by ID
        description_container = soup.find('div', id='tab-description')
        if description_container:
            description_div = description_container.find('div')  # Locate the inner <div> containing the text
            return description_div.text.strip().replace('\xa0', ' ') if description_div else "No description available"
        else:
            return "No description available"
    except Exception as e:
        print(f"Error fetching description from {link}: {e}")
        return "Error fetching description"

# Function to fetch cars from the constructed URL
def fetch_cars(url):
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    car_listings = []

    # Find all <div> elements with class "content-container"
    containers = soup.find_all('div', class_='content-container')
    for container in containers:
        try:
            # Extract model information
            model_tag = container.find('h4', itemprop='name', class_='model-name')
            model_string = model_tag.text.strip() if model_tag else "Unknown"
            make, model = model_string.split(" ", 1) if " " in model_string else ("Unknown", model_string)

            # Extract price
            price_tag = container.find('div', class_='price-container')
            price_span = price_tag.find('span', class_='price') if price_tag else None
            price = price_span.text.strip() if price_span else "Unknown"

            # Extract link
            link_tag = model_tag.find_parent('a') if model_tag else None
            link = f"https://www.arabam.com{link_tag['href']}" if link_tag and 'href' in link_tag.attrs else "Unknown"

            # Extract details from <div class="row mt8">
            details_container = container.find('div', class_='row mt8')
            if details_container:
                details = details_container.find_all('span', class_='property-value')
                mileage = details[0].text.strip() if len(details) > 0 else "Unknown"
                seller_type = details[1].text.strip() if len(details) > 1 else "Unknown"
                fuel_type = details[2].text.strip() if len(details) > 2 else "Unknown"
                transmission = details[3].text.strip() if len(details) > 3 else "Unknown"
                engine_size = details[4].text.strip() if len(details) > 4 else "Unknown"
                horsepower = details[5].text.strip() if len(details) > 5 else "Unknown"
                warranty = details[6].text.strip() if len(details) > 6 else "Unknown"
                drive_type = details[7].text.strip() if len(details) > 7 else "Unknown"
                condition = details[8].text.strip() if len(details) > 8 else "Unknown"
            else:
                mileage = seller_type = fuel_type = transmission = engine_size = horsepower = warranty = drive_type = condition = "Unknown"

            # Create a Car object
            car = Car(make, model, mileage, seller_type, fuel_type, transmission, engine_size, horsepower, warranty, drive_type, condition, price, link)
            if make != "Unknown":
                car_listings.append(car)
        except Exception as e:
            print(f"Error parsing container: {e}")

    return car_listings

# Main function to take parameters and search
def main():
    # Example parameters
    make = ""
    model = ""
    transmission = "otomatik"
    fuel_type = "Benzin"
    min_price = 1000000
    max_price = 1500000
    min_year = 2013
    max_year = 2017
    min_km = 35000
    max_km = 100000
    body_type = "Sedan"

    # Construct the search URL
    url = construct_url(make, model, transmission, fuel_type, min_price, max_price, min_year, max_year, min_km, max_km, body_type)
    print(f"Searching URL: {url}")

    # Fetch and display cars
    cars = fetch_cars(url)
    print(f"Total cars fetched: {len(cars)}")
    for car in cars:
        car.description = fetch_description(car.link)  # Fetch and attach the description for each car
        print(car)

if __name__ == "__main__":
    main()
