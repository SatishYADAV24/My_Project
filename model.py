import pandas as pd

def load_data(path="train_data.csv"):
    df = pd.read_csv(path)

    df["scheduled"] = pd.to_datetime(df["scheduled"])
    df["actual"] = pd.to_datetime(df["actual"])
    df["date"] = pd.to_datetime(df["date"])

    df["delay_min"] = (
        df["actual"] - df["scheduled"]
    ).dt.total_seconds() / 60

    df["is_late"] = df["delay_min"] > 5
    df["weekday"] = df["date"].dt.day_name()

    return df


def analyze_train(train_no):
    df = load_data()
    train_df = df[df["train_no"] == int(train_no)]

    if train_df.empty:
        return {"error": "Train not found"}

    train_df = train_df.sort_values("date")

    last_7 = train_df.tail(7)
    last_30 = train_df.tail(30)

    avg_delay = last_7["delay_min"].mean()
    late_ratio = last_7["is_late"].mean()
    delay_std = last_7["delay_min"].std()

    delay_std = 0 if pd.isna(delay_std) else delay_std

    reliability_score = 100 - (avg_delay * 2 + late_ratio * 40)
    reliability_score = max(0, min(100, reliability_score))

    prediction = "Likely Late" if avg_delay > 10 else "On Time"

    # Confidence Indicator
    if delay_std < 5:
        confidence = "High"
    elif delay_std < 10:
        confidence = "Medium"
    else:
        confidence = "Low"

    # Best Travel Day
    weekday_stats = train_df.groupby("weekday")["delay_min"].mean()
    best_day = weekday_stats.idxmin()

    return {
        "train_no": train_no,
        "reliability_score": round(reliability_score, 2),
        "prediction": prediction,
        "confidence": confidence,
        "best_travel_day": best_day,
        "last_7_days": [
            {"date": row["date"].strftime("%d %b"), "delay": round(row["delay_min"], 2)}
            for _, row in last_7.iterrows()
        ],
        "monthly_trend": [
            {"date": row["date"].strftime("%d %b"), "delay": round(row["delay_min"], 2)}
            for _, row in last_30.iterrows()
        ],
    }


def route_search(source, destination):
    df = load_data()

    route_df = df[
        (df["source"].str.lower() == source.lower()) &
        (df["destination"].str.lower() == destination.lower())
    ]

    results = []

    for train_no in route_df["train_no"].unique():
        train_df = route_df[route_df["train_no"] == train_no].sort_values("date")
        last_7 = train_df.tail(7)

        avg_delay = last_7["delay_min"].mean()
        reliability_score = 100 - avg_delay * 2
        reliability_score = max(0, min(100, reliability_score))

        results.append({
            "train_no": int(train_no),
            "reliability_score": round(reliability_score, 2)
        })

    results = sorted(results, key=lambda x: x["reliability_score"], reverse=True)

    return {"route_results": results}