import pandas as pd
from catboost import CatBoostClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import os

def train_orbital_model():
    processed_data_path = 'data/processed/clean_orbital_data.csv'
    
    if not os.path.exists(processed_data_path):
        raise FileNotFoundError("Processed data not found. Please run the data pipeline first to generate the dataset.")
        
    df = pd.read_csv(processed_data_path)
    
    X = df.drop(columns=['collision_risk'])
    y = df['collision_risk']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    print(" ---- Model Training: CatBoost Classifier initialization...")
    
    model = CatBoostClassifier(
        iterations=150,
        learning_rate=0.05,
        depth=6,
        loss_function='MultiClass',
        verbose=50
    )
    
    model.fit(X_train, y_train, eval_set=(X_test, y_test))

    preds = model.predict(X_test)
    print("\n---- Model Performance Matrix:")
    print(classification_report(y_test, preds))

    os.makedirs('backend/models', exist_ok=True)
    model_save_path = 'backend/models/orbital_model.cb'
    model.save_model(model_save_path)
    print(f"---- Model weights successfully saved to: {model_save_path}")

if __name__ == "__main__":
    train_orbital_model()