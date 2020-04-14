# Script that will store all business in a db table
# Be having this separated it makes it easier to pick the reviews with a separate script
# Especially helpfull due to rate-limiting, and if needed spread the load via other VMs
import functions.functions as fc
import requests
from pprint import pprint

API_KEY = 'mUfs9iSFOdYU_3V4GuxMZw4G5qp8y8K8Xo-mudPF8nGaVouYrnfJkXWU6ewiHbNpp0Zij5cUD--1O8S2BnBAmdllndlfWAejqYl7nA2e3nN3X902A6yXgt9-OoaNXnYx'
url = 'https://api.yelp.com/v3/businesses/search'
headers = {'Authorization': 'Bearer ' + API_KEY}

cities = ['Amsterdam', 'London', 'Milan', 'Barcelona', 'Wien', 'Paris']

limit = 50
category = 2
platform = 'yelp'
for c in cities:
    offset = 0
    while (offset + limit) < 1000:
        query = {
            'offset': offset,
            'limit': 50,
            'location': c,
            'categories': 'restaurants, All',
            'sort_by': 'review_count'
        }
        r = requests.get(url, headers=headers, params=query)
        result = r.json()['businesses']
        # prepare data to be stored
        for b in result:
            name = b['name']
            id = b['id']
            country = b['location']['country']
            lat = b['coordinates']['latitude']
            long = b['coordinates']['longitude']
            rating = b['rating']
            q = "INSERT INTO `final_project`.`business` (`business`, `lat`, `long`, `platform`, `idPlatform`, `country`, `category`, `rating`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
            val = (name, lat, long, platform, id, country, category, rating)
            fc.db.insert(q, val)
            print(c, name, 'Saved')
        offset += limit
        print(c, offset)
