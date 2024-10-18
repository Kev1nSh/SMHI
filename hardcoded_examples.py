import requests

base_url_metobs = "https://opendata-download-metobs.smhi.se/api"
endpointsthlm = f"{base_url_metobs}/version/1.0/parameter/1/station/98230/period/latest-hour/data.json"

def fetch_latest_hour_temp_stockholm():
    metadata = fetch_data_metobs(endpointsthlm)
    if 'value' in metadata and len(metadata['value']) > 0:
        latest_entry = metadata['value'][0]
        temperature = latest_entry.get('value')
        timestamp = latest_entry.get('date')
        human_readable_timestamp = convert_timestamp(timestamp)
      #  print(f"Temperature: {temperature} degrees Celsius at {human_readable_timestamp}")
        return float(temperature)
    else:
        print("No temperature data found")