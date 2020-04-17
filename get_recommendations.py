import sys
from functions import functions as fc
import pickle
import pandas as pd
pd.set_option('mode.chained_assignment', None)

# print('Number of arguments:', len(sys.argv), 'arguments.')
# print('Argument List:', str(sys.argv))
# to be launched as get_recommendations.py category nationality destination

categories = [1, 2]
nationality = sys.argv[1]
destination = sys.argv[2]

bins = [0, 0.80, 0.90, 1]
labels = [1, 2, 3]

loaded_model = pickle.load(open('models/'+str(nationality), 'rb'))
final_result = pd.DataFrame()
for c in categories:
    business = pd.DataFrame(fc.db.select(query="SELECT * from business where category='"+str(c)+"' and country='"+str(destination)+"'", all=True))
    business_to_predict = business[['country', 'rating_cal']]
    business_to_predict['b_review'] = pd.cut(business_to_predict['rating_cal'], bins, labels=labels)
    business_to_predict.drop('rating_cal', axis=1, inplace=True)
    business['match_level'] = loaded_model.predict(business_to_predict)
    business.sort_values(by=['match_level', 'rating', 'review_count'], ascending=False, inplace=True)
    result = business[['idbusiness', 'business', 'category', 'lat', 'long', 'match_level', 'rating_cal', 'review_count']][:10].reset_index(drop=True)
    final_result = final_result.append(result)
final_result.reset_index(drop=True)
final_result.to_csv('results/recommendations.csv')
print(final_result)
# print(15)