from functions import functions as fc
import pandas as pd
import numpy as np
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
import pickle

# Grab nationalities with more reviews (TOP10)
print("Grabbing nationalities from reviews (TOP10)")
q = "SELECT reviewer_country, COUNT(*) as totalReviews FROM reviews GROUP BY reviewer_country ORDER BY totalReviews DESC LIMIT 10"
nationalities_res = fc.db.select(q, all=True)
nationalities = [str(n['reviewer_country']) for n in nationalities_res]

print("Grabbing business")
b_q = "SELECT idbusiness from business where category = 1"
business_res = fc.db.select(b_q, all=True)
business = [str(b['idbusiness']) for b in business_res]

print("Grabbing business reviews")
# Get the reviews for this business of the top 10 nationalities
r_q = "SELECT r.idBusiness, reviewer_score, reviewer_score_cal, reviewer_country, rating, rating_cal, country FROM reviews r INNER JOIN business b ON r.idbusiness = b.idbusiness WHERE r.idbusiness IN (" + (',').join(business) + ") AND reviewer_country IN ("+ (',').join(nationalities) +")"
reviews = fc.db.select(r_q, all=True)
review_df = pd.DataFrame(reviews)
print("Preparing Data for model")
bins = [0, 0.80, 0.90, 1]
labels = [1, 2, 3]
review_df['b_review'] = pd.cut(review_df['rating_cal'], bins, labels=labels)
review_df['u_review'] = pd.cut(review_df['reviewer_score_cal'], bins, labels=labels)
model_data = review_df.drop(['idBusiness', 'reviewer_score', 'reviewer_score_cal', 'rating_cal', 'rating'], axis=1)
pred = 'u_review'
print("Creating model for each nationality")
for n in nationalities:
    print("Model for Nationality:", n)
    final_data = model_data[model_data['reviewer_country'] == 235].drop('reviewer_country', axis=1)
    X = final_data.drop(columns=[pred])
    y = final_data[pred].values
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
    knn = KNeighborsClassifier(n_neighbors=5)
    knn.fit(X_train, y_train)
    print("Model Created")
    file_to_save = 'models/' + str(n)
    knnPickle = open(file_to_save, 'wb')
    # source, destination
    pickle.dump(knn, knnPickle)
    print("Model Saved")
    # break
print("All Done")