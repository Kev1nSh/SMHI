import requests
import functions_forecast
import tabulate

base_url_metobs = "https://opendata-download-metobs.smhi.se/api"
endPointAll = f"{base_url_metobs}/version/1.0/parameter/1/station-set/all/period/latest-hour/data.json"
coordminmax = 0.6

def fetch_data_metobs(endpoint):
    response = requests.get(endpoint)
    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to retrieve data:", response.status_code)
        return None
    
def citiesFromCoords(lat, lon, coordminmax):
    data = fetch_data_metobs(endPointAll)
    matching_stations = []
    for station in data['station']:
        if station['latitude'] > lat - coordminmax and station['latitude'] < lat + coordminmax and station['longitude'] > lon - coordminmax and station['longitude'] < lon + coordminmax:
            matching_stations.append(station)
    if matching_stations:
        table = []
        for match in matching_stations:
            table.append([match['name'], match['key'], match['latitude'], match['longitude']])
        print(tabulate(table, headers=["Name", "Key", "Latitude", "Longitude"], tablefmt="pretty"))
        return matching_stations
    else:
        print("No stations nearby given coordinates")
      
        return None
               
def citiesFromCoords(lon, lat):
    matching_stations = []
    for station in data['station']:
        if station['latitude'] > lat - coordminmax and station['latitude'] < lat + coordminmax and station['longitude'] > lon - coordminmax and station['longitude'] < lon + coordminmax:
            matching_stations.append(station)
    if matching_stations:
        table = []
        for match in matching_stations:
            table.append([match['name'], match['key'], match['latitude'], match['longitude']])
        print(tabulate(table, headers=["Name", "Key", "Latitude", "Longitude"], tablefmt="pretty"))
        return matching_stations
    else:
        print("No stations nearby given coordinates")


def print_station_info(station_id, time_period):
    url = f"{base_url_metobs}/version/1.0/parameter/1/station/{station_id}/period/{time_period}.json"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        station_name = data['station']['title']
        print(f"Station: {station_name}")



def get_parameters_metobs():
    url = f"{base_url_metobs}/version/1.0.json"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        parameters = data['resource']
        parameter_keys = []
        parameter_titles  = []
        for parameter in parameters:
            key = parameter['key']
            title = parameter['title']
            parameter_keys.append(key)
            parameter_titles.append(title)
          #  print(f"{key}: {title}")
        return parameter_keys, parameter_titles
    else:
        print("Failed to retrieve parameters:", response.status_code)
        return []
    

def print_hardcoded_stationtemp_latestHour(parameter_key,station_id):
    url = f"{base_url_metobs}/version/1.0/parameter/{parameter_key}/station/{station_id}/period/latest-hour/data.json"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        station_name = data['station']['name']
        station_temp = data['value'][0]['value']
        timestamp = station_temp.get('date')
        print(f"Station: {station_name} - Temperature: {station_temp} at {timestamp}")
    else:
        print("Failed to retrieve data:", response.status_code)
