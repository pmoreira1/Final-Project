import sys
from functions import functions as fc
import pickle
import pandas as pd
# pd.set_option('mode.chained_assignment', None)

businness_id = sys.argv[1]
nationality = sys.argv[2]

business_details = fc.get_business_details(businness_id)
business_country = business_details['country']
businness_rating = fc.binner(business_details['rating'])


bins = [0, 0.80, 0.90, 1]
labels = [1, 2, 3]

#Load Model
loaded_model = pickle.load(open('models/'+str(nationality), 'rb'))
test_value = pd.DataFrame([int(business_country), businness_rating]).T
test_value.columns = ['country', 'rating']
print(int(loaded_model.predict(test_value)))

