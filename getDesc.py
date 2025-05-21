import sys
sys.stdout.reconfigure(encoding='utf-8')  # Force UTF-8 encoding for console output

import requests
from bs4 import BeautifulSoup

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

# Main function
def main():
    # Example link
    link = "https://www.arabam.com/ilan/sahibinden-satilik-anadol-a2-sl/sahibinden-anadol-a2-sl-1990-model/27346608"
    description = fetch_description(link)
    print("Description:", description)

if __name__ == "__main__":
    main()
