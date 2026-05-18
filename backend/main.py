from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def home():
    return {
        "message": "Inventory Risk Tracker API Running"
    }