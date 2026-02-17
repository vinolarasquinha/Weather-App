"""
Desktop Weather App - Python + Tkinter
Run using: python main.py
"""

import tkinter as tk
from tkinter import messagebox
from weather_service import get_weather


class WeatherApp:
    BG_COLOR = "#f0f4f8"
    TEXT_COLOR = "#2d3748"
    SUBTEXT_COLOR = "#4a5568"
    BUTTON_COLOR = "#4299e1"
    BUTTON_HOVER = "#3182ce"

    def __init__(self, root):
        self.root = root
        self.root.title("Weather App")
        self.root.geometry("420x350")
        self.root.resizable(False, False)
        self.root.configure(bg=self.BG_COLOR)
        self._build_ui()

    def _build_ui(self):
        bg = self.BG_COLOR

        title_label = tk.Label(
            self.root,
            text="☁ Weather Checker",
            font=("Arial", 18, "bold"),
            bg=bg,
            fg=self.TEXT_COLOR,
        )
        title_label.pack(pady=(20, 5))

        input_label = tk.Label(
            self.root,
            text="Enter a city name:",
            font=("Arial", 11),
            bg=bg,
            fg=self.SUBTEXT_COLOR,
        )
        input_label.pack(pady=(10, 2))

        self.city_entry = tk.Entry(
            self.root,
            width=28,
            font=("Arial", 12),
            relief="solid",
            bd=1,
        )
        self.city_entry.pack(pady=5, ipady=4)
        self.city_entry.focus_set()
        self.city_entry.bind("<Return>", lambda event: self._on_search())

        self.search_btn = tk.Button(
            self.root,
            text="Get Weather",
            font=("Arial", 11, "bold"),
            bg=self.BUTTON_COLOR,
            fg="white",
            activebackground=self.BUTTON_HOVER,
            activeforeground="white",
            relief="flat",
            padx=16,
            pady=4,
            cursor="hand2",
            command=self._on_search,
        )
        self.search_btn.pack(pady=10)

        self.result_var = tk.StringVar(value="")
        result_label = tk.Label(
            self.root,
            textvariable=self.result_var,
            font=("Consolas", 11),
            bg=bg,
            fg=self.TEXT_COLOR,
            justify="left",
            wraplength=380,
        )
        result_label.pack(pady=10)

    def _on_search(self):
        city = self.city_entry.get().strip()

        if not city:
            messagebox.showwarning("Input Error", "Please enter a city name.")
            return

        self.result_var.set("Fetching weather...")
        self.search_btn.config(state="disabled")
        self.root.update_idletasks()

        data = get_weather(city)

        self.search_btn.config(state="normal")

        if "error" in data:
            self.result_var.set(f"Error: {data['error']}")
        else:
            self.result_var.set(
                f"City       : {data['city']}, {data['country']}\n"
                f"Temperature: {data['temperature']} °C\n"
                f"Wind Speed : {data['windspeed']} km/h\n"
                f"Condition  : {data['condition']}"
            )


def main():
    root = tk.Tk()
    WeatherApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
