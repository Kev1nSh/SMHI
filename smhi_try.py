import requests
import json
import time
from collections import defaultdict
from datetime import datetime, timedelta
import RPi.GPIO as GPIO

LED_PIN = 26 # Sätt rätt pin nummer här
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
            "validTime": "2024-10-14T17:00:00Z",
            "parameters": [
                {"name": "Wsymb2", "values": [1]},
                {"name": "pcat", "values": [1]}
            ]
        },
        {
            "validTime": "2024-10-14T18:00:00Z",
            "parameters": [
                {"name": "Wsymb2", "values": [1]},
                {"name": "pcat", "values": [4]}
            ]
        }
    ]

}

going_to_r = None 
use_mock_data = True # Byt till True för att använda mock data

def fetch_data():
    if use_mock_data:
        return mock_response # Använd denna för att testa
    else:
        response = requests.get(API_URL)
        return response.json()

def filter_data(data):

    global going_to_r # Vet inte om detta är nödvändigt

    #Nu lägger jag för både snö och regn men det ska vara bara för snö
    #desired_wsymb2_snow = {15, 16, 17, 25, 26, 27}
    #desired_pcat_snow = {1, 2}

    desired_wysmb2_rain = {8, 9, 10, 18, 19, 20}
    desired_pcat_rain = {3, 4, 6}
    
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
                
        single_times = []
        multiple_times = {}

        for day, times in sorted(rain_days.items()):
            unique_times = sorted(set(times))
            if len(unique_times) > 1:
                multiple_times[day] = unique_times
            else:
                single_times.append(unique_times[0])
 
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


def control_led(is_raining):
    if is_raining:
        GPIO.output(LED_PIN, GPIO.HIGH)
    else:
        GPIO.output(LED_PIN, GPIO.LOW)


def send_command(command):
    
    #Här vi hämtar data från SMHI API
    data = fetch_data()
    current_time = datetime.now()
    one_hour_later = current_time + timedelta(hours=1)

    nearest_rain_time = None

    print(f"Current time: {current_time}")
    print(f"One hour later: {one_hour_later}")


    if command == 'Det kommer att regna':
        nearest_rain_time = None
        #Här vi kollar om det kommer att regna inom en timme
        for time_series in data.get('timeSeries', []):
            forecast_time = datetime.strptime(time_series['validTime'], "%Y-%m-%dT%H:%M:%SZ")

            pcat_match = False # Testar något nytt här
            wsymb2_match = False # Testar något nytt här

            for parameter in time_series.get('parameters', []):
                if parameter.get('name') in ['Wsymb2', 'pcat']:
                    if parameter.get('name') == 'pcat' and parameter['values'][0] in {3, 4, 6}:
                        if nearest_rain_time is None or (current_time <= forecast_time <= one_hour_later):
                            nearest_rain_time = forecast_time
                            print(forecast_time) # Bara för att kolla om det kommer hit
                            print("1") # Bara för att kolla om det kommer hit
                            pcat_match = True # Testar något nytt här
                            break         
                             
                    elif parameter.get('name') == 'Wsymb2' and parameter['values'][0] in {8, 9, 10, 18, 19, 20}:
                
                        if nearest_rain_time is None or (current_time <= forecast_time <= one_hour_later):
                            nearest_rain_time = forecast_time
                            print(forecast_time) # Bara för att kolla om det kommer hit
                            print("2") # Bara för att kolla om det kommer hit
                            wsymb2_match = True # Testar något nytt här
                            break         
            

            # Testar något nytt här, mest för att vara säker att vi får så accurate data som möjligt
            # Så att man inte skickar felaktiga kommandon till enheten bara för ena parametern matchar 
            # Behöver återkomma till detta senare
        """
            if pcat_match or wsymb2_match:                   
                if nearest_rain_time is None or (current_time <= forecast_time <= one_hour_later):
                    nearest_rain_time = forecast_time
                    print(forecast_time) # Bara för att kolla om det kommer hit
                    print("1") # Bara för att kolla om det kommer hit
                    break                
        """
        if nearest_rain_time:
            if current_time <= nearest_rain_time <= one_hour_later:
                print(f"Det kommer att regna om cirka 1 timme")
                print("PWR ON")
                control_led(True)
            
            else: 
                print(f"Den närmaste regn prognos är {nearest_rain_time}")
                print("STBY")  
                control_led(False)

            #print(nearest_rain_time) bara för att kolla om det funkar eller kommer dit
        else:
            print("Ingen regn prognos hittades") 
            print("STBY")
            control_led(False)
                               
    elif command == 'Det kommer inte att regna':
        print("Det kommer inte att regna på de närmaste 10 dagarna")
        print("STBY")
        control_led(False)

   
          
    
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
        GPIO.cleanup() # Använd denna för att stänga av GPIO
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


kod som behövs kollas upp igen:
  if command == 'Det kommer att regna':
        #Här vi kollar om det kommer att regna inom en timme
        for time_series in data.get('timeSeries', []):
            for parameter in time_series.get('parameters', []):
                if parameter.get('name') in ['Wsymb2', 'pcat']:
                    if parameter.get('name') == 'pcat' and parameter['values'][0] in {3, 4, 6}:
                        return forecast_time = datetime.strptime(time_series['validTime'], "%Y-%m-%dT%H:%M:%SZ")
                       
                    elif parameter.get('name') == 'Wsymb2' and parameter['values'][0] in {8, 9, 10, 18, 19, 20}:
                        return forecast_time = datetime.strptime(time_series['validTime'], "%Y-%m-%dT%H:%M:%SZ")
                        
        
    elif command == 'Det kommer inte att regna':
        print("Det kommer inte att regna på de närmaste 10 dagarna")
        print("STBY")
        control_led(False)

    if current_time <= forecast_time <= one_hour_later:
                            print(f"Det kommer att regna om en timme")
                            print("PWR ON")
                            control_led(True)
                            return
    else: 
        print(f"Den närmaste regn prognos är {forecast_time}")
        print("STBY")
        return        
    




"""