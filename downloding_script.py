import csv
import requests
import os

os.makedirs('icons', exist_ok=True)

with open('/Users/shrey/Downloads/weather_conditions.csv', mode='r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        icon_code = row['icon']
        icon_url = f"https://cdn.weatherapi.com/weather/64x64/night/{icon_code}.png"
        response = requests.get(icon_url)
        if response.status_code == 200:
            with open(f'icons/{icon_code}.png', 'wb') as img_file:
                img_file.write(response.content)
        else:
            print(f"Failed to download {icon_url}")
