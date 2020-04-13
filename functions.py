# Import all necessary libraries here.
# This file can then be loaded on all scripts and will benefit for
import pandas as pd
import numpy as np
import re
from db_class import Db
from sqlalchemy import create_engine

# Initiate a new DB connection
db = Db()


# Query Database table countries to retrieve information for each country
# Returns idCountry, fulName, 2letterCode, 3letterCode
def get_country_details(country):
    q = "SELECT * from countries where fullName='" + country + "'"
    result = db.select(q, all=False)
    return result


# full address to country. Not standard only works for this dataset
def get_country(x):
    # from analyzing the data we have only one country which is not a single word (United Kingdom)
    if x.split(" ")[-1] == 'Kingdom':
        return ' '.join(x.split(" ")[-2:])
    else:
        return x.split(" ")[-1]


def get_country_from_long(x):
    # IF TWO LETTERS IS US STATE RETURN United States
    if len(x) == 2:
        x = 'United States of America'
    q = "SELECT * from countries where fullName='"+x+"'"
    result = db.select(q, all=False)
    if result is None:
        q = "SELECT * from countries where idCountry='254'"
        result = db.select(q, all=False)
    return result


def create_pd_engine():
    host = 'ironhack.c1wtctuqirxg.eu-central-1.rds.amazonaws.com'
    port = 3306
    user = 'final_admin'
    password = 'GBL7CG93bgc4!jT%'
    database = 'final_project'
    return create_engine(
            'mysql+mysqlconnector://' + user + ':' + password + '@' + host + ':' + port + '/' + database)

