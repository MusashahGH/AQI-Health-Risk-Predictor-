# 🌬️ AQI Health Risk Predictor

An intelligent full-stack web application that analyzes real-time Air Quality Index (AQI) data and provides personalized health risk assessments and AI-powered recommendations.

The application considers factors such as **AQI level, age, asthma condition, and outdoor activity level** to calculate a personalized health risk and provide useful health advice.

---

## ✨ Features

- 🌍 **Real-Time AQI Data**
  - Fetches live air pollution data for supported cities using the OpenWeatherMap API.

- 🩺 **Personalized Risk Assessment**
  - Calculates health risk based on:
    - AQI level
    - Age
    - Asthma condition
    - Outdoor activity level

- 🤖 **AI-Powered Health Advice**
  - Uses Google Gemini AI to generate personalized health recommendations based on the calculated risk.

- 📜 **Search History**
  - Stores previous AQI assessments using SQLite.

- 📊 **AQI Information**
  - Displays air quality and health-risk information in an easy-to-understand format.

- 💻 **Modern Responsive Interface**
  - Clean and responsive frontend built using HTML, CSS, and Vanilla JavaScript.

- 🔐 **Secure API Key Handling**
  - API keys are stored using environment variables instead of being directly written in the source code.

---

## 🛠️ Technologies Used

### Frontend

- HTML5
- CSS3
- JavaScript (Vanilla JavaScript)

### Backend

- Python 3
- Flask
- SQLite
- Requests

### APIs & AI

- OpenWeatherMap API
- Google Gemini API

### Tools

- Visual Studio Code
- Git
- GitHub

---

🌐  Open the Application

After starting the Flask server, open your browser and visit:

http://127.0.0.1:5000

The AQI Health Risk Predictor should now be running locally.

## 📁 Project Structure

```text
AQI-Health-Risk-Predictor/
│
├── api/
│   └── index.py
│
├── Backend/
│   ├── app.py
│   ├── database.py
│   ├── fetch_aqi.py
│   ├── risk_engine.py
│   └── aqi_data.csv
│
├── Frontend/
│   ├── templates/
│   │   └── index.html
│   │
│   └── static/
│       ├── style.css
│       └── script.js
│
├── vercel.json
├── requirements.txt
├── .gitignore
└── README.md
