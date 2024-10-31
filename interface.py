import tkinter as tk
from tkinter import ttk
from customtkinter import *
import customtkinter as ctk
import smhi_try
from smhi_stationer import get_city_coords, get_station_coords, fetch_stations, fetch_cities, city_input_loop, get_city_coords, clear_terminal
 
def display_resutls(lat, lon, text_widget):
    text_widget.configure(state = "normal")
    text_widget.delete(1.0, ctk.END)
    smhi_try.main(lat, lon, text_widget)
    text_widget.configure(state = "disabled")
    resize_window()

def on_submit():
    city_name = city_entry.get()
    lat, lon = get_city_coords(city_name)
    if lat is not None and lon is not None:
        display_resutls(lat, lon, text_widget)
    else:
        text_widget.configure(state = "normal")
        text_widget.delete(1.0, ctk.END)
        text_widget.insert(ctk.END, "City not found\n")
        text_widget.configure(state = "disabled")
        resize_window()

def resize_window():
    text_widget.update_idletasks()
    req_width = text_widget.winfo_reqwidth()
    req_height = text_widget.winfo_reqheight()

    # Add some padding to the required width and height
    new_width = req_width + 150
    new_height = req_height + 10

    root.geometry(f"{new_width}x{new_height}")


set_appearance_mode("system")
set_default_color_theme("blue")

root = CTk()
root.title("SMHI App")
root.geometry("500x370")

# Configure the grid
root.grid_columnconfigure(0, weight = 1)
root.grid_columnconfigure(1, weight = 1)
root.grid_columnconfigure(2, weight = 1)


# Create the left frame
frame_left = ctk.CTkFrame(root)
frame_left.grid(row = 0, column = 0, columnspan = 2, padx = 20, pady = 20, sticky = "E")
#frame.pack(expand=True, fill="both", padx = 20, pady = 60)

# Create the label
CTkLabel(frame_left, text = "City Name:", font = ("Arial", 16)).grid(row = 0, column = 0, padx = 5, pady = 10, sticky = "E")

# Create the entry field
city_entry = ctk.CTkEntry(frame_left)
city_entry.grid(row = 0, column = 1, padx = 5, pady = 10, sticky = "W")
city_entry.bind("<Return>", lambda event: on_submit())

# Create the submit button
submit_button = ctk.CTkButton(root, text = "Submit",font = ("Arial", 16), command = on_submit)
submit_button.grid(row = 0, column = 2, padx = 10, pady = 30, sticky = "W")

# Create the text widget
text_widget = ctk.CTkTextbox(root, height = 470, width = 450, font = ("Courier", 12.5), wrap = "word", padx = 10, pady = 10)
text_widget.grid(row = 1, column = 0, columnspan = 3, padx = 20, pady = 20, sticky = "NSEW")
text_widget.configure(state = "disabled")

# Center the window
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width - 500) // 2
y = (screen_height - 370) // 2
root.geometry(f"500x370+{x}+{y}")


# Initialize the data
fetch_stations()
fetch_cities()
clear_terminal()

# Run the app
root.mainloop()