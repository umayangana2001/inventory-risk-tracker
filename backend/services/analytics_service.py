import pandas as pd
from datetime import datetime, timedelta

from services.excel_loader import load_data


def calculate_weekly_usage():

    data = load_data()

    consumption_df = data["Consumption"]

    weekly_usage = (
        consumption_df
        .groupby("Item")["Consumption"]
        .mean()
        .reset_index()
    )

    weekly_usage.rename(
        columns={
            "Consumption": "AvgWeeklyUsage"
        },
        inplace=True
    )

    return weekly_usage.to_dict(orient="records")


def calculate_inventory_risk():

    data = load_data()

    consumption_df = data["Consumption"]
    onhand_df = data["OnHand"]
    itemmaster_df = data["ItemMaster"]

    # Average weekly usage
    weekly_usage = (
        consumption_df
        .groupby("Item")["Consumption"]
        .mean()
        .reset_index()
    )

    weekly_usage.rename(
        columns={
            "Consumption": "AvgWeeklyUsage"
        },
        inplace=True
    )

    # Latest stock snapshot
    latest_onhand = (
        onhand_df
        .sort_values("SnapshotDate")
        .groupby("Item")
        .tail(1)
    )

    # Merge stock + usage
    merged_df = latest_onhand.merge(
        weekly_usage,
        on="Item",
        how="left"
    )

    # Merge safety stock
    merged_df = merged_df.merge(
        itemmaster_df[["Item", "SafetyStock"]],
        on="Item",
        how="left"
    )

    # Weeks coverage
    merged_df["WeeksCoverage"] = (
        merged_df["OnHand"] /
        merged_df["AvgWeeklyUsage"]
    )

    # Risk classification
    def classify_risk(row):

        if row["OnHand"] <= 0:
            return "OUT OF STOCK"

        elif row["WeeksCoverage"] < 1:
            return "CRITICAL"

        elif row["WeeksCoverage"] < 3:
            return "RISK"

        else:
            return "SAFE"

    merged_df["RiskStatus"] = merged_df.apply(
        classify_risk,
        axis=1
    )

    result = merged_df[
        [
            "Item",
            "OnHand",
            "AvgWeeklyUsage",
            "WeeksCoverage",
            "SafetyStock",
            "RiskStatus"
        ]
    ]

    return result.to_dict(orient="records")


def shipment_impact_analysis():

    data = load_data()

    consumption_df = data["Consumption"]
    onhand_df = data["OnHand"]
    shipments_df = data["Shipments"]

    # Average weekly usage
    weekly_usage = (
        consumption_df
        .groupby("Item")["Consumption"]
        .mean()
        .reset_index()
    )

    weekly_usage.rename(
        columns={
            "Consumption": "AvgWeeklyUsage"
        },
        inplace=True
    )

    # Latest stock snapshot
    latest_onhand = (
        onhand_df
        .sort_values("SnapshotDate")
        .groupby("Item")
        .tail(1)
    )

    # Pending shipments
    pending_shipments = shipments_df[
        shipments_df["Status"] == "Pending"
    ]

    # Shipment totals
    shipment_totals = (
        pending_shipments
        .groupby("Item")["Quantity"]
        .sum()
        .reset_index()
    )

    shipment_totals.rename(
        columns={
            "Quantity": "IncomingShipmentQty"
        },
        inplace=True
    )

    # Merge
    merged_df = latest_onhand.merge(
        weekly_usage,
        on="Item",
        how="left"
    )

    merged_df = merged_df.merge(
        shipment_totals,
        on="Item",
        how="left"
    )

    # Fill missing values
    merged_df["IncomingShipmentQty"] = (
        merged_df["IncomingShipmentQty"]
        .fillna(0)
    )

    # Projected stock
    merged_df["ProjectedStock"] = (
        merged_df["OnHand"] +
        merged_df["IncomingShipmentQty"]
    )

    # Projected coverage
    merged_df["ProjectedWeeksCoverage"] = (
        merged_df["ProjectedStock"] /
        merged_df["AvgWeeklyUsage"]
    )

    # Risk classification
    def classify_projected_risk(row):

        if row["ProjectedStock"] <= 0:
            return "OUT OF STOCK"

        elif row["ProjectedWeeksCoverage"] < 1:
            return "CRITICAL"

        elif row["ProjectedWeeksCoverage"] < 3:
            return "RISK"

        else:
            return "SAFE"

    merged_df["ProjectedRiskStatus"] = merged_df.apply(
        classify_projected_risk,
        axis=1
    )

    result = merged_df[
        [
            "Item",
            "OnHand",
            "IncomingShipmentQty",
            "ProjectedStock",
            "AvgWeeklyUsage",
            "ProjectedWeeksCoverage",
            "ProjectedRiskStatus"
        ]
    ]

    return result.to_dict(orient="records")


