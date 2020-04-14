from functions import functions as fc
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

API_KEY = 'mUfs9iSFOdYU_3V4GuxMZw4G5qp8y8K8Xo-mudPF8nGaVouYrnfJkXWU6ewiHbNpp0Zij5cUD--1O8S2BnBAmdllndlfWAejqYl7nA2e3nN3X902A6yXgt9-OoaNXnYx'
headers = {'Authorization': 'Bearer ' + API_KEY}

q = "SELECT * FROM business where platform = 'yelp' and updated = 0 ORDER BY RAND() LIMIT 10"
business = fc.db.select(q, all=True)

# Driver for webscrapping
# For Windows
driver = webdriver.Chrome('chromedriver.exe')

# For headless Linux
# chrome_options = Options()
# chrome_options.add_argument("--headless")
# driver = webdriver.Chrome('/usr/bin/chromedriver', options=chrome_options)

for b in business:
    url = 'https://api.yelp.com/v3/businesses/'+b['idPlatform']+'/reviews'
    r = requests.get(url, headers=headers)
    result = r.json()['reviews']
    for review in result:
        user_profile = review['user']['profile_url']
        driver.get(user_profile)
        content = driver.page_source
        soup = BeautifulSoup(content, "html.parser")
        review_origin = soup.find('h3', attrs={'class': 'user-location alternate'})
        # Split and get last value
        if review_origin.text is not None:
            review_details = review_origin.text.split(', ')
        else:
            continue
        country = fc.get_country_from_long(review_details[-1])['idCountry']
        # print(country)
        query = "INSERT INTO `reviews` (`name`,`idBusiness`,`reviewer_score`, `reviewer_score_cal`, `reviewer_country`, `review_country`, `review_average`, `review_average_cal`, `review_category`, `lat`, `long`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        val = (b['business'], b['idbusiness'], review['rating'], review['rating']/5, country, b['country'], b['rating'], b['rating']/5, b['category'], b['lat'], b['long'])
        fc.db.insert(query, val)
    update_q = "UPDATE business set updated = 1 where idbusiness=%s"
    update_val = (b['idbusiness'],)
    fc.db.update(update_q, update_val)
    print(b['business'], 'Updated')
driver.quit()
