from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime
import os


def generate_report(
        sensor_data,
        crop,
        prediction,
        weather
):

    os.makedirs(
        "outputs/reports",
        exist_ok=True
    )

    pdf_path = "outputs/reports/agriculture_report.pdf"

    pdf = SimpleDocTemplate(pdf_path)

    styles = getSampleStyleSheet()

    content = []

    content.append(
        Paragraph(
            "IoT Smart Agriculture Monitoring Report",
            styles["Title"]
        )
    )

    content.append(Spacer(1, 20))

    content.append(
        Paragraph(
            f"Generated On: {datetime.now()}",
            styles["Normal"]
        )
    )

    content.append(Spacer(1, 20))

    # Sensor Data

    content.append(
        Paragraph(
            "Latest Sensor Data",
            styles["Heading2"]
        )
    )

    content.append(Spacer(1, 10))

    for key, value in sensor_data.items():

        content.append(
            Paragraph(
                f"<b>{key}</b>: {value}",
                styles["Normal"]
            )
        )

    content.append(Spacer(1, 20))

    # Crop Recommendation

    content.append(
        Paragraph(
            "Crop Recommendation",
            styles["Heading2"]
        )
    )

    content.append(
        Paragraph(
            crop,
            styles["Normal"]
        )
    )

    content.append(Spacer(1, 20))

    # AI Prediction

    content.append(
        Paragraph(
            "AI Irrigation Prediction",
            styles["Heading2"]
        )
    )

    content.append(
        Paragraph(
            prediction,
            styles["Normal"]
        )
    )

    content.append(Spacer(1, 20))

    # Weather

    content.append(
        Paragraph(
            "Weather Information",
            styles["Heading2"]
        )
    )

    content.append(
        Paragraph(
            f"Temperature: {weather['temp']} °C",
            styles["Normal"]
        )
    )

    content.append(
        Paragraph(
            f"Humidity: {weather['humidity']} %",
            styles["Normal"]
        )
    )

    content.append(
        Paragraph(
            f"Condition: {weather['weather']}",
            styles["Normal"]
        )
    )

    pdf.build(content)

    return pdf_path