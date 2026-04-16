from sklearn.linear_model import LinearRegression
import numpy as np

model = LinearRegression()

def train_model(dataset):
    if len(dataset) < 2:
        return

    X = np.array([[d["rating"], d["distance"]] for d in dataset])
    y = np.array([d["rating"] / (d["distance"] + 0.0001) for d in dataset])

    model.fit(X, y)

def predict_score(rating, distance):
    try:
        return model.predict([[rating, distance]])[0]
    except:
        return rating / (distance + 0.0001)
