import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

from sklearn.metrics import make_scorer, fbeta_score, roc_curve

#############
##Making scorers
#############
f_precision = make_scorer(fbeta_score, beta = .5) ## More weight towards precision

#############
## Selecting Features
#############
features=['country','img_count', 'vid_count',
          'usd_goal', 'description_len', 'blurb_len',
          'slug_len', 'med_rewards','category_core',
          'reward_len', 'created_month', 'created_weekday',
          'deadline_month', 'deadline_weekday',
          'length_of_project']
dependent=['failed']
toscale = ['img_count', 'vid_count', 'usd_goal', 'description_len',
           'blurb_len', 'slug_len',
           'med_rewards', 'reward_len', 'length_of_project']
#############
## Load dataset
#############
df = pd.read_pickle('../data/kickstarter_analysis.pkl')
df = df.dropna()

X=df[features]
y=df[dependent]

#############
## Getting dummy variables
#############
X = pd.get_dummies(X, drop_first = True)
y = y.values.ravel()

#############
## getting training data
#############
X_train, X_test, y_train, y_test = train_test_split(X, y,
                                                   test_size = 0.4, random_state = 42)

#############
## Implementing Random Forest Classifier
## Utilizing best parameters done during randomizedSearchCV
#############
clf = RandomForestClassifier(n_estimators = 500, min_samples_split = 2, min_samples_leaf = 2,
                            max_features = 'sqrt', max_depth = 30, bootstrap = True)
clf.fit(X_train, y_train)

train_pred = clf.predict(X_train)
y_pred = clf.predict(X_test)

train_score = fbeta_score(y_train, train_pred, beta = 0.5)
score = fbeta_score(y_test, y_pred, beta = 0.5)

print("RF Score on training: {} \nRF Score on testing: {}".format(train_score, score))
