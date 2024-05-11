import requests
from datetime import datetime
import smtplib
import time

MY_LAT = 52.520008  # Your latitude
MY_LONG = 13.404954  # Your longitude

EMAIL = "aaronfeininger@gmail.com"
PASSWORD = "svnsqsyfwnzwjahl"

response = requests.get(url="http://api.open-notify.org/iss-now.json")
response.raise_for_status()
data = response.json()

iss_latitude = float(data["iss_position"]["latitude"])
iss_longitude = float(data["iss_position"]["longitude"])

# Your position is within +5 or -5 degrees of the ISS position.

parameters = {
    "lat": MY_LAT,
    "lng": MY_LONG,
    "formatted": 0,
}

response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
response.raise_for_status()
data = response.json()
sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0]) + 2
sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0]) + 2

time_now = datetime.now()
current_hour = time_now.hour

# If the ISS is close to my current position
# ,and it is currently dark
# Then email me to tell me to look up.
# BONUS: run the code every 60 seconds.


def is_iss_visible():
    global MY_LAT, MY_LONG, iss_latitude, iss_longitude, sunrise, sunset, current_hour
    if (MY_LAT - 5 < iss_latitude < MY_LAT + 5 and MY_LONG - 5 < iss_longitude < MY_LONG + 5
            and sunset < current_hour or current_hour < sunrise):
        return True


print(sunset, sunrise, current_hour)

while True:
    time.sleep(120)
    if is_iss_visible():
        with smtplib.SMTP("smtp.gmail.com", 587) as connection:
            connection.starttls()
            connection.login(EMAIL, PASSWORD)
            connection.sendmail(from_addr=EMAIL, to_addrs="rkowert@posteo.de",
                                msg="Subject:ISS visible now\n\n"
                                    "The ISS is now visible in your region.")
