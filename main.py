import tkinter as tk
from tkinter import ttk, messagebox
import requests
import datetime
import json

class CurrencyConverter:
    def __init__(self):
        self.url = 'https://api.exchangerate-api.com/v4/latest/USD'
        self.currencies = self.get_currencies()

    def get_currencies(self):
        try:
            response = requests.get(self.url)
            data = response.json()
            return data['rates']
        except Exception as e:
            self.log_error(f"Error fetching currencies: {e}")
            return {}

    def convert(self, from_currency, to_currency, amount):
        if from_currency != 'USD':
            amount = amount / self.currencies[from_currency]
        amount = round(amount * self.currencies[to_currency], 2)
        return amount

    def get_historical_rate(self, date, from_currency, to_currency):
        url = f'https://api.exchangerate-api.com/v4/{date}/USD'
        try:
            response = requests.get(url)
            data = response.json()
            rate = data['rates'][to_currency] / data['rates'][from_currency]
            return round(rate, 4)
        except Exception as e:
            self.log_error(f"Error fetching historical rates: {e}")
            return None

    def log_error(self, message):
        with open('error_log.txt', 'a') as f:
            f.write(f"{datetime.datetime.now()}: {message}\n")

class CurrencyConverterApp:
    def __init__(self, root):
        self.converter = CurrencyConverter()
        self.root = root
        self.root.title("Currency Converter")
        self.root.geometry("500x400")
        self.theme = tk.StringVar(value="Light")
        self.favorites = []
        self.load_favorites()
        self.create_widgets()

    def create_widgets(self):
        # Theme Selection
        theme_label = tk.Label(self.root, text="Select Theme:")
        theme_label.pack(pady=5)
        
        theme_menu = ttk.Combobox(self.root, textvariable=self.theme, values=["Light", "Dark"])
        theme_menu.pack(pady=5)
        theme_menu.bind("<<ComboboxSelected>>", self.change_theme)

        # Amount Entry
        self.amount_label = tk.Label(self.root, text="Amount:")
        self.amount_label.pack(pady=10)
        
        self.amount_entry = tk.Entry(self.root)
        self.amount_entry.pack(pady=10)

        # From Currency
        self.from_currency_label = tk.Label(self.root, text="From Currency:")
        self.from_currency_label.pack(pady=10)

        self.from_currency = ttk.Combobox(self.root, values=list(self.converter.currencies.keys()))
        self.from_currency.set("USD")
        self.from_currency.pack(pady=10)

        # To Currency
        self.to_currency_label = tk.Label(self.root, text="To Currency:")
        self.to_currency_label.pack(pady=10)

        self.to_currency = ttk.Combobox(self.root, values=list(self.converter.currencies.keys()))
        self.to_currency.set("INR")
        self.to_currency.pack(pady=10)

        # Convert Button
        self.convert_button = tk.Button(self.root, text="Convert", command=self.convert_currency)
        self.convert_button.pack(pady=20)

        # Favorite Button
        self.favorite_button = tk.Button(self.root, text="Save as Favorite", command=self.save_favorite)
        self.favorite_button.pack(pady=10)

        # View Favorites Button
        self.view_favorites_button = tk.Button(self.root, text="View Favorites", command=self.view_favorites)
        self.view_favorites_button.pack(pady=10)

        # Result Label
        self.result_label = tk.Label(self.root, text="")
        self.result_label.pack(pady=10)

        # Historical Rates Button
        self.historical_button = tk.Button(self.root, text="Get Historical Rate", command=self.get_historical_rate)
        self.historical_button.pack(pady=10)

    def convert_currency(self):
        try:
            amount = float(self.amount_entry.get())
            from_curr = self.from_currency.get()
            to_curr = self.to_currency.get()

            if from_curr not in self.converter.currencies or to_curr not in self.converter.currencies:
                raise ValueError("Invalid currency")

            converted_amount = self.converter.convert(from_curr, to_curr, amount)
            self.result_label.config(text=f"{amount} {from_curr} = {converted_amount} {to_curr}")
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter a valid amount and select valid currencies.")
            self.converter.log_error("Invalid input in conversion.")

    def save_favorite(self):
        from_curr = self.from_currency.get()
        to_curr = self.to_currency.get()
        if from_curr and to_curr:
            self.favorites.append((from_curr, to_curr))
            self.save_favorites()
            messagebox.showinfo("Saved", f"Favorite conversion {from_curr} to {to_curr} saved!")
        else:
            messagebox.showerror("Error", "Please select both currencies.")

    def view_favorites(self):
        favorites_str = "\n".join([f"{f[0]} to {f[1]}" for f in self.favorites])
        messagebox.showinfo("Favorites", favorites_str if favorites_str else "No favorites saved.")

    def save_favorites(self):
        with open('favorites.json', 'w') as f:
            json.dump(self.favorites, f)

    def load_favorites(self):
        try:
            with open('favorites.json', 'r') as f:
                self.favorites = json.load(f)
        except FileNotFoundError:
            self.favorites = []

    def change_theme(self, event=None):
        theme = self.theme.get()
        if theme == "Dark":
            self.root.config(bg="black")
            for widget in self.root.winfo_children():
                widget.config(bg="black", fg="white")
        else:
            self.root.config(bg="white")
            for widget in self.root.winfo_children():
                widget.config(bg="white", fg="black")

    def get_historical_rate(self):
        from_curr = self.from_currency.get()
        to_curr = self.to_currency.get()
        date = tk.simpledialog.askstring("Input", "Enter date (YYYY-MM-DD):")
        if from_curr and to_curr and date:
            rate = self.converter.get_historical_rate(date, from_curr, to_curr)
            if rate:
                self.result_label.config(text=f"Historical rate on {date}: 1 {from_curr} = {rate} {to_curr}")
            else:
                messagebox.showerror("Error", "Could not fetch historical rate.")

def main():
    root = tk.Tk()
    app = CurrencyConverterApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
