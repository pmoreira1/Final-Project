<img src="https://bit.ly/2VnXWr2" alt="Ironhack Logo" width="100"/>

# Final Project

**The demand level of travellers in data**

*Pedro Moreira*

*Data Analytics, Amsterdam 2020*

## Content
- [Project Description](#project-description)
- [Rules](#rules)
- [Workflow](#workflow)
- [Organization](#organization)
- [Links](#links)

## Project Description
This project goal is to categorize travellers based on their country of origin. This categorization is based on reviews grabbed (via .CSV, API and web scrapping) from booking.com, expedia and yelp.

After a deep analysis of the data grabbed a model will be created to predict a match level of the traveller to the business.

## Data Pipeline
<img src="https://drive.google.com/open?id=162Heb4EuZ6DcV0PUhXNGiobYvWJ04Ha-" alt="Project Workflow">

## Organization
```
FINAL-PROJECT
│   .gitignore
│   dataset_importer.py
│   get_match_level.py
│   get_recommendations.py
│   Model decision.ipynb
│   model_creation.py
│   Presentation.twb
│   README.md
│   Recommendations.twb
│   yelp_business_grabber.py
│   yelp_review_grabber.py
├───data
│       countries_with_codes.csv
│       hotel_clean.csv
│       mysql_reviews.csv
├───functions
│       db_class.py
│       functions.py
├───models
│       108
│       14
│       157
│       196
│       216
│       234
│       235
│       236
│       41
│       84
├───results
│       recommendations.csv

```
## Links

[Repository](https://github.com/pmoreira1/final-project)

[Slides](https://docs.google.com/presentation/d/1j0eeq0fz75578fAVJXVEYlf8t-NFS1X-Zo07Bfz8IWA/edit?usp=sharing)

