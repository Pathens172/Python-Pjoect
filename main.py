import requests
import tkinter as tk
from tkinter import messagebox

# Replace this with your real OpenWeatherMap API key
API_KEY = "your_api_key_here"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

def get_weather(city, unit):
    """Fetch current weather data."""
    if unit == 'C':
        unit = 'metric'  # Celsius
    elif unit == 'F':
        unit = 'imperial'  # Fahrenheit
    elif unit == 'K':
        unit = 'standard'  # Kelvin
    else:
        messagebox.showerror("Error", "Invalid unit!")
        return
    
    params = {"q": city, "appid": API_KEY, "units": unit}
    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()  # Raise error for bad status codes
        data = response.json()
        return {
            "city": data["name"],
            "temperature": data["main"]["temp"],
            "description": data["weather"][0]["description"],
            "humidity": data["main"]["humidity"],
            "wind_speed": data["wind"]["speed"],
        }
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"Request failed: {e}")
        return {"error": "API error."}

def show_weather():
    """Show weather info when the button is clicked."""
    city = city_entry.get()  # Get the city name the user typed
    unit = unit_var.get()  # Get the unit the user selected

    # Check if city or unit is missing
    if not city:  # If no city is entered
        messagebox.showerror("Error", "Please enter a city name.")  # Show error message
        return

    # Fetch the weather data
    weather = get_weather(city, unit)

    if "error" in weather:  # If there's an error with the weather request
        messagebox.showerror("Error", weather["error"])
    else:
        # Display the weather information in a label
        result_label.config(text=f"City: {weather['city']}\n"
                                f"Temperature: {weather['temperature']}°{unit}\n"
                                f"Weather: {weather['description']}\n"
                                f"Humidity: {weather['humidity']}%\n"
                                f"Wind Speed: {weather['wind_speed']} m/s")

# Set up the main window
root = tk.Tk()
root.title("Weather App")  # Set the title of the window

# Create labels and entries for city name and units
city_label = tk.Label(root, text="Enter City:")
city_entry = tk.Entry(root)

unit_label = tk.Label(root, text="Select Unit (C/F/K):")
unit_var = tk.StringVar()
unit_menu = tk.OptionMenu(root, unit_var, 'C', 'F', 'K')
unit_var.set('C')  # Default unit is Celsius

# Create a button to fetch the weather
get_weather_button = tk.Button(root, text="Get Weather", command=show_weather)

# Create a label to display the results
result_label = tk.Label(root, text="", justify="left")

# Add padding for neatness
city_label.pack(pady=5)
city_entry.pack(pady=5)
unit_label.pack(pady=5)
unit_menu.pack(pady=5)
get_weather_button.pack(pady=10)
result_label.pack(pady=10)

# Run the app
root.mainloop()
