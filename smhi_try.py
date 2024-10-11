import requests
import json
import time
from collections import defaultdict
from datetime import datetime
#import RPi.GPIO as GPIO
"""
LED_PIN = 18 # Sätt rätt pin nummer här
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)
"""


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

going_to_r = None 

def fetch_data():
    #return mock_response # Använd denna för att testa
    response = requests.get(API_URL)
    return response.json()

def filter_data(data):

    global going_to_r # Vet inte om detta är nödvändigt

    #Nu lägger jag för både snö och regn men det ska vara bara för snö
    #desired_wsymb2_snow = {15, 16, 17, 25, 26, 27}
    #desired_pcat_snow = {1, 2}

    desired_wysmb2_rain = {15, 16, 17, 25, 26, 27}
    desired_pcat_rain = {2, 3}
    
    going_to_r = None # Vet inte om detta är nödvändigt
    
    checked_parameters = []
    rain_days = defaultdict(list)

    for time_series in data.get('timeSeries', []):
        for parameter in time_series.get('parameters', []):
            if parameter.get('name') in ['Wsymb2', 'pcat']:
                checked_parameters.append(parameter) # Spara alla parametrar som vi har kollat på
                if parameter.get('name') == 'pcat' and parameter['values'][0] in desired_pcat_rain:
                    going_to_r = True
                    rain_days[time_series['validTime'][:10]].append(time_series['validTime'])
                elif parameter.get('name') == 'Wsymb2' and parameter['values'][0] in desired_wysmb2_rain:
                    going_to_r = True
                    rain_days[time_series['validTime'][:10]].append(time_series['validTime'])


    for param in checked_parameters:
        print(f"Checked parameter: {param}")

    
    if going_to_r is True:
        # Borde implementera att printas datan för de dagarna som ska regna samt filtrera ut de dagar som är närmast för att undvika att väder ändras 
        # Kanske använda datetime för att filtrera ut de dagar som är närmast samt loopa konstant funktionen för att kolla om väderprognosen ändras
        
        
        single_times = []
        multiple_times = {}

        for day, times in sorted(rain_days.items()):
            if len(times) > 1:
                multiple_times[day] = sorted(set(times))
            else:
                single_times.append(times[0])
 
        for day, times in multiple_times.items():
            print(f"Det kommer att regna denna datum {day} i dessa tidspunkter:")
            for time in times:
                print(f"T{time[11:]}")
                

        if single_times:
            print("\nDet kommer att regna dessa dagar:")
            for time in single_times:
                print(time)

        return True
        
    return False

"""
def control_led(is_raining):
    if is_raining:
        GPIO.output(LED_PIN, GPIO.HIGH)
    else:
        GPIO.output(LED_PIN, GPIO.LOW)
"""

def send_command(command):
    if command == 'Det kommer att regna':
        print("PWR ON")
    
    elif command == 'Det kommer inte att regna':
        print("Det kommer inte att regna på de närmaste 10 dagarna")
        print("STBY")
        
    
def main():
    global going_to_r # Vet inte om detta är nödvändigt

    try: 
        while True:
            data = fetch_data()
            if filter_data(data):
                send_command('Det kommer att regna')
                # Borde implementera funktion som schemalägger kommando beroende på när det ska regna 
                # beroende på datan och datumet som man får tillbaka från SMHI API 
        
            else:
                send_command('Det kommer inte att regna')
            time.sleep(3600)
    
    except KeyboardInterrupt:
        #GPIO.cleanup() # Använd denna för att stänga av GPIO
        print('Avslutar programmet')
        exit(0)
    
    
if __name__ == '__main__':
    main()




"""
Det kommer att regna denna datum 2024-10-13 i dessa tidspunkter:
T05:00:00Z
T06:00:00Z
T07:00:00Z
T08:00:00Z
T09:00:00Z
T10:00:00Z
T11:00:00Z

Det kommer att regna dessa dagar:
2024-10-18T00:00:00Z

2024-10-19T00:00:00Z

2024-10-20T12:00:00Z

2024-10-21T00:00:00Z
"""