import adafruit_display_text.label
import board
import displayio
import framebufferio
import rgbmatrix
import terminalio
import requests
import time

displayio.release_displays()

matrix = rgbmatrix.RGBMatrix(
    width=64, height=32, bit_depth=1,
    rgb_pins=[board.D6, board.D5, board.D9, board.D11, board.D10, board.D12],
    addr_pins=[board.A5, board.A4, board.A3, board.A2],
    clock_pin=board.D13, latch_pin=board.D0, output_enable_pin=board.D1)

display = framebufferio.FramebufferDisplay(matrix, auto_refresh=False)


location = "Toronto"

response = requests.get(f"http://api.weatherapi.com/v1/current.json?key=35e9192ccc59453bb91171820252901&q={location}&aqi=no")
weather_data = response.json()

uv = weather_data['current']['uv']
temp_c = weather_data['current']['temp_c']
condition = weather_data['current']['condition']['text']
icon_url = "http:" + weather_data['current']['condition']['icon']
wind_kph = weather_data['current']['wind_kph']
precip_mm = weather_data['current']['precip_mm']
feelslike_c = weather_data['current']['feelslike_c']
day = weather_data['current']['is_day']

print(f"Temperature (C): {temp_c}")
print(f"Condition: {condition}")
print(f"Wind (kph): {wind_kph}")
print(f"Precipitation (mm): {precip_mm}")
print(f"Feels Like (C): {feelslike_c}")

def create_label(text, x, y, color):
    return adafruit_display_text.label.Label(
        terminalio.FONT, text=text, color=color, x=x, y=y, scale=1)

def get_uv_color(uv):
    if uv <= 1:
        return 0x00FF00  # Green
    elif uv <= 2:
        return 0xADFF2F  # Green-ish Yellow
    elif uv <= 3:
        return 0xFFFF00  # Yellow
    elif uv <= 4:
        return 0xFFD700  # Light Orange
    elif uv <= 5:
        return 0xFFA500  # Orange
    elif uv <= 6:
        return 0xFF4500  # Light Red
    elif uv <= 7:
        return 0xFF0000  # Red
    elif uv <= 8:
        return 0x800000  # Maroon
    elif uv <= 9:
        return 0xFFB6C1  # Light Pink
    else:
        return 0x800080  # Purple

def get_temp_color(temp):
    if temp <= 0:
        return 0x0000FF  # Blue
    elif temp <= 15:
        return 0x00FFFF  # Cyan
    elif temp <= 25:
        return 0x00FF00  # Green
    elif temp <= 35:
        return 0xFFFF00  # Yellow
    else:
        return 0xFF0000  # Red

datax = 32

def display_weather_stats():
    group = displayio.Group()
    group.append(create_label(f"Temp:", x=0, y=4, color=0xFFFFFF))
    group.append(create_label(f"{temp_c}c", x=datax, y=4, color=get_temp_color(temp_c)))
    group.append(create_label(f"Feel:", x=0, y=16, color=0xFFFFFF))
    group.append(create_label(f"{feelslike_c}c", x=datax, y=16, color=get_temp_color(feelslike_c)))
    if precip_mm > 0:
        group.append(create_label(f"Precip:", x=0, y=26, color=0xFFFFFF))
        group.append(create_label(f"{precip_mm}mm", x=datax, y=26, color=0xFFFFFF))
    else:
        group.append(create_label(f"UV:", x=0, y=26, color=0xFFFFFF))
        group.append(create_label(f"{uv}", x=datax, y=26, color=get_uv_color(uv)))
    display.root_group = group
    display.refresh(minimum_frames_per_second=0)

def display_weather_icon():
    group = displayio.Group()

    background_bitmap = displayio.Bitmap(display.width, display.height, 1)
    background_palette = displayio.Palette(1)
    background_palette[0] = 0xFFFFFF  # White
    background_tile_grid = displayio.TileGrid(background_bitmap, pixel_shader=background_palette)
    group.append(background_tile_grid)
    
    code = icon_url.split('/')[-1].split('.')[0]
    print("THE CODE IS" + str(code))
    if day:
        filename = f"d{code}.bmp"
    else:
        filename = f"n{code}.bmp"
    try:
        bitmap = displayio.OnDiskBitmap(filename)
    except FileNotFoundError:
        bitmap = displayio.OnDiskBitmap("d320.bmp")
    tile_grid = displayio.TileGrid(bitmap, pixel_shader=bitmap.pixel_shader, x=0, y=-16)
    group.append(tile_grid)
    display.root_group = group
    display.refresh(minimum_frames_per_second=0)

while True:
    display_weather_stats()
    time.sleep(5)
    display_weather_icon()
    time.sleep(5)
    