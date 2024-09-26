import requests
from datetime import datetime
import smtplib
import time

# Fetch the current ISS position
response_iss = requests.get(url="http://api.open-notify.org/iss-now.json")
data = response_iss.json()
iss_longitude = float(data["iss_position"]["longitude"])
iss_latitude = float(data["iss_position"]["latitude"])
iss_position = (iss_longitude, iss_latitude)

# Your location coordinates
my_lat = 41.199475
my_lng = 29.073983


# Function to send an email alert
def send_email():
    my_email = "your_email@gmail.com"  # Replace with your email
    password = "your_app_password"  # Replace with your app password (use an app-specific password)
    recipient_email = "recipient_email@gmail.com"  # Replace with the recipient's email

    # Establish connection with the email server
    connection = smtplib.SMTP("smtp.gmail.com")
    connection.starttls()
    connection.login(user=my_email, password=password)

    # Send the email
    connection.sendmail(
        from_addr=my_email,
        to_addrs=recipient_email,
        msg=f"""From: ISS Notifier\nSubject: LOOK UP!☝️\n\n
        The ISS is above you! Look up, you don't want to miss it!
        """.encode()
    )

    # Close the connection
    connection.close()


# Function to check if ISS is above
def iss_is_above():
    if (my_lat + 5 >= iss_latitude and my_lat - 5 <= iss_latitude) and (
            my_lng + 5 >= iss_longitude and my_lng - 5 <= iss_longitude):
        return True


# Function to check if it's nighttime at your location
def is_night():
    parameters = {
        "lat": my_lat,
        "lng": my_lng,
        "formatted": 0
    }
    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])
    time_now = datetime.now().hour
    if time_now >= sunset or time_now <= sunrise:
        return True


# Main loop to continuously check for ISS and night conditions
while True:
    time.sleep(60)  # Wait for 60 seconds between checks
    if is_night() and iss_is_above():
        send_email()
        print("Email Sent")
