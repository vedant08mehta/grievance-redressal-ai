import pandas as pd
import pickle

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

data = pd.read_csv("grievances.csv")

X = data["complaint"]
y = data["department"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = Pipeline([
    ("tfidf", TfidfVectorizer()),
    ("clf", LogisticRegression())
])

model.fit(X_train, y_train)

acc = model.score(X_test, y_test)
print("Accuracy:", acc)

with open("model.pkl", "wb") as f:
    pickle.dump(model, f)

print("Model saved!")