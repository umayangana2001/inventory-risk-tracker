from services.excel_loader import load_data


def calculate_weekly_usage():

    data = load_data()

    consumption_df = data["consumption"]

    return {
        "columns": consumption_df.columns.tolist(),
        "sample_rows": consumption_df.head(5).to_dict(orient="records")
    }