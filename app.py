import requests
from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

def get_weather(city):
    geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1"
    geo_response = requests.get(geo_url)
    geo_data = geo_response.json()

    if "results" not in geo_data or len(geo_data["results"]) == 0:
        return {"error": "❌ شهر پیدا نشد!"}

    latitude = geo_data["results"][0]["latitude"]
    longitude = geo_data["results"][0]["longitude"]

    url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current_weather=true"
    response = requests.get(url)
    data = response.json()

    current = data.get("current_weather", {})
    temp = current.get("temperature")
    wind = current.get("windspeed")

    if temp is None or wind is None:
        return {"error": "❌ اطلاعات کافی نیست."}

    if temp < 5:
        suggestion = "پیشنهاد: خیلی سرده، لباس گرم بپوش! 🧥"
    elif temp <= 20:
        if wind <= 10:
            suggestion = "پیشنهاد: هوا عالیه 😎"
        else:
            suggestion = "پیشنهاد: هوا خوبه ولی یه کم باد میاد 🌬️"
    else:
        if wind > 20:
            suggestion = "پیشنهاد: گرمه و باد شدیده! 🥵💨"
        else:
            suggestion = "پیشنهاد: هوا گرمه ☀️"

    return {"city": city, "temperature": temp, "windspeed": wind, "suggestion": suggestion}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/weather', methods=['GET'])
def weather():
    city = request.args.get('city')
    if not city:
        return jsonify({"error": "لطفا اسم شهر را وارد کنید!"})
    result = get_weather(city)
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)
