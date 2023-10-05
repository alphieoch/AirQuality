import tkinter as tk
from tkinter import ttk, messagebox
import webbrowser
import requests
import folium
import platform
import subprocess
import warnings
import geocoder
from urllib3.exceptions import InsecureRequestWarning

# Suppress SSL warnings
warnings.simplefilter('ignore', InsecureRequestWarning)

# Function to detect the system's theme (dark/light mode)
def get_system_theme():
    system_platform = platform.system()
    if system_platform == "Windows":
        import winreg as reg
        key_path = r'SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Themes\\Personalize'
        with reg.OpenKey(reg.HKEY_CURRENT_USER, key_path) as key:
            theme = reg.QueryValueEx(key, 'AppsUseLightTheme')[0]
            if theme == 1:
                return 'light'
            else:
                return 'dark'
    elif system_platform == "Darwin":
        cmd = "defaults read -g AppleInterfaceStyle"
        try:
            theme = subprocess.check_output(cmd, shell=True)
            if theme.strip().decode() == "Dark":
                return 'dark'
            else:
                return 'light'
        except subprocess.CalledProcessError:
            return 'light'
    return 'light'

def fetch_current_location():
    try:
        location = geocoder.ip('me')
        city = location.city
        region = location.state
        country = location.country
        address_entry.delete(0, tk.END)
        address_entry.insert(0, f"{city}, {region}, {country}")
        fetch_air_quality_iqair()
    except geocoder.GeocoderTimedOut:
        messagebox.showerror("Error", "Geocoder timed out. Please check your internet connection and try again.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

def fetch_air_quality_iqair():
    address = address_entry.get()
    api_url = f"https://api.iqair.com/v1/forecast/{address}"
    api_key = "c58f03e3-9d50-47b7-9306-08808afda89c"  # Replace with your IQAir API key
    response = requests.get(api_url, headers={"Authorization": f"Bearer {api_key}"})
    if response.status_code == 200:
        response_data = response.json()
        air_quality_index = response_data["data"]["current"]["pollution"]["aqius"]
        city_name = response_data["data"]["city"]
        label_result.config(text=f"Air quality index for {city_name} is {air_quality_index}.")

        # Mask rating logic
        if air_quality_index <= 50:
            mask_rating = 1
        elif 50 < air_quality_index <= 100:
            mask_rating = 3
        elif 100 < air_quality_index <= 150:
            mask_rating = 5
        elif 150 < air_quality_index <= 200:
            mask_rating = 7
        elif 200 < air_quality_index <= 300:
            mask_rating = 9
        else:
            mask_rating = 10
        label_mask_rating.config(text=f"Face Mask Rating: {mask_rating}/10")

        lat = response_data["data"]["location"]["coordinates"][1]
        lon = response_data["data"]["location"]["coordinates"][0]
        m = folium.Map(location=[lat, lon], zoom_start=10)
        folium.Marker(location=[lat, lon], popup=f'{city_name}: {air_quality_index} AQI').add_to(m)
        m.save('air_quality_map.html')
    else:
        messagebox.showerror("Error", "Failed to fetch air quality data. Please try again.")

def display_help():
    help_message = """
    Air Quality Checker Help:

    1. Enter your address (City, State, Country) in the provided textbox.
    2. Press 'Check Air Quality' to fetch the air quality index for that address.
    3. Alternatively, press 'Use Current Location' to automatically detect your location and fetch the air quality.
    4. The program will display the Air Quality Index (AQI) and a Face Mask Rating (on a 1-10 scale).
        - Rating 1: Air quality is good. No need for a mask.
        - Rating 10: Air quality is hazardous. It's highly recommended to wear a mask.
    5. Press 'Open Air Quality Map' to view the map with your location and AQI information.
    6. For recommendations on precautions, press 'Recommendations'.

    Remember, the air quality data is fetched from IQAir and may vary in real-time.
    """
    messagebox.showinfo("Help", help_message)

def display_about():
    about_message = """
    Air Quality Checker:

    This application fetches real-time air quality data from IQAir, a leading global air quality monitoring and data platform.

    The Face Mask Rating provided is a simple guide based on the Air Quality Index (AQI) to help users determine the necessity of wearing a mask. A rating closer to 10 indicates a higher recommendation to wear a mask.

    All data and recommendations are for informational purposes only. Always refer to local guidelines and health recommendations.

    All Rights Reserved. © 2023 Alphonce Ochieng
    """
    messagebox.showinfo("About", about_message)

def open_map():
    webbrowser.open('air_quality_map.html')

# GUI theme detection and color setup
theme = get_system_theme()
if theme == 'dark':
    bg_color = '#333333'
    text_color = '#FFFFFF'
    btn_color = '#444444'
    entry_bg = '#444444'
    entry_fg = '#FFFFFF'
else:
    bg_color = '#FFFFFF'
    text_color = '#000000'
    btn_color = '#DDDDDD'
    entry_bg = '#FFFFFF'
    entry_fg = '#000000'

# Create a style object for ttk
style = ttk.Style()
style.configure('Custom.TLabel', background=bg_color, foreground=text_color)

# GUI building
window = tk.Tk()
window.title("Air Quality Checker")
window.geometry("600x400")
window.config(bg=bg_color)

frame_address = ttk.LabelFrame(window, text="Enter your address")
frame_address.grid(row=0, column=0, pady=20, padx=20, sticky='nsew')

address_entry = ttk.Entry(frame_address, width=40)
address_entry.grid(row=0, column=0, pady=10, padx=10, sticky='nsew')
address_entry.insert(0, "City, State, Country...")

btn_fetch = ttk.Button(frame_address, text="Check Air Quality", command=fetch_air_quality_iqair)
btn_fetch.grid(row=1, column=0, pady=10, sticky='nsew')

btn_current_location = ttk.Button(frame_address, text="Use Current Location", command=fetch_current_location)
btn_current_location.grid(row=2, column=0, pady=10, sticky='nsew')

label_result = ttk.Label(window, text="Air quality result will be displayed here.", style='Custom.TLabel')
label_result.grid(row=1, column=0, pady=20, sticky='nsew')

label_mask_rating = ttk.Label(window, text="Face Mask Rating will be displayed here.", style='Custom.TLabel')
label_mask_rating.grid(row=2, column=0, pady=10, sticky='nsew')

btn_map = ttk.Button(window, text="Open Air Quality Map", command=open_map)
btn_map.grid(row=3, column=0, pady=10, sticky='nsew')

btn_recommendations = ttk.Button(window, text="Recommendations", command=display_help)  # Reuse the help function here
btn_recommendations.grid(row=4, column=0, pady=10, sticky='nsew')

btn_about = ttk.Button(window, text="About", command=display_about)
btn_about.grid(row=5, column=0, pady=10, sticky='nsew')

btn_help = ttk.Button(window, text="?", command=display_help, width=2)
btn_help.grid(row=0, column=1, pady=10, sticky='nsew')

window.mainloop()

# All Rights Reserved. © 2023 Alphonce Ochieng
