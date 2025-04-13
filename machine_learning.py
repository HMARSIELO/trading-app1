import pickle
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split, cross_val_score

DATA_FILE = 'trade_data.pkl'
SCALER_FILE = 'scaler.pkl'

def load_trade_data():
    try:
        with open(DATA_FILE, 'rb') as f:
            data = pickle.load(f)
    except FileNotFoundError:
        data = []
    return data

def save_trade_data(data):
    with open(DATA_FILE, 'wb') as f:
        pickle.dump(data, f)

def save_scaler(scaler):
    with open(SCALER_FILE, 'wb') as f:
        pickle.dump(scaler, f)

def load_scaler():
    try:
        with open(SCALER_FILE, 'rb') as f:
            return pickle.load(f)
    except FileNotFoundError:
        return StandardScaler()  # مؤقت

def prepare_features(data):
    if not data:
        return None, None
    X = np.array([d[0] for d in data])
    y = np.array([d[1] for d in data])
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    save_scaler(scaler)
    return X_scaled, y

def train_model(data):
    X, y = prepare_features(data)
    if X is None or len(X) == 0:
        print("Not enough training data.")
        return None
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    scores = cross_val_score(model, X, y, cv=5)
    print(f"Cross-Validation Accuracy: {np.mean(scores):.2f}")
    return model

def predict_signal(model, features):
    scaler = load_scaler()
    features_scaled = scaler.transform([features])
    prediction = model.predict(features_scaled)
    return prediction[0]

if __name__ == "__main__":
    trade_data = load_trade_data()
    if not trade_data:
        trade_data = [
            ([25, 0.5, 1.2, 2.5, 1000], 1),
            ([45, -0.2, 0.8, 1.5, 500], 0),
            ([30, 0.1, 1.0, 2.0, 800], 1),
            ([60, -0.5, 1.5, 3.0, 1200], 0),
            ([28, 0.3, 1.1, 2.2, 950], 1)
        ]
        save_trade_data(trade_data)
        print("Default training data created and saved.")

    model = train_model(trade_data)
    if model:
        test_features = [28, 0.3, 1.1, 2.2, 950]
        result = predict_signal(model, test_features)
        print(f"Predicted signal: {'BUY' if result == 1 else 'HOLD'}")
