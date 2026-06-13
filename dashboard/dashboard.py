import streamlit as st
import pandas as pd
import os
import sys
import plotly.graph_objects as go
from streamlit_autorefresh import st_autorefresh

# Adjust path to import modules from parent directory
sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            ".."
        )
    )
)

from crop_recommendation import recommend_crop
from ml.predict_irrigation import predict_pump
from utils.pdf_report import generate_report
from weather.weather_service import get_weather

st.set_page_config(
    page_title="IoT Smart Agriculture",
    page_icon="🌱",
    layout="wide"
)

# Auto-refresh every 5 seconds
st_autorefresh(
    interval=5000,
    key="refresh"
)

st.title("🌱 IoT Smart Agriculture Monitoring System")

csv_file = "data/sensor_data.csv"

if not os.path.exists(csv_file):

    sample_data = {
        "Soil":[70],
        "Temperature":[28],
        "Humidity":[60],
        "Light":[500],
        "Water":[80],
        "Pump":["OFF"],
        "Alerts":[""]
    }

    df = pd.DataFrame(sample_data)

else:
    df = pd.read_csv(csv_file)

df = pd.read_csv(csv_file)
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
c2.metric("Alerts", len(df[df["Alerts"] != ""]))
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

c1, c2, c3 = st.columns(3)
c1.metric("Temperature", f"{weather['temp']} °C")
c2.metric("Humidity", f"{weather['humidity']} %")
c3.metric("Condition", weather["weather"])

# --- PDF REPORT ---
st.divider()

if st.button("📄 Generate PDF Report"):

    pdf_path = generate_report(
        latest.to_dict(),
        crop,
        prediction,
        weather
    )

    if os.path.exists(pdf_path):

        st.success(
            "PDF Generated Successfully!"
        )

        with open(
            pdf_path,
            "rb"
        ) as file:

            pdf_bytes = file.read()

        st.download_button(
            label="📥 Download PDF Report",
            data=pdf_bytes,
            file_name="IoT_Smart_Agriculture_Report.pdf",
            mime="application/pdf"
        )

    else:

        st.error(
            "PDF file not found."
        )

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
alerts = df[df["Alerts"] != ""]
st.dataframe(alerts, use_container_width=True)

st.subheader("🗂 Raw Sensor Data")
st.dataframe(df, use_container_width=True)