from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

def prepare_training_data(memory):
    data = []
    labels = []
    for trade in memory:
        coin = {
            'volume': random.randint(100, 2000),  # replace with real volume
            'wallets': random.randint(20, 500),
            'age': random.randint(5, 180)
        }
        features = [
            rate_name(trade['coin']),
            scale_volume(coin['volume']),
            calculate_growth(coin['wallets']),
            time_decay(coin['age']),
            trade['score']
        ]
        label = 1 if trade['profit'] > 0 else 0
        data.append(features)
        labels.append(label)
    return data, labels

def train_classifier(memory):
    data, labels = prepare_training_data(memory)
    X_train, X_test, y_train, y_test = train_test_split(data, labels, test_size=0.2)
    model = RandomForestClassifier()
    model.fit(X_train, y_train)
    accuracy = accuracy_score(y_test, model.predict(X_test))
    print(f"🧪 ML Model Accuracy: {accuracy:.2f}")
    return model