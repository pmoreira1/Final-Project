import pandas as pd
import functions

# Load dataset
hotels = pd.read_csv('../data/Hotel_Reviews.csv')

# Create a smaller dataset with only necessary values
hotels_short = hotels[['Hotel_Address', 'Hotel_Name', 'Reviewer_Nationality', 'Positive_Review', 'Negative_Review',
                       'Average_Score', 'Reviewer_Score', 'lat', 'lng']]

# Drop rows with na value
hotels_short.dropna(inplace=True)

# Get Hotel Country from Hotel Address
hotels_short['Country'] = hotels_short['Hotel_Address'].apply(lambda x: functions.get_country(x))

# Drop reviews with empty nationality
to_drop = hotels_short[hotels_short['Reviewer_Nationality'] == ' ' ].index

# Delete these row indexes from dataFrame
hotels_short.drop(to_drop, inplace=True)
final_review_data = hotels_short[['Hotel_Name', 'Reviewer_Nationality', 'Reviewer_Score',
                                  'Country', 'Average_Score', 'lat', 'lng']]

# Trim Reviewer_Nationality
final_review_data['Reviewer_Nationality'] = final_review_data['Reviewer_Nationality'].apply(lambda x: x.strip())

# Column Renaming
final_review_data.rename(columns={
    'Hotel_Name': 'name',
    'Reviewer_Nationality': 'reviewer_country',
    'Reviewer_Score': 'reviewer_score',
    'Country': 'review_country',
    'Average_Score': 'review_average',
    'lng': 'long'
}, inplace=True)

# Country Translation into ids
countries = list(final_review_data['reviewer_country'].value_counts().keys())
country_trans_dict = {c:functions.get_country_details(c)['idCountry'] for c in countries}
final_review_data['review_country'].replace(country_trans_dict, inplace=True)
final_review_data['reviewer_country'].replace(country_trans_dict, inplace=True)
# Add category for all hotels
final_review_data['review_category'] = '1'

# Reset index
final_review_data.reset_index(drop=True, inplace=True)

# Save CSV
final_review_data.to_csv('data/hotel_clean.csv')

# Save one by one on DB.
for i, r in final_review_data[165208:].iterrows():
    q = "INSERT INTO `final_project`.`reviews` (`name`, `reviewer_score`, `reviewer_country`, `review_country`, `review_average`, `review_category`, `lat`,`long`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
    val = (r['name'], r['reviewer_score'], r['reviewer_country'], r['review_country'], r['review_average'],
           r['review_category'], r['lat'], r['long'])
    insert_record = functions.db.insert(q, val)
    print(i, "out of", len(final_review_data), "Inserted:", insert_record)