import tkinter as tk
from tkinter import ttk, messagebox
import webbrowser
import requests
import pandas as pd
import folium
import os
import platform
import subprocess

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

# Mocked IQAir request for demonstration purposes
def mock_iqair_request():
    return {
        "status": "success",
        "data": {
            "city": "London",
            "state": "England",
            "country": "UK",
            "location": {"type": "Point", "coordinates": [-0.1276474, 51.5072955]},
            "current": {
                "weather": {
                    "ts": "2023-10-04T11:00:00.000Z",
                    "tp": 13,
                    "pr": 1017,
                    "hu": 87,
                    "ws": 1.5,
                    "wd": 90,
                    "ic": "10d"
                },
                "pollution": {
                    "ts": "2023-10-04T10:00:00.000Z",
                    "aqius": 58,
                    "mainus": "p2",
                    "aqicn": 25,
                    "maincn": "p2"
                }
            }
        }
    }

# Function to fetch air quality data from IQAir and update the GUI
def fetch_air_quality_iqair():
    response_data = mock_iqair_request()
    air_quality_index = response_data["data"]["current"]["pollution"]["aqius"]
    label_result.config(text=f"Air quality index for London is {air_quality_index}.")
    m = folium.Map(location=[51.5074, -0.1278], zoom_start=10)
    folium.Marker(location=[51.5074, -0.1278], popup=f'London: {air_quality_index} AQI').add_to(m)
    m.save('air_quality_map.html')

# Function to provide recommendations based on air quality value
def show_recommendation():
    try:
        aqi = int(label_result.cget("text").split()[-1])
        if aqi <= 50:
            recommendation = "Air quality is good. No precautions necessary."
        elif 50 < aqi <= 100:
            recommendation = "Air quality is moderate. If you are particularly sensitive, consider staying indoors."
        else:
            recommendation = "Air quality is poor. Consider staying indoors and using an air purifier."
        label_recommendation.config(text=recommendation)
    except:
        messagebox.showerror("Error", "Fetch the air quality index first.")

# Function to open the generated Folium map in the default web browser
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

# GUI building and event handling
window = tk.Tk()
window.title("Air Quality Checker")
window.geometry("600x400")
window.config(bg=bg_color)
frame_address = ttk.LabelFrame(window, text="Enter your address")
frame_address.grid(row=0, column=0, pady=20, padx=20, sticky='nsew')
address_entry = ttk.Entry(frame_address, width=40, background=entry_bg, foreground=entry_fg)
address_entry.grid(row=0, column=0, pady=10, padx=10, sticky='nsew')
address_entry.insert(0, "City, State, Country...")
btn_fetch = ttk.Button(frame_address, text="Check Air Quality", command=fetch_air_quality_iqair)
btn_fetch.grid(row=1, column=0, pady=10, sticky='nsew')
label_result = ttk.Label(window, text="Air quality result will be displayed here.", bg=bg_color, fg=text_color)
label_result.grid(row=1, column=0, pady=20, sticky='nsew')
btn_map = ttk.Button(window, text="Open Air Quality Map", command=open_map)
btn_map.grid(row=2, column=0, pady=10, sticky='nsew')
label_recommendation = ttk.Label(window, text="", bg=bg_color, fg=text_color)
label_recommendation.grid(row=3, column=0, pady=20, sticky='nsew')
btn_recommendation = ttk.Button(window, text="Get Recommendation", command=show_recommendation)
btn_recommendation.grid(row=4, column=0, pady=10, sticky='nsew')

# Start the GUI's main loop (only if the script is run as the main module)
if __name__ == "__main__":
    window.mainloop()

# All Rights Reserved. © 2023 Alphonce Ochieng
"""

annotated_script_content
