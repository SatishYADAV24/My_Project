import pandas as pd
import random
from datetime import datetime, timedelta

routes = [
    {"train_no": 12345, "source": "Delhi", "destination": "Lucknow"},
    {"train_no": 12346, "source": "Delhi", "destination": "Mumbai"},
    {"train_no": 22301, "source": "Kolkata", "destination": "Delhi"},
    {"train_no": 12010, "source": "Chennai", "destination": "Bangalore"},
    {"train_no": 19005, "source": "Ahmedabad", "destination": "Mumbai"},
]

start_date = datetime(2026, 1, 1)

data = []

for train in routes:
    for i in range(90):  # 3 months data
        date = start_date + timedelta(days=i)

        scheduled_hour = random.randint(5, 22)
        scheduled_min = random.choice([0, 15, 30, 45])

        delay = max(0, int(random.gauss(12, 7)))

        scheduled_time = datetime(
            date.year, date.month, date.day,
            scheduled_hour, scheduled_min
        )

        actual_time = scheduled_time + timedelta(minutes=delay)

        data.append({
            "train_no": train["train_no"],
            "source": train["source"],
            "destination": train["destination"],
            "date": date.strftime("%Y-%m-%d"),
            "scheduled": scheduled_time.strftime("%Y-%m-%d %H:%M"),
            "actual": actual_time.strftime("%Y-%m-%d %H:%M"),
        })

df = pd.DataFrame(data)
df.to_csv("train_data.csv", index=False)

print("Dataset upgraded successfully 🚆")