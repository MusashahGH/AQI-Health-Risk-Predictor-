import requests
import pandas as pd
from risk_engine import calculate_risk

API_KEY = "87cd0dc16459fa4e5815d739fefc1baa"

cities = {
    "lahore": (31.5497, 74.3436),
    "karachi": (24.8607, 67.0011),
    "islamabad": (33.6844, 73.0479),
    "faisalabad": (31.4180, 73.0791),
    "multan": (30.1575, 71.5249),
    "peshawar": (34.0151, 71.5249),
}

sample_user = {"age": 30, "has_asthma": True, "activity_level": "medium"}

rows = []

for city, (lat, lon) in cities.items():
    url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={API_KEY}"
    response = requests.get(url)
    data = response.json()

    if "list" not in data:
        print(f"{city} ke liye data nahi mila: {data}")
        continue

    components = data["list"][0]["components"]
    aqi_index = data["list"][0]["main"]["aqi"]

    risk, advice = calculate_risk(
        aqi_index=aqi_index,
        age=sample_user["age"],
        has_asthma=sample_user["has_asthma"],
        activity_level=sample_user["activity_level"]
    )

    row = {
        "city": city,
        "aqi_index": aqi_index,
        "pm25": components["pm2_5"],
        "pm10": components["pm10"],
        "no2": components["no2"],
        "so2": components["so2"],
        "co": components["co"],
        "o3": components["o3"],
        "risk": risk,
        "advice": advice,
    }
    rows.append(row)

df = pd.DataFrame(rows)
print(df)
df.to_csv("aqi_data.csv", index=False)
print("Saved to aqi_data.csv")