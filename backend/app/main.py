import os
import numpy as np
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from catboost import CatBoostClassifier
from app.schemas import ConjunctionRequest

app = FastAPI(title="OrbitalGuard Core API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MODEL_PATH = "models/orbital_model.cb"

if os.path.exists(MODEL_PATH):
    model = CatBoostClassifier()
    model.load_model(MODEL_PATH)
    print(" [SUCCESS] Model loaded inside the Docker container!")
else:
    model = None
    print(" [WARNING] Model file nahi mili container ke andar!")

@app.post("/predict-risk")
async def predict_risk(data: ConjunctionRequest):
    if model is None:
        raise HTTPException(status_code=500, detail="ML Model weight file missing on Docker server!")
    
    try:
        risk_index = data.relative_velocity / (data.relative_distance + 0.1)

        features = np.array([[
            data.semi_major_axis,
            data.eccentricity,
            data.inclination,
            data.relative_distance,
            data.relative_velocity,
            risk_index
        ]])
        
        probs = model.predict_proba(features)[0]
        pred_class = int(model.predict(features)[0][0])
        
        categories = {0: "SAFE", 1: "WARNING", 2: "CRITICAL_DANGER"}
        actions = {
            "SAFE": "Maintain current orbit tracking parameters.",
            "WARNING": "Alert orbital mechanics team. Increase radar telemetry scan rate.",
            "CRITICAL_DANGER": "TRIGGER IMMEDIATE EVASIVE MANOEUVRE THRUSTERS!"
        }
        
        return {
            "status": "success",
            "collision_risk_class": categories[pred_class],
            "confidence_score": round(float(max(probs)) * 100, 2),
            "recommended_action": actions[categories[pred_class]],
            "probabilities": {categories[i]: round(float(probs[i]) * 100, 2) for i in range(3)}
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Inference Error: {str(e)}")