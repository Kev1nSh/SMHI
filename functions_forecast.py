import requests
from datetime import datetime
from tabulate import tabulate


base_url_forecast = "https://opendata-download-metfcst.smhi.se/api"

time_periods = {'latest-hour', 'latest-day', 'latest-months'}




def fetch_data_forecast(endpoint):
    response = requests.get(endpoint)
    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to retrieve data:", response.status_code)
        return None

def convert_timestamp(timestamp):
    dt_object = datetime.fromtimestamp(timestamp / 1000)
    return dt_object.strftime("%Y-%m-%d %H:%M:%S")


def getCoords():
    lat = float(input("Enter latitude: "))
    lon = float(input("Enter longitude: "))
    return lat, lon



    




#https://opendata-download-metfcst.smhi.se/api/category/pmp3g/version/2/geotype/point/lon/18.1/lat/59.2/data.json

def get_nearest_available_point_data(longitude, latitude):
    longitude_str = f"{longitude:.3f}"
    latitude_str = f"{latitude:.3f}"
    pointsearchurl = f"{base_url_forecast}/category/pmp3g/version/2/geotype/point/lon/{longitude_str}/lat/{latitude_str}/data.json"
    print(f"Request UTL: {pointsearchurl}")
    response = requests.get(pointsearchurl)
 
    if response.status_code == 200:
        data = response.json()
        returned_longitude = data['geometry']['coordinates'][0][0]
        returned_latitude = data['geometry']['coordinates'][0][1]
        print(f"Nearest point found at: {returned_longitude}, {returned_latitude}")
    else:
        print("Failed to retrieve data:", response.status_code)
        return None

max_lat = 68.8032  #Saarikoski
min_lat = 55.3811  #Trelleborg
max_long = 24.1112  #Haparanda
min_long = 11.2178  #Smögen


#Saarikoski 68.8032, longitud: 21.2468
#trelleborg 55.3811, longitud: 13.1195
#smögen     58.3536, longitud: 11.2178 
#haparanda  65.8237, longitud: 24.1112

#lowest lat: 55.3811, long: 13.1195

def coord_input_loop():
    while(True):
        longitude = float(input("Enter longitude: "))
        if longitude < min_long or longitude > max_long:
            print("Longitude out of range for sweden")
            continue
        latitude = float(input("Enter latitude: "))
        if latitude < min_lat or latitude > max_lat:
            print("Latitude out of range for sweden")
            continue
        else:
            return longitude, latitude

   



if __name__ == "__main__":

        longitude, latitude = coord_input_loop()

        data = get_nearest_available_point_data(longitude, latitude)
        citiesFromCoords(latitude, longitude)


  
   
  

   # parameter_keys,parameter_titles,  = get_parameters()
    #for key, title in zip(parameter_keys, parameter_titles):  ##kika mer på denna
     #   print(f"{key}: {title}")
   
  
        
   # get_parameters()
   # print_all_stations(1)
  # print_station_info(97400)
   # latest_value = fetch_latest_data(97400, 1)
   # print(latest_value)

    # GET /api/version/1.0/parameter/1/station/159880/period/latest-months.atom

    #Stockholm -Arlanda 97400
    #Stockholm -Bromma 97200
    #Stockholm -Observatoriekullen A 98230
    #Stockholm -Observatoriekullen  98210


