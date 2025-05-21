import requests
from flask import Flask, jsonify, request
from flask_cors import CORS 
import json
from bs4 import BeautifulSoup

app = Flask(__name__)
CORS(app)

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

    def to_dict(self):
        return {
            "make": self.make,
            "model": self.model,
            "mileage": self.mileage,
            "seller_type": self.seller_type,
            "fuel_type": self.fuel_type,
            "transmission": self.transmission,
            "engine_size": self.engine_size,
            "horsepower": self.horsepower,
            "warranty": self.warranty,
            "drive_type": self.drive_type,
            "condition": self.condition,
            "price": self.price,
            "link": self.link,
            "description": self.description,
        }

# Function to fetch car details
def fetch_description(link):
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        response = requests.get(link, headers=headers, timeout=5)
        soup = BeautifulSoup(response.text, 'html.parser')
        description_container = soup.find('div', id='tab-description')
        if description_container:
            description_div = description_container.find('div')
            if description_div:
                return " ".join(description_div.text.strip().split())
        return "No description available"
    except Exception as e:
        return f"Error fetching description: {str(e)}"

@app.route("/search-car", methods=['POST'])
def search_car():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data provided."}), 400

        # Validate input
        required_fields = ['priceMin', 'priceMax', 'kmMin', 'kmMax', 'yearMin', 'yearMax', 'bodyType', 'transmission', 'fuel']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing field: {field}"}), 400

        # Dummy response for demonstration
        car_list = [
            Car("Brand1", "Model1", "50000 km", "Dealer", "Diesel", "Automatic", "2.0L", "150hp", "Yes", "FWD", "Used", "200,000 TL", "https://example.com", "Test description").to_dict(),
            Car("Brand2", "Model2", "30000 km", "Individual", "Petrol", "Manual", "1.6L", "110hp", "No", "AWD", "New", "150,000 TL", "https://example.com", "Another test description").to_dict()
        ]

        return jsonify({"cars": car_list}), 200

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=False)
