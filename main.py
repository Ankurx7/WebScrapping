import requests
from bs4 import BeautifulSoup
import csv

url = "https://www.noon.com/uae-en/sports-and-outdoors/exercise-and-fitness/yoga-16328/"

def fetch_data(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status() 
        print("Page fetched successfully.")
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        product_titles = soup.find_all('span', class_='sc-16h9t2v-0 kEppzG')  
        product_prices = soup.find_all('span', class_='sc-16h9t2v-0 cFLXlO')  
        
        products = []
        
        
        for title, price in zip(product_titles[:200], product_prices[:200]):  
            product_name = title.get_text(strip=True)
            product_price = price.get_text(strip=True)
            products.append([product_name, product_price])

        return products
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching page: {e}")
        return []

def save_to_csv(products):
    if products:
        with open('noon_products.csv', 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Product Name', 'Price']
            writer = csv.writer(csvfile)
            writer.writerow(fieldnames)
            writer.writerows(products)
        print("Data saved to 'noon_products.csv'")
    else:
        print("No data to save.")


products_data = fetch_data(url)


save_to_csv(products_data)
