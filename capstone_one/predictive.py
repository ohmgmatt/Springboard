import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

df = pd.read_pickle('kickstarter_analysis.pkl')
df = df.dropna()

y = df['failed'].values

vectorizer = CountVectorizer()
X = vectorizer.fit_transform(df['blurb'].values)

X_train, X_test, y_train, y_test = train_test_split(X, y,
  test_size = 0.3, random_state = 42)

clf = MultinomialNB()
clf.fit(X_train, y_train)

words = np.array(vectorizer.get_feature_names())
print(len(words))

x = np.eye(X_test.shape[1])
print('Got the x')
probs = clf.predict_log_proba(x)
print('Did the probs')


print(probs)
