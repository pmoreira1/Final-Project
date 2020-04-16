import sys
from functions import functions as fc
import pickle
import pandas as pd
pd.set_option('mode.chained_assignment', None)

# print('Number of arguments:', len(sys.argv), 'arguments.')
# print('Argument List:', str(sys.argv))
# to be launched as get_recommendations.py category nationality destination

category = sys.argv[1]
nationality = sys.argv[2]
destination = sys.argv[3]

bins = [0, 0.80, 0.90, 1]
labels = [1, 2, 3]

loaded_model = pickle.load(open('models/'+str(nationality), 'rb'))

hotels = pd.DataFrame(fc.db.select(query="SELECT * from business where category='"+str(category)+"' and country='"+str(destination)+"'", all=True))
hotels_to_predict = hotels[['country', 'rating_cal']]
hotels_to_predict['b_review'] = pd.cut(hotels_to_predict['rating_cal'], bins, labels=labels)
hotels_to_predict.drop('rating_cal', axis=1, inplace=True)
hotels['match_level'] = loaded_model.predict(hotels_to_predict)
hotels.sort_values(by=['match_level', 'rating', 'review_count'], ascending=False, inplace=True)

result = hotels[['business', 'lat', 'long', 'match_level', 'rating', 'review_count']].head(10).reset_index(drop=True)
result.to_csv('results/result.csv')
print(result)
# print(15)