def alternative_item_analysis():

    data = load_data()

    consumption_df = data["Consumption"]
    onhand_df = data["OnHand"]
    alternatives_df = data["Alternatives"]

    # Average weekly usage
    weekly_usage = (
        consumption_df
        .groupby("Item")["Consumption"]
        .mean()
        .reset_index()
    )

    weekly_usage.rename(
        columns={
            "Consumption": "AvgWeeklyUsage"
        },
        inplace=True
    )

    # Latest stock snapshot
    latest_onhand = (
        onhand_df
        .sort_values("SnapshotDate")
        .groupby("Item")
        .tail(1)
    )

    # Merge stock + usage
    merged_df = latest_onhand.merge(
        weekly_usage,
        on="Item",
        how="left"
    )

    # Weeks coverage
    merged_df["WeeksCoverage"] = (
        merged_df["OnHand"] /
        merged_df["AvgWeeklyUsage"]
    )

    # Risky items only
    risky_items = merged_df[
        merged_df["WeeksCoverage"] < 3
    ]

    results = []

    for _, row in risky_items.iterrows():

        item = row["Item"]
        current_stock = row["OnHand"]
        avg_usage = row["AvgWeeklyUsage"]

        # Find alternatives
        item_alternatives = alternatives_df[
            alternatives_df["Item"] == item
        ]

        for _, alt_row in item_alternatives.iterrows():

            alt_item = alt_row["Alternative"]

            # Alternative stock
            alt_stock_row = latest_onhand[
                latest_onhand["Item"] == alt_item
            ]

            if alt_stock_row.empty:
                continue

            alt_stock = alt_stock_row.iloc[0]["OnHand"]

            combined_stock = (
                current_stock +
                alt_stock
            )

            coverage_after_alt = (
                combined_stock /
                avg_usage
            )

            if coverage_after_alt >= 3:
                status = "RECOVERED"
            else:
                status = "STILL RISK"

            results.append({
                "Item": int(item),
                "CurrentStock": float(current_stock),
                "AlternativeItem": int(alt_item),
                "AlternativeStock": float(alt_stock),
                "CombinedStock": float(combined_stock),
                "CoverageAfterAlternative": round(coverage_after_alt, 2),
                "Status": status
            })

    return results


def generate_inventory_timeline(item_id):

    data = load_data()

    consumption_df = data["Consumption"]
    onhand_df = data["OnHand"]
    shipments_df = data["Shipments"]

    # Latest stock
    latest_stock_row = (
        onhand_df
        .sort_values("SnapshotDate")
        .groupby("Item")
        .tail(1)
    )

    item_stock_row = latest_stock_row[
        latest_stock_row["Item"] == item_id
    ]

    if item_stock_row.empty:
        return {
            "error": "Item not found"
        }

    current_stock = item_stock_row.iloc[0]["OnHand"]

    # Average weekly usage
    item_consumption = consumption_df[
        consumption_df["Item"] == item_id
    ]

    avg_weekly_usage = (
        item_consumption["Consumption"].mean()
    )

    # Pending shipments
    pending_shipments = shipments_df[
        (shipments_df["Item"] == item_id) &
        (shipments_df["Status"] == "Pending")
    ]

    timeline = []

    stock = current_stock

    # Current real date
    current_date = datetime.now()

    # Simulate next 12 REAL calendar weeks
    for week in range(12):

        # Future week date
        future_date = current_date + timedelta(weeks=week)

        # Real calendar week
        year, week_number, _ = future_date.isocalendar()

        # Example: 2026-W21
        week_label = f"{year}-W{week_number}"

        # Reduce stock
        stock = stock - avg_weekly_usage

        # Shipment logic
        shipment_arrivals = pending_shipments[
            pending_shipments["ArrivalDate"].notna()
        ]

        # Temporary shipment simulation
        if not shipment_arrivals.empty:

            # Shipment arrives after 3 future weeks
            if week == 3:

                incoming_qty = shipment_arrivals.iloc[0]["Quantity"]

                stock = stock + incoming_qty

        # Risk classification
        if stock <= 0:
            status = "OUT OF STOCK"

        elif stock < avg_weekly_usage:
            status = "CRITICAL"

        elif stock < (avg_weekly_usage * 3):
            status = "RISK"

        else:
            status = "SAFE"

        timeline.append({
            "Week": week_label,
            "ProjectedStock": round(stock, 2),
            "Status": status
        })

    return timeline