import os
import json
from dotenv import load_dotenv
load_dotenv()

import requests
from flask import Flask, request, jsonify, render_template
from google import genai
from database import init_db, save_check, get_history

from risk_engine import calculate_risk

app = Flask(__name__, template_folder='../Frontend/templates', static_folder='../Frontend/static')
init_db()

API_KEY = os.getenv("OPENWEATHER_KEY")
GEMINI_KEY = os.getenv("GEMINI_API_KEY", "")

gemini_client = genai.Client(api_key=GEMINI_KEY) if GEMINI_KEY else None

cities = {
    "lahore": (31.5497, 74.3436),
    "karachi": (24.8607, 67.0011),
    "islamabad": (33.6844, 73.0479),
    "faisalabad": (31.4180, 73.0791),
    "multan": (30.1575, 71.5249),
    "peshawar": (34.0151, 71.5249),
}

def generate_ai_advice(city, aqi_index, risk, age, has_asthma, activity_level):
    fallback = {
        "summary": f"{risk} for this profile in {city}.",
        "avoid": ["Limit outdoor exertion", "Carry a mask", "Avoid traffic hotspots"],
        "precautions": ["Drink water", "Monitor symptoms", "Use protective gear"]
    }

    if gemini_client is None:
        return fallback

    prompt = f"""
    A user wants a personalized air quality safety report.
    City: {city}
    Current AQI level: {aqi_index} (scale 1-5, 5 is worst)
    Calculated risk level: {risk}
    User age: {age}
    Has asthma: {has_asthma}
    Activity level: {activity_level}

    Respond ONLY with valid JSON, no markdown formatting, no code fences, in exactly this shape:
    {{
      "summary": "one short sentence on what this risk means for this specific person",
      "avoid": ["short phrase", "short phrase", "short phrase"],
      "precautions": ["short phrase", "short phrase", "short phrase"]
    }}
    Keep each list item under 8 words, specific to this person's age and condition.
    """

    try:
        response = gemini_client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )
        text = response.text.strip().replace("```json", "").replace("```", "").strip()
        payload = json.loads(text)
        if not isinstance(payload, dict):
            raise ValueError("AI response is not a JSON object")
        return payload
    except Exception as exc:
        app.logger.warning("AI advice generation failed: %s", exc)
        return fallback

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/check-risk", methods=["GET"])
def check_risk():
    name = request.args.get("name", "Guest")
    age = int(request.args.get("age", 30))
    has_asthma = request.args.get("has_asthma", "false").lower() == "true"
    activity_level = request.args.get("activity_level", "medium")

    lat = request.args.get("lat")
    lon = request.args.get("lon")
    city = request.args.get("city", "lahore").lower()

    if lat and lon:
        lat, lon = float(lat), float(lon)
        location_label = "Your Location"
    elif city in cities:
        lat, lon = cities[city]
        location_label = city.title()
    else:
        return jsonify({"error": "City not supported"}), 400

    url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={API_KEY}"
    response = requests.get(url, timeout=15)
    if response.status_code != 200:
        return jsonify({"error": "Unable to fetch AQI data right now."}), 502

    data = response.json()
    if "list" not in data or not data["list"]:
        return jsonify({"error": "No AQI data available for this location."}), 400

    components = data["list"][0]["components"]
    aqi_index = data["list"][0]["main"]["aqi"]

    risk, basic_advice = calculate_risk(
        aqi_index=aqi_index,
        age=age,
        has_asthma=has_asthma,
        activity_level=activity_level
    )

    ai_data = generate_ai_advice(location_label, aqi_index, risk, age, has_asthma, activity_level)
    
    save_check(name, location_label, age, has_asthma, activity_level, aqi_index, risk, ai_data.get("summary", ""))
        
    return jsonify({
        "city": location_label,
        "aqi_index": aqi_index,
        "pm25": round(components["pm2_5"], 1),
        "pm10": round(components["pm10"], 1),
        "no2": round(components["no2"], 1),
        "risk": risk,
        "summary": ai_data.get("summary", ""),
        "avoid": ai_data.get("avoid", []),
        "precautions": ai_data.get("precautions", [])
    })

if __name__ == "__main__":
    app.run(debug=True)