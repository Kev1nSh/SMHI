import requests
import json
import time
import RPi.GPIO as GPIO

LED_PIN = 18 # Sätt rätt pin nummer här
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)



API_URL = "https://opendata-download-metfcst.smhi.se/api/category/pmp3g/version/2/geotype/point/lon/18.063240/lat/59.334591/data.json"  

pcat_meanings = {
    1: 'none',
    2: 'snow',
    3: 'snow and rain',
    4: 'rain',
    5: 'drizzle',
    6: 'freezing rain',
    7: 'freezing drizzle'
}

wsymb2_meanings = {
    1: 'clear sky',
    2: 'nearly clear sky',
    3: 'variable cloudiness',
    4: 'halfclear sky',
    5: 'cloudy sky',
    6: 'overcast',
    7: 'fog',
    8: 'light rain showers',
    9: 'moderate rain showers',
    10: 'heavy rain showers',
    11: 'thunderstorm',
    12: 'light sleet showers',
    13: 'moderate sleet showers',
    14: 'heavy sleet showers',
    15: 'light snow showers',
    16: 'moderate snow showers',
    17: 'heavy snow showers',
    18: 'light rain',
    19: 'moderate rain',
    20: 'heavy rain',
    21: 'thunder',
    22: 'light sleet',
    23: 'moderate sleet',
    24: 'heavy sleet',
    25: 'light snowfall',
    26: 'moderate snowfall',
    27: 'heavy snowfall'
}

mock_response = {
     "timeSeries": [
        {
            "validTime": "2024-10-10T18:00:00Z",
            "parameters": [
                {"name": "Wsymb2", "values": [1]},
                {"name": "pcat", "values": [6]}
            ]
        },
        {
            "validTime": "2024-10-10T19:00:00Z",
            "parameters": [
                {"name": "Wsymb2", "values": [1]},
                {"name": "pcat", "values": [6]}
            ]
        }
    ]

}

def fetch_data():
    return mock_response
    #response = requests.get(API_URL)
    #return response.json()

def filter_data(data):

    #Nu lägger jag för både snö och regn men det ska vara bara för snö
    #desired_wsymb2_snow = {15, 16, 17, 25, 26, 27}
    #desired_pcat_snow = {1, 2}

    desired_wysmb2_rain = {15, 16, 17, 25, 26, 27}
    desired_pcat_rain = {2, 3}
    
    is_raining = False

    for time_series in data.get('timeSeries', []):
        for parameter in time_series.get('parameters', []):
            print(f"CHecking parameter {parameter}")
            #Printar ut alla parametrar för att se vad som finns, 
            #lär behövas tar bort senare eftersom för mycket data att printa med det rikitga datan 
            if parameter.get('name') == 'pcat' and parameter['values'][0] in desired_pcat_rain:
                print('Det kommer att regna')
                is_raining = True
            elif parameter.get('name') == 'Wsymb2' and parameter['values'][0] in desired_wysmb2_rain:
                is_raining = True
        if is_raining:
            return True
    return False

def control_led(is_raining):
    if is_raining:
        GPIO.output(LED_PIN, GPIO.HIGH)
    else:
        GPIO.output(LED_PIN, GPIO.LOW)

def send_command(command):
    if command == 'Det kommer att regna':
        print("PWR ON")
    
    elif command == 'Det kommer inte att regna':
        print("Det kommer inte att regna på de närmaste 10 dagarna")
        print("STBY")
        
    
def main():
    try: 
        while True:
            data = fetch_data()
            if filter_data(data):
                send_command('Det kommer att regna')
        
            else:
                send_command('Det kommer inte att regna')
            time.sleep(3600)
    
    except KeyboardInterrupt:
        GPIO.cleanup()
        #print('Avslutar programmet')
        #exit(0)
    
    
if __name__ == '__main__':
    main()