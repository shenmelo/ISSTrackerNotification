import time
import requests
from datetime import datetime
import smtplib

MY_LAT = 14.902350 # Your latitude
MY_LONG = 120.848938 # Your longitude

EMAIL = "" # Enter your email here
PASSWORD = "" # Enter your password here

def is_visible_position():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    if MY_LAT-5 <= iss_latitude <= MY_LAT+5 and MY_LONG-5 <= iss_longitude <= MY_LONG+5:
        return True


def is_night_time():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }

    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    time_now = datetime.now().hour
    if sunrise > time_now > sunset:
        return True


while True:
    time.sleep(60)
    if is_visible_position() and is_night_time():
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=EMAIL, password=PASSWORD)
            connection.sendmail(from_addr=EMAIL,
                                to_addrs="sherwinatendido17@yahoo.com",
                                msg="Subject:ISS Visible\n\nISS is currently overhead, go out and check.")






