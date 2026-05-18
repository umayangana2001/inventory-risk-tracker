import pandas as pd

EXCEL_PATH = r"C:\Users\tharushiu\Desktop\Internship_diary\inventory-risk-tracker\datasets\inventory_input.xlsx"


def load_data():

    consumption_df = pd.read_excel(
        EXCEL_PATH,
        sheet_name="Consumption",
        header=3
    )

    return {
        "message": "Excel loaded successfully",
        "rows": len(consumption_df)
    }