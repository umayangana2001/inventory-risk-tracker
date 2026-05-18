from services.excel_loader import load_data


def calculate_weekly_usage():

    data = load_data()

    return {
        "message": "analytics service working"
    }