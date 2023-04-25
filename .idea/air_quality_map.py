import requests
import pandas as pd
import folium
import schedule
import time

# TFL API endpoint URL
url = 'https://api.tfl.gov.uk/AirQuality'

# TFL API headers with app ID and app key
headers = {'app_id': '<your_app_id>', 'app_key': '<your_app_key>'}

# Define a function to get the air quality data and create a map
def get_air_quality_data():
    try:
        # Make a GET request to the TFL API
        response = requests.get(url, headers=headers)

        # Check the response status code
        if response.status_code == 200:
            # Parse the JSON data from the response
            data = response.json()['$value']
            df = pd.DataFrame(data)

            # Group the data by borough and calculate the average values
            grouped_data = df.groupby('SiteName').mean()

            # Create a Folium map and add markers for each borough
            map = folium.Map(location=[grouped_data['Latitude'].mean(),
                                       grouped_data['Longitude'].mean()],
                             zoom_start=10)

            for index, row in grouped_data.iterrows():
                folium.Marker(location=[row['Latitude'], row['Longitude']],
                              popup='{}: {} µg/m³'.format(index, round(row['Value'], 2))).add_to(map)

            # Save the map to an HTML file
            map.save('air_quality_map.html')
        else:
            # If the response status code is not 200, print an error message
            print(f'Response status code: {response.status_code}')
            print('Waiting for TFL coming soon...')
    except requests.exceptions.RequestException as e:
        # If there is an error making the request, print an error message
        print('Error:', e)
        print('Waiting for TFL coming soon...')

# Schedule the function to run every 30 seconds
schedule.every(30).seconds.do(get_air_quality_data)

# Run the scheduled function indefinitely
while True:
    schedule.run_pending()
    time.sleep(1)

# © 2023 Alphonce Ochieng - All Rights Reserved
