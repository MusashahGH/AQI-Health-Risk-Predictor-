def calculate_risk(aqi_index, age, has_asthma, activity_level):
    """
    aqi_index: 1 (Good) to 5 (Very Poor) — OpenWeatherMap scale
    age: integer
    has_asthma: True/False
    activity_level: "low", "medium", "high"
    """
    score = 0

    # base score from AQI
    if aqi_index == 5:
        score += 3
    elif aqi_index == 4:
        score += 2
    elif aqi_index == 3:
        score += 1

    # health factors
    if has_asthma:
        score += 2
    if age > 60 or age < 12:
        score += 1

    # activity factor
    if activity_level == "high":
        score += 1

    # final category
    if score >= 5:
        risk = "High Risk"
        advice = "Avoid going outside unless necessary. Wear an N95 mask if you must."
    elif score >= 3:
        risk = "Moderate Risk"
        advice = "Avoid prolonged outdoor activity. Keep a mask with you."
    else:
        risk = "Low Risk"
        advice = "Normal activities are fine, no special precautions needed."

    return risk, advice


# Dummy test data (no API needed for this)
# it only work when you run risk_engine.py file
if __name__ == "__main__":
    test_cases = [
        {"aqi_index": 5, "age": 8, "has_asthma": True, "activity_level": "high"},
        {"aqi_index": 2, "age": 25, "has_asthma": False, "activity_level": "medium"},
        {"aqi_index": 4, "age": 65, "has_asthma": False, "activity_level": "low"},
    ]
    for case in test_cases:
        risk, advice = calculate_risk(**case)
        print(case, "->", risk, "-", advice)