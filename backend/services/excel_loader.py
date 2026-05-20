import pandas as pd

EXCEL_PATH = r"C:\Users\tharushiu\Desktop\Internship_diary\inventory-risk-tracker\datasets\inventory_input.xlsx"


def load_data():

    itemmaster_df = pd.read_excel(
        EXCEL_PATH,
        sheet_name="ItemMaster"
    )

    onhand_df = pd.read_excel(
        EXCEL_PATH,
        sheet_name="OnHand"
    )

    consumption_df = pd.read_excel(
        EXCEL_PATH,
        sheet_name="Consumption"
    )

    shipments_df = pd.read_excel(
        EXCEL_PATH,
        sheet_name="Shipments"
    )

    alternatives_df = pd.read_excel(
        EXCEL_PATH,
        sheet_name="Alternatives"
    )

    return {
        "ItemMaster": itemmaster_df,
        "OnHand": onhand_df,
        "Consumption": consumption_df,
        "Shipments": shipments_df,
        "Alternatives": alternatives_df
    }