import requests
from bs4 import BeautifulSoup

class Car:
    def __init__(self, images=None, description="", paint_info="", km="", price="", year="", brand="", serie="", transmission="", fuel_type="", body_type="", model="", ilan_no="", renk="", motor_hacmi="", motor_gucu="", cekis="", arac_durumu="", ort_yakit_tuketimi="", depo="", boya_degisen="", takasa_uygun="", kimden="", original_parts=None, changed_parts=None, painted_parts=None, local_painted_parts=None):
        self.images = images if images else []
        self.description = description
        self.paint_info = paint_info
        self.km = km
        self.price = price
        self.year = year
        self.brand = brand
        self.serie = serie
        self.transmission = transmission
        self.fuel_type = fuel_type
        self.body_type = body_type
        self.model = model
        self.ilan_no = ilan_no
        self.renk = renk
        self.motor_hacmi = motor_hacmi
        self.motor_gucu = motor_gucu
        self.cekis = cekis
        self.arac_durumu = arac_durumu
        self.ort_yakit_tuketimi = ort_yakit_tuketimi
        self.depo = depo
        self.boya_degisen = boya_degisen
        self.takasa_uygun = takasa_uygun
        self.kimden = kimden
        self.original_parts = original_parts if original_parts else []
        self.changed_parts = changed_parts if changed_parts else []
        self.painted_parts = painted_parts if painted_parts else []
        self.local_painted_parts = local_painted_parts if local_painted_parts else []

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        details = [
            f"Description: {self.description[:100]}...", 
            f"Price: {self.price}",
            f"Year: {self.year}",
            f"Brand: {self.brand}",
            f"Serie: {self.serie}",
            f"Model: {self.model}",
            f"Transmission: {self.transmission}",
            f"Fuel Type: {self.fuel_type}",
            f"Body Type: {self.body_type}",
            f"Kilometre: {self.km}",
            f"Color: {self.renk}",
            f"Engine Volume: {self.motor_hacmi}",
            f"Engine Power: {self.motor_gucu}",
            f"Drive: {self.cekis}",
            f"Condition: {self.arac_durumu}",
            f"Avg. Fuel Consumption: {self.ort_yakit_tuketimi}",
            f"Fuel Tank: {self.depo}",
            f"Paint/Change Info: {self.boya_degisen}",
            f"Trade-In: {self.takasa_uygun}",
            f"Seller Type: {self.kimden}",
            f"Original Parts: {', '.join(self.original_parts) if self.original_parts else 'None'}",
            f"Changed Parts: {', '.join(self.changed_parts) if self.changed_parts else 'None'}",
            f"Painted Parts: {', '.join(self.painted_parts) if self.painted_parts else 'None'}",
            f"Locally Painted Parts: {', '.join(self.local_painted_parts) if self.local_painted_parts else 'None'}",
        ]
        return "\n".join(details)

def scrape_car_data(url):
    try:
        # Send a GET request to the URL
        response = requests.get(url)
        response.raise_for_status()

        # Handle encoding explicitly for Turkish characters
        response.encoding = response.apparent_encoding

        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract car images
        images = []
        for img_tag in soup.select('img'):  # Adjust the selector based on site structure
            img_url = img_tag.get('src')
            if img_url and 'http' in img_url:
                images.append(img_url)

        # Extract the seller's description
        description_section = soup.find('div', id='tab-description')  # Updated selector
        description_text = description_section.get_text(strip=True) if description_section else ""

        # Extract "Paint, Changing, and Tramer" information
        paint_info_section = soup.find('div', class_='paint-info')  # Adjust based on site structure
        paint_info_text = paint_info_section.get_text(strip=True) if paint_info_section else ""

        # Extract car price
        price_section = soup.find('div', {'data-testid': 'desktop-information-price'})
        price_text = price_section.get_text(strip=True) if price_section else ""

        # Extract additional details
        def get_property_value(key):
            properties_section = soup.find('div', class_='product-properties-details')
            if not properties_section:
                return ""
            for item in properties_section.find_all('div', class_='property-item'):
                key_element = item.find('div', class_='property-key')
                value_element = item.find('div', class_='property-value')
                if key_element and key_element.get_text(strip=True) == key:
                    return value_element.get_text(strip=True) if value_element else ""
            return ""

        km_text = get_property_value("Kilometre")
        year_text = get_property_value("Yıl")
        brand_text = get_property_value("Marka")
        serie_text = get_property_value("Seri")
        transmission_text = get_property_value("Vites Tipi")
        fuel_type_text = get_property_value("Yakıt Tipi")
        body_type_text = get_property_value("Kasa Tipi")
        model_text = get_property_value("Model")
        ilan_no = get_property_value("İlan No")
        renk = get_property_value("Renk")
        motor_hacmi = get_property_value("Motor Hacmi")
        motor_gucu = get_property_value("Motor Gücü")
        cekis = get_property_value("Çekiş")
        arac_durumu = get_property_value("Araç Durumu")
        ort_yakit_tuketimi = get_property_value("Ort. Yakıt Tüketimi")
        depo = get_property_value("Yakıt Deposu")
        boya_degisen = get_property_value("Boya-değişen")
        takasa_uygun = get_property_value("Takasa Uygun")
        kimden = get_property_value("Kimden")

        # Extract car damage info
        original_parts = []
        changed_parts = []
        painted_parts = []
        local_painted_parts = []

        damage_section = soup.find('div', class_='car-damage-info')
        if damage_section:
            # Iterate through all damage items
            for item in damage_section.find_all('div', class_='car-damage-info-item'):
                header_text = item.find('p').get_text(strip=True) if item.find('p') else ""

                # Check for original parts
                if "Orjinal" in header_text:
                    original_parts = [li.get_text(strip=True) for li in item.find_all('li') if li.get_text(strip=True)]

                # Check for changed parts
                elif "Değişmiş" in header_text:
                    changed_parts = [li.get_text(strip=True) for li in item.find_all('li') if li.get_text(strip=True)]

                # Check for painted parts
                elif "Boyalı" in header_text:
                    painted_parts = [li.get_text(strip=True) for li in item.find_all('li') if li.get_text(strip=True)]

                # Check for locally painted parts
                elif "Lokal boyalı" in header_text:
                    local_painted_parts = [li.get_text(strip=True) for li in item.find_all('li') if li.get_text(strip=True)]

        # Store in the Car class
        car = Car(
            images=images,
            description=description_text,
            paint_info=paint_info_text,
            km=km_text,
            price=price_text,
            year=year_text,
            brand=brand_text,
            serie=serie_text,
            transmission=transmission_text,
            fuel_type=fuel_type_text,
            body_type=body_type_text,
            model=model_text,
            ilan_no=ilan_no,
            renk=renk,
            motor_hacmi=motor_hacmi,
            motor_gucu=motor_gucu,
            cekis=cekis,
            arac_durumu=arac_durumu,
            ort_yakit_tuketimi=ort_yakit_tuketimi,
            depo=depo,
            boya_degisen=boya_degisen,
            takasa_uygun=takasa_uygun,
            kimden=kimden,
            original_parts=original_parts,
            changed_parts=changed_parts,
            painted_parts=painted_parts,
            local_painted_parts=local_painted_parts
        )
        return car

    except Exception as e:
        print(f"Error occurred: {e}")
        return None

# Example usage
url = "https://www.arabam.com/ilan/galeriden-satilik-peugeot-308-1-2-puretech-allure/etna-motors-boyasiz-yet-servis-bakm-garantili-mavi-308-allure/27356337"
car_data = scrape_car_data(url)
if car_data:
    print(car_data)
