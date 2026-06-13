import streamlit as st
import pandas as pd
import os
import sys
import random
import plotly.graph_objects as go
from streamlit_autorefresh import st_autorefresh

# Adjust path to import modules from parent directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from crop_recommendation import recommend_crop
from ml.predict_irrigation import predict_pump
from utils.pdf_report import generate_report
from weather.weather_service import get_weather

st.set_page_config(page_title="IoT Smart Agriculture", page_icon="🌱", layout="wide")

# Auto-refresh every 5 seconds
st_autorefresh(interval=5000, key="refresh")

st.title("🌱 IoT Smart Agriculture Monitoring System")

# Ensure data directory exists
os.makedirs("data", exist_ok=True)
csv_file = "data/sensor_data.csv"

# --- DATA MANAGEMENT BUTTONS ---
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🔄 Refresh"):
        st.rerun()

with col2:
    if st.button("🎲 Generate New Data"):
        new_row = {
            "Soil": random.randint(20, 100),
            "Temperature": random.randint(20, 40),
            "Humidity": random.randint(30, 90),
            "Light": random.randint(100, 1000),
            "Water": random.randint(10, 100),
            "Pump": random.choice(["ON", "OFF"]),
            "Alerts": ""
        }
        
        df = pd.read_csv(csv_file) if os.path.exists(csv_file) else pd.DataFrame()

        if len(df) == 1 and df.iloc[0]["Soil"] == 0:
            df = pd.DataFrame()

        df.loc[len(df)] = new_row
        df.to_csv(csv_file, index=False)
        st.success("New data generated")
        st.rerun()

with col3:
    if st.button("🗑 Clear Data"):
        default_df = pd.DataFrame([{
            "Soil": 0,
            "Temperature": 0,
            "Humidity": 0,
            "Light": 0,
            "Water": 0,
            "Pump": "OFF",
            "Alerts": ""
        }])
        default_df.to_csv(csv_file, index=False)
        st.success("Data reset successfully")
        st.rerun()

# --- LOAD AND PROTECT DATA ---
if not os.path.exists(csv_file):
    # Initialize file if it doesn't exist
    pd.DataFrame(columns=["Soil", "Temperature", "Humidity", "Light", "Water", "Pump", "Alerts"]).to_csv(csv_file, index=False)

df = pd.read_csv(csv_file)

if df.empty:
    df = pd.DataFrame([{
        "Soil": 0,
        "Temperature": 0,
        "Humidity": 0,
        "Light": 0,
        "Water": 0,
        "Pump": "OFF",
        "Alerts": ""
    }])

latest = df.iloc[-1]

def create_gauge(title, value, max_value=100):
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=value,
            title={"text": title},
            gauge={
                "axis": {"range": [0, max_value]},
                "steps": [
                    {"range": [0, 30], "color": "red"},
                    {"range": [30, 70], "color": "yellow"},
                    {"range": [70, max_value], "color": "green"}
                ]
            }
        )
    )
    fig.update_layout(height=250)
    return fig

# --- STATISTICS ---
st.subheader("📈 Project Statistics")
c1, c2, c3 = st.columns(3)
c1.metric("Records", len(df))
c2.metric("Alerts", len(df[df["Alerts"].astype(str) != ""]))
c3.metric("Pump ON Count", len(df[df["Pump"] == "ON"]))

# --- LIVE SENSOR STATUS ---
st.subheader("📡 Live Sensor Status")
a, b, c, d, e = st.columns(5)
a.metric("Soil", f"{latest['Soil']}%")
b.metric("Temperature", f"{latest['Temperature']}°C")
c.metric("Humidity", f"{latest['Humidity']}%")
d.metric("Light", latest["Light"])
e.metric("Water", f"{latest['Water']}%")

# --- SENSOR GAUGES ---
st.subheader("📟 Sensor Gauges")
g1, g2 = st.columns(2)
with g1:
    st.plotly_chart(create_gauge("Soil Moisture", latest["Soil"]), use_container_width=True)
with g2:
    st.plotly_chart(create_gauge("Temperature", latest["Temperature"], 50), use_container_width=True)

g3, g4 = st.columns(2)
with g3:
    st.plotly_chart(create_gauge("Humidity", latest["Humidity"]), use_container_width=True)
with g4:
    st.plotly_chart(create_gauge("Water Level", latest["Water"]), use_container_width=True)

# --- CROP & AI PREDICTION ---
st.subheader("🌾 Crop Recommendation")
crop = recommend_crop(latest["Temperature"], latest["Humidity"], latest["Soil"])
st.success(f"Recommended Crop: {crop}")

st.subheader("🤖 AI Irrigation Prediction")
prediction = predict_pump(latest["Soil"], latest["Temperature"], latest["Humidity"], latest["Water"])
st.info(f"Machine Learning Suggests Pump: {prediction}")

# --- WEATHER FORECAST ---
st.subheader("☁ Weather Forecast")
city = st.text_input("Farm Location", "Delhi")
weather = get_weather(city)
w1, w2, w3 = st.columns(3)
w1.metric("Temperature", f"{weather['temp']} °C")
w2.metric("Humidity", f"{weather['humidity']} %")
w3.metric("Condition", weather["weather"])

# --- PDF REPORT ---
st.divider()
if st.button("📄 Generate PDF Report"):
    pdf_path = generate_report(latest.to_dict(), crop, prediction, weather)
    if pdf_path and os.path.exists(pdf_path):
        st.success("PDF Generated Successfully!")
        with open(pdf_path, "rb") as file:
            st.download_button("📥 Download PDF Report", file, "IoT_Smart_Agriculture_Report.pdf", "application/pdf")
    else:
        st.error("Failed to generate report.")

# --- TRENDS & DATA ---
st.subheader("🌱 Soil Moisture Trend")
st.line_chart(df["Soil"])
st.subheader("🌡 Temperature Trend")
st.line_chart(df["Temperature"])
st.subheader("💧 Humidity Trend")
st.line_chart(df["Humidity"])
st.subheader("🚰 Water Level Trend")
st.line_chart(df["Water"])

st.subheader("📜 Alert History")
st.dataframe(df[df["Alerts"].astype(str) != ""], use_container_width=True)
st.subheader("🗂 Raw Sensor Data")
st.dataframe(df, use_container_width=True)