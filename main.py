import requests
from pync import Notifier as notification
from plyer import notification
import time

import mysql.connector
import hashlib

db = mysql.connector.connect(
    host="localhost",
    port=3306,
    user="root",  # Replace with your MySQL username
    password="devesh@2004",  # Replace with your MySQL password
    database="myappdb"  # Change to your database name
)

cursor = db.cursor()


def signup(username, password):
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    query = "INSERT INTO users (username, password) VALUES (%s, %s)"
    values = (username, hashed_password)
    cursor.execute(query, values)
    db.commit()


def signin(username, password):
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    query = "SELECT * FROM users WHERE username = %s AND password = %s"
    values = (username, hashed_password)
    cursor.execute(query, values)
    user = cursor.fetchone()
    return user is not None


# API keys
weather_api_key = "86cb5d717ff2f87e41dc6a65c304500c"
earthquake_api_url = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_day.geojson"


# Function to get weather information
def get_weather(city):
    weather_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_api_key}"
    response = requests.get(weather_url)
    data = response.json()
    if data["cod"] == 200:
        temperature = data["main"]["temp"] - 273.15  # Convert to Celsius
        weather_description = data["weather"][0]["description"]
        return f"Temperature in {city}: {temperature:.2f}°C, {weather_description.capitalize()}"
    else:
        return "Weather information not available."


# Function to get earthquake information
def get_earthquake_info():
    response = requests.get(earthquake_api_url)
    data = response.json()
    features = data.get("features")
    if features:
        earthquake = features[0]
        magnitude = earthquake["properties"]["mag"]
        place = earthquake["properties"]["place"]
        return f"Earthquake Alert!\nMagnitude: {magnitude}\nLocation: {place}"
    else:
        return "No recent earthquakes."


# Main function to display notifications
def main():
    print()
    print("*-----------------------------------------------------------------------------*")
    print("**--------   Welcome To Weather and Earthquake notification System   --------**")
    print("*-----------------------------------------------------------------------------*")
    print()
    print()

    while True:
        print("Choose an option:")
        print("1. Sign up")
        print("2. Sign in")

        choice = input("Enter the option number: ").strip()

        if choice == '1':
            username = input("Enter a username: ")
            password = input("Enter a password: ")
            signup(username, password)
            print("Sign-up successful.")
            break
        elif choice == '2':
            username = input("Enter your username: ")
            password = input("Enter your password: ")
            if signin(username, password):
                print("Sign-in successful.")
                break
            else:
                print("Sign-in failed. Invalid username or password.")
        else:
            print("Invalid option. Please enter 1, 2.")

    while True:
        print("Press 1 for weather and earthquake forecast notification: ")
        print("Press 2 to quit the program")
        choice = input("Enter the option number: ").strip()

        if choice == '1':
            city = input("Enter the city name: ")
            weather_info = get_weather(city)
            earthquake_info = get_earthquake_info()

            # Desktop notification for weather
            notification.notify(
                title=f"Weather in {city}",
                message=weather_info,
                timeout=10
            )

            # Introduce a delay of 5 seconds before showing the earthquake notification
            time.sleep(5)

            # Desktop notification for earthquake
            notification.notify(
                title="Earthquake Alert",
                message=earthquake_info,
                timeout=10
            )
        elif choice == '2':
            break

    print()
    print("*-----------------------------------------------------------------------------*")
    print("**--------              Thanks for Using the System!!!               --------**")
    print("*-----------------------------------------------------------------------------*")
    print()
    print()


if __name__ == "__main__":
    main()
