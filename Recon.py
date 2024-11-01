from flask import Flask, render_template, request
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

app = Flask(__name__)

# Set up Selenium Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_service = Service('C:/Users/Logic Supply/Desktop/Car Part Search/chromedriver.exe')

def create_driver():
    return webdriver.Chrome(service=chrome_service, options=chrome_options)

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
        results = []

        if platform == 'ebay':
            results = search_ebay(car_details)
        elif platform == 'amazon':
            results = search_amazon(car_details)
        elif platform == 'google':
            results = search_google(car_details)
        elif platform == 'rockauto':
            results = search_rockauto(car_details)

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

    with create_driver() as driver:
        driver.get(search_url)
        time.sleep(3)

        results = []
        items = driver.find_elements(By.CSS_SELECTOR, '.s-item')

        for item in items:
            try:
                title = item.find_element(By.CSS_SELECTOR, '.s-item__title')
                link = item.find_element(By.CSS_SELECTOR, '.s-item__link')
                img = item.find_element(By.CSS_SELECTOR, '.s-item__image-img').get_attribute('src') if item.find_elements(By.CSS_SELECTOR, '.s-item__image-img') else None

                results.append({
                    'title': title.text,
                    'link': link.get_attribute('href'),
                    'img': img
                })
            except Exception as e:
                print(f"Error extracting eBay item: {e}")

    return results

def search_amazon(car_details):
    base_url = "https://www.amazon.com/s?"
    search_query = f"field-keywords={car_details['make']}+{car_details['model']}+{car_details['year']}+{car_details['trim']}+{car_details['engine']}"

    if car_details.get('part_number'):
        search_query += f"+{car_details['part_number']}"
    if car_details.get('keywords'):
        search_query += f"+{car_details['keywords']}"

    search_url = base_url + search_query

    with create_driver() as driver:
        driver.get(search_url)
        time.sleep(3)

        results = []
        items = driver.find_elements(By.CSS_SELECTOR, '.s-main-slot .s-result-item')

        for item in items:
            try:
                title = item.find_element(By.CSS_SELECTOR, 'h2 .a-link-normal')
                link = title.get_attribute('href')
                img = item.find_element(By.CSS_SELECTOR, 'img.s-image').get_attribute('src') if item.find_elements(By.CSS_SELECTOR, 'img.s-image') else None

                results.append({
                    'title': title.text,
                    'link': link,
                    'img': img
                })
            except Exception as e:
                print(f"Error extracting Amazon item: {e}")

    return results

def search_google(car_details):
    base_url = "https://www.google.com/search?"
    search_query = f"{car_details['make']} {car_details['model']} {car_details['year']} {car_details['trim']} {car_details['engine']}"

    if car_details.get('part_number'):
        search_query += f" {car_details['part_number']}"
    if car_details.get('keywords'):
        search_query += f" {car_details['keywords']}"

    search_url = base_url + f"q={search_query}"

    with create_driver() as driver:
        driver.get(search_url)
        time.sleep(3)

        results = []
        items = driver.find_elements(By.CSS_SELECTOR, '.g')

        for item in items:
            try:
                title = item.find_element(By.CSS_SELECTOR, 'h3')
                link = item.find_element(By.CSS_SELECTOR, 'a').get_attribute('href') if item.find_elements(By.CSS_SELECTOR, 'a') else None

                results.append({
                    'title': title.text,
                    'link': link
                })
            except Exception as e:
                print(f"Error extracting Google item: {e}")

    return results

def search_rockauto(car_details):
    base_url = "https://www.rockauto.com/en/catalog/"
    search_query = f"{car_details['make']} {car_details['model']} {car_details['year']} {car_details['trim']} {car_details['engine']}"

    if car_details.get('part_number'):
        search_query += f" {car_details['part_number']}"
    if car_details.get('keywords'):
        search_query += f" {car_details['keywords']}"

    search_url = base_url + search_query.replace(" ", "+")

    with create_driver() as driver:
        driver.get(search_url)
        time.sleep(3)

        results = []
        items = driver.find_elements(By.CSS_SELECTOR, '.result-item')  # Ensure this selector is correct

        for item in items:
            try:
                title = item.find_element(By.CSS_SELECTOR, '.part-name')  # Ensure this selector is correct
                link = item.find_element(By.CSS_SELECTOR, 'a').get_attribute('href') if item.find_elements(By.CSS_SELECTOR, 'a') else None
                img = item.find_element(By.CSS_SELECTOR, 'img').get_attribute('src') if item.find_elements(By.CSS_SELECTOR, 'img') else None

                results.append({
                    'title': title.text.strip(),
                    'link': link,
                    'img': img
                })
            except Exception as e:
                print(f"Error extracting RockAuto item: {e}")

    return results

if __name__ == '__main__':
    app.run(debug=True)
