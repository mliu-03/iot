import requests
from geopy.distance import geodesic
import yagmail
import json
import os

CONFIG_FILE = "config.json"
GEOFENCE_RADIUS = 700  # Meters

def load_or_ask_for_config():
    """Load saved config or ask user for recipient and dweet thing names."""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            config = json.load(f)
    else:
        recipient_name = input("Enter recipient's name: ")
        recipient_email = input("Enter recipient's email: ")
        thing_name = input("Enter other dweet.io thing names (comma separated): ").split(",")
        payment = input("Enter amount willing to pay for meal swipe: ")


        config = {
            "recipient_name": recipient_name,
            "recipient_email": recipient_email,
            "thing_name": thing_name,
            "payment": payment
        }

        with open(CONFIG_FILE, "w") as f:
            json.dump(config, f)

    return config

# Load user config
config = load_or_ask_for_config()
RECIPIENT_NAME = config["recipient_name"]
RECIPIENT_EMAIL = config["recipient_email"]
THING_NAME = config["thing_name"]  # Other devices to compare
PAYMENT = config["payment"]  # Other devices to compare

# Email Configuration (Update with your details)
SENDER_EMAIL = "miyaliu03@gmail.com"
SENDER_PASSWORD = "bxeb uhpv yunx kdki"


def get_location(thing_name):
    """Fetch latitude and longitude from dweet.io for a given thing."""
    url = f"https://dweet.io/get/latest/dweet/for/{thing_name}"
    try:
        response = requests.get(url)
        data = response.json()

        if "with" in data and len(data["with"]) > 0:
            content = data["with"][0]["content"]
            latitude = content.get("your_latitude")
            longitude = content.get("your_longitude")

            if latitude is not None and longitude is not None:
                return (latitude, longitude)
            else:
                print(f"Latitude or longitude not found for {thing_name}.")
        else:
            print(f"No dweet data available for {thing_name}.")
    except Exception as e:
        print(f"Error fetching data for {thing_name}: {e}")

    return None

def send_email(alert_message):
    """Send email notification using yagmail."""
    try:
        yag = yagmail.SMTP(SENDER_EMAIL, SENDER_PASSWORD)
        yag.send(
            to=RECIPIENT_EMAIL,
            subject="💸iSwipe Request!",
           contents=alert_message,
        )
        print("✅ Email sent successfully!")
    except Exception as e:
        print(f"❌ Error sending email: {e}")

# Get reference location
reference_location = "38.9, -77.04921385899615"

if reference_location:
    print(f"📍 Reference Location iSwiper: {reference_location}\n")

    for thing in THING_NAME:
        location = get_location(thing)
        if location:
            distance = geodesic(reference_location, location).meters
            print(f"Distance from iSwiper to {thing}: {distance:.2f} meters")

            if distance <= GEOFENCE_RADIUS:
                alert_message = f"🚨 {RECIPIENT_NAME}, a meal swipe for {PAYMENT} is {distance:.2f} meters away! Respond to this email if you are interested in making some money!"
                print(alert_message)
                send_email(alert_message)
else:
    print(f"❌ Failed to retrieve location for {REFERENCE_THING}.")
