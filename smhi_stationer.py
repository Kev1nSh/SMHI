import requests

param_data = []
stations_data = []
cities = []

username = "kevin125sh"

def param_input_loop():
    global param_data
    
    while(True):
        paramNumber = (input("Enter parameter number: "))
        paramMatch = False


        for param in param_data:
                if param['key'] == paramNumber:
                    print("Parameter found, title:", {param['title']})
                    paramFound = True
                    break

        if not paramMatch:
            print("Parameter not found with the given number") 


def stad_input_loop():
    global stations_data

    while(True):
        stadName = input("Skriv staden:")
        stadMatch = False
        
        for stad in stations_data:
            if stadName in stad['name']:
                print("Stad hittad:", stadName)
                stadMatch = True
                break
        if not stadMatch:
            print("Stad ej hittad")

def fetch_cities():
    global cities

    """ geonames_url_p = "http://api.geonames.org/searchJSON"
    params = {
        'q' : '',
        'country' : 'SE',
        'featureClass' : 'P',
        'maxRows' : 1000,
        'username' : username
    } """

    geoname_url = "http://api.geonames.org/searchJSON?q=&country=SE&featureClass=P&maxRows=1000&username=kevin125sh"
    response = requests.get(geoname_url)
   
    data = response.json()
    
    for elememt in data['geonames']:
        city_name = elememt.get('name')
        cities.append({'name':city_name})
    
    print(cities)
    return cities
       


    """ 
    try:
        response = requests.get(geonames_url, params=params)
        response.raise_for_status()

    except requests.exceptions.RequestException as e:
        print("Error fetching data:", {e})
        return []
    
    try:
        data = response.json()
    except ValueError:
        print("Error decoding JSON")
        return []
    if 'geonames' not in data:
        print("No geonames in response")
        return []
    
    for element in data['geonames']:
        cities.append(element['name'])
        city_name = element.get['name']
        lat = element.get['lat']
        lon = element.get['lon']

        if city_name and lat and lon:
            cities.append({'name': city_name, 'lat': lat, 'lon': lon})
    
    return cities 
    """

def fetch_parameters():
    global param_data

    url = "https://opendata-download-metobs.smhi.se/api/version/1.0/parameter.json"

    response = requests.get(url)
    
    if response.status_code == 200:

        parameter_data = response.json()
        param_data = parameter_data.get('resource', [])

        for param in param_data:
            print(param['key'])
            print(param['title'])
            print(param['summary'])
            """ 
            print(param['updated'])
            print(param['title'])
            print(param['summary'])
            print(param['unit'])  """
            print('-' * 20) 
        

    else: 
        print(f'Error fetching data, error code:', {response.status_code}) 


def fetch_stations():
    global stations_data

    url = "https://opendata-download-metobs.smhi.se/api/version/1.0/parameter/1/station.json"

    response = requests.get(url)

    if response.status_code == 200:
        
        data = response.json()
        stations_data = data.get('station', [])  

        for station in stations_data:
            print(station['name'])
            print(station['id'])
            print(station['latitude'])
            print(station['longitude'])
            print(station['height'])
            print(station['active'])
            print('-' * 20)
    else:
        print(f'Error fetching data, error code:', {response.status_code})  
    
if __name__ == '__main__':
    #fetch_stations()
    #fetch_parameters()
    #param_input_loop()
    
    #stad_input_loop()
    fetch_cities()

'''
 13 Rådande väder
 17 Nederbörd 2 gånger per dygn, 06 och 18
 27 Lufttemperatur 2 gånger per dygn, 06 och 18

'''