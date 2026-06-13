def recommend_crop(temp, humidity, soil):

    if temp > 30 and soil > 60:
        return "Rice"

    elif temp < 30 and soil < 50:
        return "Wheat"

    elif humidity > 70:
        return "Sugarcane"

    elif soil > 50:
        return "Maize"

    return "Vegetables"