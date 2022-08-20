import requests, json
from flask import Flask, render_template, request
import os

app = Flask('app')
lst = []

@app.route('/')
def home():
  return render_template("index.html")

@app.route('/edu')
def education():
  return render_template("edu.html")

@app.route('/lic_cert')
def lic_cert():
  return render_template("lic_cert.html")

@app.route('/exp')
def exp():
  return render_template("exp.html")

@app.route('/weather')
def weather():
  country = "Toronto"
  url = f"https://api.openweathermap.org/data/2.5/weather?q={country},CA&appid=9821d430bd99ea2cf1e664d59fc7b028"
  r = requests.get(url)
  data = r.json()
  temp = float(data["main"]["temp"])
  temp_min = float(data["main"]["temp_min"])
  temp_max = float(data["main"]["temp_max"])
  lon = data["coord"]["lon"]
  lat = data["coord"]["lat"]
  humid = float(data["main"]["humidity"])
  desc = data["weather"][0]["description"]
  wind_speed = data["wind"]["speed"]

  return render_template("weather.html",temp=temp,temp_min=temp_min,temp_max=temp_max,lon=lon,lat=lat,humid=humid,desc=desc,wind_speed=wind_speed,country=country)

@app.route('/bmi', methods = ['GET', 'POST'])
def bmi():
  return render_template("bmi.html")

@app.route('/form', methods = ['GET', 'POST'])
def form_function():
  if request.method == 'POST':
    data = request.form
    height = float(data["height"])
    weight = float(data["weight"])
    bmi = weight / (height/100)**2
    bmi = round(bmi, 2)
    if bmi <= 18.4:
      status = "underweight"
    elif bmi <= 24.9:
      status = "healthy"
    elif bmi <= 29.9:
      status = "overweight"
    elif bmi <= 34.9:
      status = "severely overweight"
    elif bmi <= 39.9:
      status = "obese"
    else:
      status = "severely obese"
  
  data_json = {
    "height": height,
    "weight": weight,
    "bmi": bmi,
    "result": status
  }
  lst.append(data_json)
  json_file = r"static/docs/data.json"
  filesize = os.path.getsize(json_file)

  with open(json_file, mode='w') as f:
    json.dump(lst, f, indent=4)

  return render_template("bmi.html", bmi = bmi, status = status)

app.run(host='0.0.0.0', port=8080)
