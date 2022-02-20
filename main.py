import os

import requests
from twilio.rest import Client


OWM_Endpoint = "https://api.openweathermap.org/data/2.5/onecall"
api_key = os.environ.get("OWM_API_KEY")
account_sid = "AC43c64c938f1743a763eaf701952573c7"
auth_token = os.environ.get("AUTH_TOKEN")


weather_params = {
    "lat": 40.761532,
    "lon": -73.831108,
    "appid": api_key,
    "exclude": "current,minutely, daily"
}

response = requests.get(OWM_Endpoint, params=weather_params)
response.raise_for_status()
weather_data = response.json()
weather_slice = weather_data["hourly"][:12]

need_umbrella = False


for hour_data in weather_slice:
    condition_code = hour_data["weather"][0]["id"]
    if int(condition_code) < 700:
        need_umbrella = True

if need_umbrella:
    client = Client(account_sid, auth_token)

    message = client.messages \
        .create(
        body="It's going to rain/snow; remember to bundle up🧣 & carry an umbrella☔",
        from_='+19126179157',
        to='+19293718183'
    )
    print(message.status)


