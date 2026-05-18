from fastapi import FastAPI
from services.excel_loader import load_data

app = FastAPI()


@app.get("/")
def home():
    return {"message": "Inventory Risk Tracker API Running"}


@app.get("/test-data")
def test_data():

    data = load_data()

    return data