from fastapi import FastAPI
from services.analytics_service import (
    calculate_weekly_usage,
    calculate_inventory_risk,
    shipment_impact_analysis,
    alternative_item_analysis,
    generate_inventory_timeline
)
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {
        "message": "Inventory Risk Tracker API Running"
    }


@app.get("/weekly-usage")
def weekly_usage():

    result = calculate_weekly_usage()

    return result
@app.get("/inventory-risk")
def inventory_risk():

    result = calculate_inventory_risk()

    return result

@app.get("/shipment-impact")
def shipment_impact():

    result = shipment_impact_analysis()

    return result

@app.get("/alternative-analysis")
def alternative_analysis():

    result = alternative_item_analysis()

    return result

@app.get("/timeline/{item_id}")
def inventory_timeline(item_id: int):

    result = generate_inventory_timeline(item_id)

    return result