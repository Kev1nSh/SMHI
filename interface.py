import tkinter as tk
from tkinter import ttk
import smhi_try
from smhi_stationer import get_city_coords, get_station_coords, fetch_stations, fetch_cities, city_input_loop, get_city_coords, clear_terminal
 



def display_resutls(lat, lon, textwidget):
    textwidget.delete(1.0, tk.END)
    textwidget.insert(tk.END, f"Latitude: {lat}\n")
    textwidget.insert(tk.END, f"Longitude: {lon}\n")
    smhi_try.main(lat, lon, textwidget)

def on_submit(city_entry, text_widget):
    city_name = city_entry.get()
    lat, lon = get_city_coords(city_name)
    if lat is not None and lon is not None:
        display_resutls(lat, lon, text_widget)
    else:
        text_widget.insert(tk.END, "City not found\n")

# Create the main window
root = tk.Tk()
root.title("SMHI App")

# Create and place the input fields and labels
ttk.Label(root, text="City Name:").grid(row=0, column=0, padx=10, pady=10)
city_entry = ttk.Entry(root)
city_entry.grid(row=0, column=1, padx=10, pady=10)

# Create and place the submit button
submit_button = ttk.Button(root, text="Submit", command=lambda: on_submit(city_entry, text_widget))
submit_button.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

# Create and place the text widget for displaying the results
text_widget = tk.Text(root, height=20, width=50)
text_widget.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

# Initialize the data
fetch_stations()
fetch_cities()
clear_terminal()
# Run the app
root.mainloop()