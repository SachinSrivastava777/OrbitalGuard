# OrbitalGuard: Space Debris Tracking & Collision Risk Engine

A production-grade space technology framework that predicts space debris collision vectors in Low Earth Orbit (LEO) using Machine Learning, serves predictions via a high-performance FastAPI microservice, and visualizes live telemetry metrics through a Streamlit Mission Control console.

---

## Project Structure

```text
OrbitalGuard/
├── backend/       # FastAPI app, Pydantic schemas, and CatBoost ML model
└── frontend/      # Streamlit telemetry console (ui.py)
How to Run Locally
Follow these steps sequentially to spin up both environments on your local system:
```

1. Set Up Virtual Environment
Open your terminal at the root project directory and execute:
```
Bash
python -m venv venv
On Windows, activate with:
```
```
DOS
venv\Scripts\activate
```

2. Boot Up the Backend (FastAPI Engine)
Navigate to the backend directory, upgrade your local dependencies, and trigger the Uvicorn runtime:
```
Bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```
Verification Check: Open your browser and go to http://127.0.0.1:8000/docs to access the interactive FastAPI Swagger interface.

3. Spin Up the Frontend (Streamlit Dashboard)
Open a separate terminal window, ensure the virtual environment is active, and launch the UI configuration:

```
Bash
cd frontend
pip install -r requirements.txt
streamlit run ui.py
The application will automatically initialize a browser instance pointing to http://localhost:8501. Adjust the real-time telemetry sliders and click "Analyze Collision Vectors" to query live machine learning predictions.
