# IoT Smart Agriculture Monitoring System Architecture

## 1. Overview

The IoT Smart Agriculture Monitoring System is designed to monitor environmental conditions in agricultural fields and automate irrigation based on soil moisture levels. The system integrates IoT sensors, cloud services, machine learning, and a real-time dashboard to provide smart farming capabilities.

---

## 2. System Architecture

```text
                    +------------------+
                    |     DHT22        |
                    | Temp & Humidity  |
                    +---------+--------+
                              |
                              |
                    +---------v--------+
                    |      ESP32       |
                    | Microcontroller  |
                    +----+----+----+---+
                         |    |    |
                         |    |    |
             +-----------+    |    +-----------+
             |                |                |
     +-------v------+  +------v------+  +------v------+
     | Soil Sensor  |  | Water Level |  | Light Sensor|
     +--------------+  +-------------+  +-------------+
                         |
                         |
                 +-------v-------+
                 | Relay Module  |
                 +-------+-------+
                         |
                         |
                 +-------v-------+
                 | Water Pump    |
                 +---------------+

                         |
                         |
                Serial / Cloud Data
                         |
                         v

      +--------------------------------------+
      | Python Data Processing Layer         |
      | - CSV Logging                        |
      | - Alert Generation                   |
      | - Pump Control Logic                 |
      +------------------+-------------------+
                         |
                         |
                         v

      +--------------------------------------+
      | Streamlit Dashboard                  |
      | - Live Sensor Status                 |
      | - Gauge Charts                       |
      | - Sensor Trends                      |
      | - Weather Forecast                   |
      | - Crop Recommendation                |
      | - AI Irrigation Prediction           |
      | - PDF Report Generation              |
      +------------------+-------------------+
                         |
                         |
                         v

      +--------------------------------------+
      | ThingSpeak Cloud Platform            |
      | - Data Storage                       |
      | - Cloud Visualization                |
      | - Remote Monitoring                  |
      +--------------------------------------+
```

---

## 3. Hardware Components

### ESP32

Acts as the central controller that collects sensor data and controls irrigation.

### DHT22 Sensor

Measures:

* Temperature (°C)
* Humidity (%)

### Soil Moisture Sensor

Measures soil water content and determines irrigation requirements.

### Water Level Sensor

Monitors water availability in the storage tank.

### LDR (Light Sensor)

Measures ambient light intensity.

### Relay Module

Controls the irrigation pump automatically.

### LED Indicator

Provides visual indication of pump status.

---

## 4. Software Components

### ESP32 Firmware

Developed using Arduino IDE and responsible for:

* Reading sensors
* Processing values
* Controlling relay
* Sending data through serial communication

### Python Backend

Handles:

* Data collection
* CSV storage
* Alert generation
* System monitoring

### Machine Learning Module

Uses a Decision Tree Classifier to predict:

* Pump ON
* Pump OFF

based on:

* Soil Moisture
* Temperature
* Humidity
* Water Level

### Crop Recommendation Module

Suggests suitable crops according to environmental conditions.

### Weather Service

Retrieves live weather data using OpenWeatherMap API.

### PDF Reporting Module

Generates downloadable reports containing:

* Sensor values
* Crop recommendations
* Irrigation predictions
* Weather information

---

## 5. Data Flow

### Step 1

Sensors collect environmental data.

### Step 2

ESP32 processes readings and determines irrigation status.

### Step 3

Data is transmitted to the Python application.

### Step 4

Python stores data in:

```text
data/sensor_data.csv
```

### Step 5

Machine Learning predicts irrigation requirements.

### Step 6

Crop recommendation logic suggests suitable crops.

### Step 7

Data is uploaded to ThingSpeak Cloud.

### Step 8

Dashboard visualizes data in real time.

### Step 9

Users generate PDF reports for analysis.

---

## 6. Key Features

* Real-time sensor monitoring
* Automated irrigation control
* Crop recommendation system
* Machine learning irrigation prediction
* ThingSpeak cloud integration
* Weather forecasting
* PDF report generation
* Interactive Streamlit dashboard
* Historical trend analysis

---

## 7. Technologies Used

### Hardware

* ESP32
* DHT22
* Soil Moisture Sensor
* Water Level Sensor
* LDR
* Relay Module
* LED

### Software

* Python
* Streamlit
* Pandas
* Plotly
* Scikit-Learn
* ReportLab
* Requests

### Cloud Services

* ThingSpeak
* OpenWeatherMap API

---

## 8. Future Enhancements

* Real sensor deployment in agricultural fields
* Mobile application integration
* SMS and Email alerts
* MQTT communication
* Firebase cloud storage
* Deep learning based crop prediction
* Multi-zone irrigation management

---

## Conclusion

The IoT Smart Agriculture Monitoring System demonstrates how IoT, cloud computing, machine learning, and real-time visualization can be integrated to improve agricultural productivity, reduce water wastage, and support smart farming practices.
