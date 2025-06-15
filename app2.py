import requests
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from io import BytesIO

API_KEY = "491236870f82e91a0c8a72d52df1faed"

def get_weather():
    city = city_entry.get()
    if not city:
        messagebox.showwarning("Input Error", "Please enter a city name.")
        return

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

    try:
        response = requests.get(url)
        data = response.json()

        if data["cod"] != 200:
            messagebox.showerror("Error", data.get("message", "Cannot fetch weather data."))
            return

        temp = data["main"]["temp"]
        condition = data["weather"][0]["main"]
        desc = data["weather"][0]["description"]
        city_name = data["name"]
        icon_code = data["weather"][0]["icon"]

        weather_label.config(text=f"{city_name}\n{condition} ({desc})\n{temp}°C")
        update_background(condition)
        show_icon(icon_code)

    except Exception as e:
        messagebox.showerror("Error", f"Something went wrong:\n{e}")

def update_background(condition):
    condition = condition.lower()
    if "clear" in condition:
        frame.config(bg="#FFD700")  # Sunny
    elif "cloud" in condition:
        frame.config(bg="#B0C4DE")  # Cloudy
    elif "rain" in condition or "drizzle" in condition:
        frame.config(bg="#87CEFA")  # Rainy
    elif "thunderstorm" in condition:
        frame.config(bg="#778899")  # Thunder
    elif "snow" in condition:
        frame.config(bg="#FFFFFF")  # Snow
    else:
        frame.config(bg="#D3D3D3")  # Default Gray
    weather_label.config(bg=frame["bg"])
    icon_label.config(bg=frame["bg"])

def show_icon(icon_code):
    icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
    response = requests.get(icon_url)
    img_data = response.content
    img = Image.open(BytesIO(img_data))
    img = img.resize((80, 80), Image.Resampling.LANCZOS)
    photo = ImageTk.PhotoImage(img)
    icon_label.config(image=photo)
    icon_label.image = photo  # Keep reference

# --- GUI Setup ---
root = tk.Tk()
root.title("Weather App with Icons")
root.geometry("400x350")
root.config(bg="#ECECEC")

tk.Label(root, text="Enter City Name:", bg="#ECECEC", font=("Arial", 12)).pack(pady=10)

city_entry = tk.Entry(root, font=("Arial", 12))
city_entry.pack()

tk.Button(root, text="Get Weather", command=get_weather, font=("Arial", 12)).pack(pady=10)

frame = tk.Frame(root, bg="#D3D3D3", bd=2, relief=tk.RIDGE)
frame.pack(pady=20, fill="both", expand=True)

weather_label = tk.Label(frame, text="", font=("Arial", 14), bg="#D3D3D3")
weather_label.pack(pady=10)

icon_label = tk.Label(frame, bg="#D3D3D3")
icon_label.pack()

root.mainloop()
