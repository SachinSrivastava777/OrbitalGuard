import pandas as pd
import numpy as np
import os

def generate_orbital_dataset(num_samples=5000):
    print("Orbital Pipeline: Re-generating realistic simulation telemetry...")
    np.random.seed(42)
    
    semi_major_axis = np.random.uniform(6500, 42000, num_samples)
    eccentricity = np.random.uniform(0.0, 0.1, num_samples)
    inclination = np.random.uniform(0, 90, num_samples)
    relative_distance = np.random.exponential(scale=15.0, size=num_samples)
    relative_velocity = np.random.uniform(1.0, 15.0, num_samples)
    
    df = pd.DataFrame({
        'semi_major_axis': semi_major_axis,
        'eccentricity': eccentricity,
        'inclination': inclination,
        'relative_distance': relative_distance,
        'relative_velocity': relative_velocity
    })

    base_score = (df['relative_velocity'] * 5) - (df['relative_distance'] * 8)

    noise = np.random.normal(0, 15, num_samples)
    final_score = base_score + noise

    conditions = [
        (final_score > 15),
        (final_score <= 15) & (final_score > -20)
    ]
    choices = [2, 1]
    df['collision_risk'] = np.select(conditions, choices, default=0)
    
    os.makedirs('data/raw', exist_ok=True)
    os.makedirs('data/processed', exist_ok=True)
    
    df.to_csv('data/raw/satellite_telemetry.csv', index=False)
    df['risk_index'] = (df['relative_velocity'] / (df['relative_distance'] + 0.1))
    df.to_csv('data/processed/clean_orbital_data.csv', index=False)
    
    print(f"Dataset generated with overlapping risk zones. Shape: {df.shape}")

if __name__ == "__main__":
    generate_orbital_dataset()