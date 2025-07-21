# training/train_bot.py

from training.train_utils import prepare_training_data
from bot.memory import load_memory
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import pickle

def run_training():
    memory = load_memory()
    data, labels = prepare_training_data(memory)

    if len(data) < 10:
        print("⚠️ Not enough data to train. Run the bot to collect more trades.")
        return

    X_train, X_test, y_train, y_test = train_test_split(data, labels, test_size=0.3)
    model = RandomForestClassifier()
    model.fit(X_train, y_train)

    accuracy = accuracy_score(y_test, model.predict(X_test))
    print(f"✅ Training complete. Accuracy: {accuracy:.2f}")

    with open("models/degen_model.pkl", "wb") as f:
        pickle.dump(model, f)
    print("💾 Model saved to models/degen_model.pkl")

if __name__ == "__main__":
    run_training()