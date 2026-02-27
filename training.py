import pandas as pd
import pickle

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report

data = pd.read_csv("grievances.csv")

X = data["complaint"]
y = data["department"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

model = Pipeline([
    ("tfidf", TfidfVectorizer(
        ngram_range=(1, 2),
        max_features=5000,
        stop_words="english"
    )),
    ("clf", LogisticRegression())
])

model.fit(X_train, y_train)

y_pred = model.predict(X_test)

print("Accuracy:", model.score(X_test, y_test))
print("\nClassification Report:")
print(classification_report(y_test, y_pred))

with open("model.pkl", "wb") as f:
    pickle.dump(model, f)

print("\nModel saved!")
