import tkinter as tk
from tkinter import ttk, messagebox
import requests

class CurrencyConverter:
    def __init__(self):
        self.url = 'https://api.exchangerate-api.com/v4/latest/USD'
        self.currencies = self.get_currencies()

    def get_currencies(self):
        response = requests.get(self.url)
        data = response.json()
        return data['rates']

    def convert(self, from_currency, to_currency, amount):
        if from_currency != 'USD':
            amount = amount / self.currencies[from_currency]
        amount = round(amount * self.currencies[to_currency], 2)
        return amount

class CurrencyConverterApp:
    def __init__(self, root):
        self.converter = CurrencyConverter()
        self.root = root
        self.root.title("Currency Converter")
        self.root.geometry("400x300")
        self.create_widgets()

    def create_widgets(self):
        self.amount_label = tk.Label(self.root, text="Amount:")
        self.amount_label.pack(pady=10)
        
        self.amount_entry = tk.Entry(self.root)
        self.amount_entry.pack(pady=10)

        self.from_currency_label = tk.Label(self.root, text="From Currency:")
        self.from_currency_label.pack(pady=10)

        self.from_currency = ttk.Combobox(self.root, values=list(self.converter.currencies.keys()))
        self.from_currency.set("USD")
        self.from_currency.pack(pady=10)

        self.to_currency_label = tk.Label(self.root, text="To Currency:")
        self.to_currency_label.pack(pady=10)

        self.to_currency = ttk.Combobox(self.root, values=list(self.converter.currencies.keys()))
        self.to_currency.set("INR")
        self.to_currency.pack(pady=10)

        self.convert_button = tk.Button(self.root, text="Convert", command=self.convert_currency)
        self.convert_button.pack(pady=20)

        self.result_label = tk.Label(self.root, text="")
        self.result_label.pack(pady=10)

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

def main():
    root = tk.Tk()
    app = CurrencyConverterApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
