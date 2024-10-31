from flask import Flask, render_template, request
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

app = Flask(__name__)

# Sample repair data
repair_data = [
    {
        'make_model': 'Honda Accord',
        'link': 'https://charm.li/honda-accord-manual',
        'description': 'Comprehensive service manual covering engine, transmission, and electrical systems.'
    },
    {
        'make_model': 'Toyota Camry',
        'link': 'https://charm.li/toyota-camry-manual',
        'description': 'Detailed guide for repairs and maintenance procedures.'
    },
    # Add more entries as necessary
]

# Set up Selenium Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_service = Service('C:/Users/Logic Supply/Desktop/Car Part Search/chromedriver.exe')

driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        car_details = {
            'make': request.form['make'],
            'model': request.form['model'],
            'year': request.form['year'],
            'trim': request.form['trim'],
            'engine': request.form['engine'],
            'part_number': request.form.get('part_number'),
            'keywords': request.form.get('keywords')
        }

        platform = request.form['platform']

        # Perform search based on selected platform
        if platform == 'ebay':
            results = search_ebay(car_details)
        elif platform == 'amazon':
            results = search_amazon(car_details)
        elif platform == 'google':
            results = search_google(car_details)
        elif platform == 'rockauto':
            results = search_rockauto(car_details)
        else:
            results = []

        return render_template('results.html', results=results)

    return render_template('index.html')

def search_ebay(car_details):
    base_url = "https://www.ebay.com/sch/i.html?"
    search_query = f"_nkw={car_details['make']}+{car_details['model']}+{car_details['year']}+{car_details['trim']}+{car_details['engine']}"

    if car_details.get('part_number'):
        search_query += f"+{car_details['part_number']}"
    if car_details.get('keywords'):
        search_query += f"+{car_details['keywords']}"

    search_url = base_url + search_query

    driver.get(search_url)
    time.sleep(3)  # Wait for the page to load

    results = []
    items = driver.find_elements("css selector", '.s-item')
    for item in items:
        title = item.find_element("css selector", '.s-item__title')
        link = item.find_element("css selector", '.s-item__link')
        img = item.find_element("css selector", '.s-item__image-img').get_attribute('src') if item.find_elements("css selector", '.s-item__image-img') else None
        if title and link:
            results.append({
                'title': title.text,
                'link': link.get_attribute('href'),
                'img': img
            })

    return results

def search_amazon(car_details):
    base_url = "https://www.amazon.com/s?"
    search_query = f"field-keywords={car_details['make']}+{car_details['model']}+{car_details['year']}+{car_details['trim']}+{car_details['engine']}"

    if car_details.get('part_number'):
        search_query += f"+{car_details['part_number']}"
    if car_details.get('keywords'):
        search_query += f"+{car_details['keywords']}"

    search_url = base_url + search_query

    driver.get(search_url)
    time.sleep(3)

    results = []
    items = driver.find_elements("css selector", '.s-main-slot .s-result-item')
    for item in items:
        title = item.find_element("css selector", 'h2 .a-link-normal')
        link = item.find_element("css selector", 'h2 .a-link-normal').get_attribute('href')
        img = item.find_element("css selector", 'img.s-image').get_attribute('src') if item.find_elements("css selector", 'img.s-image') else None
        if title and link:
            results.append({
                'title': title.text,
                'link': link,
                'img': img
            })

    return results

def search_google(car_details):
    base_url = "https://www.google.com/search?"
    search_query = f"{car_details['make']} {car_details['model']} {car_details['year']} {car_details['trim']} {car_details['engine']}"

    if car_details.get('part_number'):
        search_query += f" {car_details['part_number']}"
    if car_details.get('keywords'):
        search_query += f" {car_details['keywords']}"

    search_url = base_url + f"q={search_query}"

    driver.get(search_url)
    time.sleep(3)

    results = []
    items = driver.find_elements("css selector", '.g')
    for item in items:
        title = item.find_element("css selector", 'h3')
        link = item.find_element("css selector", 'a').get_attribute('href') if item.find_elements("css selector", 'a') else None
        if title and link:
            results.append({
                'title': title.text,
                'link': link
            })

    return results

def search_rockauto(car_details):
    base_url = "https://www.rockauto.com/en/catalog/"
    search_query = f"{car_details['make']} {car_details['model']} {car_details['year']} {car_details['trim']} {car_details['engine']}"

    if car_details.get('part_number'):
        search_query += f" {car_details['part_number']}"
    if car_details.get('keywords'):
        search_query += f" {car_details['keywords']}"

    search_url = base_url + search_query.replace(" ", "+")

    driver.get(search_url)
    time.sleep(3)

    results = []
    items = driver.find_elements("css selector", '.result-item')  # Ensure this selector is correct
    for item in items:
        title = item.find_element("css selector", '.part-name')  # Ensure this selector is correct
        link = item.find_element("css selector", 'a').get_attribute('href') if item.find_elements("css selector", 'a') else None
        img = item.find_element("css selector", 'img').get_attribute('src') if item.find_elements("css selector", 'img') else None
        if title and link:
            results.append({
                'title': title.text.strip(),
                'link': link,
                'img': img
            })

    return results

if __name__ == '__main__':
    app.run(debug=True)