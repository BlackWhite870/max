import tkinter as tk
from tkinter import messagebox
from weather_api import get_weather
from db import save_weather_to_db

API_KEY = "4efc62592ed42d49e71229ad7cc4c032"

def show_weather():
    city = entry.get()
    if not city:
        messagebox.showwarning("Внимание", "Введите название города")
        return

    try:
        weather = get_weather(city, API_KEY)
        result = f"Погода в {weather['city']}:\n{weather['temperature']}°C, {weather['description']}"
        output_label.config(text=result)

        save_weather_to_db(weather['city'], weather['temperature'], weather['description'])

    except ValueError as e:
        output_label.config(text="")
        messagebox.showerror("Ошибка", str(e))


root = tk.Tk()
root.title("Погода")
root.geometry("600x500")
root.resizable(False, False)

label = tk.Label(root, text="Введите город:")
label.pack(pady=10)

entry = tk.Entry(root, width=50)
entry.pack()

btn = tk.Button(root, text="Узнать погоду", command=show_weather)
btn.pack(pady=10)

output_label = tk.Label(root, text="", font=("Arial", 12))
output_label.pack(pady=10)

root.mainloop()