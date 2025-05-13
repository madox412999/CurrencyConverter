import tkinter as tk
from tkinter import ttk
import requests
from PIL import Image, ImageTk
import io
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from tkinter import messagebox
import customtkinter as ctk

currency_to_country = {
    "AED": "ae", "AFN": "af", "ALL": "al", "AMD": "am", "ANG": "an", "AOA": "ao", "ARS": "ar", "AUD": "au",
    "AWG": "aw", "AZN": "az", "BAM": "ba", "BBD": "bb", "BDT": "bd", "BGN": "bg", "BHD": "bh", "BIF": "bi",
    "BMD": "bm", "BND": "bn", "BOB": "bo", "BRL": "br", "BSD": "bs", "BTN": "bt", "BWP": "bw", "BYN": "by",
    "BZD": "bz", "CAD": "ca", "CDF": "cd", "CHF": "ch", "CLP": "cl", "CNY": "cn", "COP": "co", "CRC": "cr",
    "CUP": "cu", "CVE": "cv", "CZK": "cz", "DJF": "dj", "DKK": "dk", "DOP": "do", "DZD": "dz", "EGP": "eg",
    "ERN": "er", "ETB": "et", "EUR": "eu", "FJD": "fj", "FKP": "fk", "FOK": "fo", "GBP": "gb", "GEL": "ge",
    "GGP": "gg", "GHS": "gh", "GIP": "gi", "GMD": "gm", "GNF": "gn", "GTQ": "gt", "GYD": "gy", "HKD": "hk",
    "HNL": "hn", "HRK": "hr", "HTG": "ht", "HUF": "hu", "IDR": "id", "ILS": "il", "IMP": "im", "INR": "in",
    "IQD": "iq", "IRR": "ir", "ISK": "is", "JEP": "je", "JMD": "jm", "JOD": "jo", "JPY": "jp", "KES": "ke",
    "KGS": "kg", "KHR": "kh", "KID": "ki", "KMF": "km", "KRW": "kr", "KWD": "kw", "KYD": "ky", "KZT": "kz",
    "LAK": "la", "LBP": "lb", "LKR": "lk", "LRD": "lr", "LSL": "ls", "LYD": "ly", "MAD": "ma", "MDL": "md",
    "MGA": "mg", "MKD": "mk", "MMK": "mm", "MNT": "mn", "MOP": "mo", "MRU": "mr", "MUR": "mu", "MVR": "mv",
    "MWK": "mw", "MXN": "mx", "MYR": "my", "MZN": "mz", "NAD": "na", "NGN": "ng", "NIO": "ni", "NOK": "no",
    "NPR": "np", "NZD": "nz", "OMR": "om", "PAB": "pa", "PEN": "pe", "PGK": "pg", "PHP": "ph", "PKR": "pk",
    "PLN": "pl", "PYG": "py", "QAR": "qa", "RON": "ro", "RSD": "rs", "RUB": "ru", "RWF": "rw", "SAR": "sa",
    "SBD": "sb", "SCR": "sc", "SDG": "sd", "SEK": "se", "SGD": "sg", "SHP": "sh", "SLE": "sl", "SLL": "sl",
    "SOS": "so", "SRD": "sr", "SSP": "ss", "STN": "st", "SYP": "sy", "SZL": "sz", "THB": "th", "TJS": "tj",
    "TMT": "tm", "TND": "tn", "TOP": "to", "TRY": "tr", "TTD": "tt", "TVD": "tv", "TWD": "tw", "TZS": "tz",
    "UAH": "ua", "UGX": "ug", "USD": "us", "UYU": "uy", "UZS": "uz", "VES": "ve", "VND": "vn", "VUV": "vu",
    "WST": "ws", "XAF": "cm", "XCD": "ag", "XOF": "sn", "XPF": "pf", "YER": "ye", "ZAR": "za", "ZMW": "zm",
    "ZWL": "zw"
}

def get_flag_image(currency_code):
    country_code = currency_to_country.get(currency_code.upper())
    if not country_code:
        return None
    url = f"https://flagcdn.com/w40/{country_code}.png"
    try:
        response = requests.get(url)
        img_data = response.content
        image = Image.open(io.BytesIO(img_data)).resize((32, 24))
        return ImageTk.PhotoImage(image)
    except:
        return None

def get_currency_list():
    try:
        response = requests.get("https://open.er-api.com/v6/latest/USD")
        data = response.json()
        return list(data["rates"].keys())
    except:
        return ["USD", "EUR"]

def convert_currency():
    try:
        amount_str = entry_amount.get()
        if not amount_str.strip():
            label_result_field.config(text="Enter amount")
            return
        amount = float(amount_str)
        if amount <= 0:
            label_result_field.config(text="Invalid amount")
            return

        from_currency = combo_from.get()
        to_currency = combo_to.get()

        window.config(cursor="watch")
        window.update()

        url = f"https://open.er-api.com/v6/latest/{from_currency}"
        response = requests.get(url)
        data = response.json()
        rate = data["rates"][to_currency]
        result = amount * rate
        label_result_field.config(text=f"{result:.2f}")

    except Exception as e:
        print("Conversion error:", e)
        label_result_field.config(text="")
    finally:
        window.config(cursor="")
        window.update()

def show_exchange_chart():
    from_currency = combo_from.get()
    to_currency = combo_to.get()

    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=7)

    url = (
        f"https://api.frankfurter.app/{start_date.strftime('%Y-%m-%d')}..{end_date.strftime('%Y-%m-%d')}"
        f"?from={from_currency}&to={to_currency}"
    )

    try:
        response = requests.get(url)
        data = response.json()
        print("DEBUG chart:", data)

        if "rates" not in data or not data["rates"]:
            raise Exception("No data returned from the API.")

        dates = []
        rates = []

        for date in sorted(data["rates"].keys()):
            rate = data["rates"][date].get(to_currency)
            if rate is not None:
                dates.append(date)
                rates.append(rate)

        if not rates:
            raise Exception("No valid rates to display.")

        plt.figure(figsize=(6, 4))
        plt.plot(dates, rates, marker='o', color='#2196F3')
        plt.title(f"{from_currency} to {to_currency} (Up to 7 Recent Business Days)")
        plt.xlabel("Date")
        plt.ylabel(f"1 {from_currency} in {to_currency}")
        plt.grid(True)
        plt.tight_layout()
        plt.show()

    except Exception as e:
        print("Chart error:", e)
        tk.messagebox.showerror("Chart Error", "Could not load the chart.\nMake sure both currencies are supported.")

def update_flags(*args):
    flag1 = get_flag_image(combo_from.get())
    label_flag_from.configure(image=flag1)
    label_flag_from.image = flag1

    flag2 = get_flag_image(combo_to.get())
    label_flag_to.configure(image=flag2)
    label_flag_to.image = flag2

currency_list = get_currency_list()
currency_list.sort()

window = tk.Tk()
window.title("Currency Converter 💱")
window.geometry("525x345")
window.update_idletasks()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
window_width = 525
window_height = 345

x = (screen_width // 2) - (window_width // 2)
y = (screen_height // 2) - (window_height // 2)

window.geometry(f"{window_width}x{window_height}+{x}+{y}")

window.configure(bg="#ECEFF1")

dark_mode = tk.BooleanVar()

top_bar = tk.Frame(window, bg="#ECEFF1")
top_bar.pack(fill="x", padx=0, pady=0)

title = tk.Label(window, text="Currency Converter", font=("Helvetica", 18, "bold"), bg="#ECEFF1", fg="#333333")
title.pack(pady=12)

main_frame = tk.Frame(window, bg="#ECEFF1")
main_frame.pack(pady=5)

label_from = tk.Label(main_frame, text="From:", font=("Helvetica", 12), bg="#ECEFF1", fg="#333333")
label_from.grid(row=0, column=0, padx=5, sticky="e")

entry_amount = tk.Entry(main_frame, font=("Helvetica", 12), width=10, bg="white", relief="solid", bd=1)
entry_amount.grid(row=0, column=1, padx=5)

combo_from = ttk.Combobox(main_frame, values=currency_list, font=("Helvetica", 12), state="readonly", width=8)
combo_from.set("USD")
combo_from.grid(row=0, column=2, padx=5)

flag_from = get_flag_image(combo_from.get())
label_flag_from = tk.Label(main_frame, image=flag_from, bg="#ECEFF1")
label_flag_from.image = flag_from
label_flag_from.grid(row=0, column=3, padx=5)

spacer = tk.Label(main_frame, text="", bg="#ECEFF1")
spacer.grid(row=1, column=0, pady=5)

label_to = tk.Label(main_frame, text="To:", font=("Helvetica", 12), bg="#ECEFF1", fg="#333333")
label_to.grid(row=2, column=0, padx=5, sticky="e")

label_result_field = tk.Label(main_frame, text="", font=("Helvetica", 12), width=10,
                              bg="white", relief="solid", bd=1, anchor="w")
label_result_field.grid(row=2, column=1, padx=5)

combo_to = ttk.Combobox(main_frame, values=currency_list, font=("Helvetica", 12), state="readonly", width=8)
combo_to.set("EUR")
combo_to.grid(row=2, column=2, padx=5)

flag_to = get_flag_image(combo_to.get())
label_flag_to = tk.Label(main_frame, image=flag_to, bg="#ECEFF1")
label_flag_to.image = flag_to
label_flag_to.grid(row=2, column=3, padx=5)

btn_swap = tk.Button(main_frame, text="⇄ Swap", command=lambda: [swap_currencies(), update_flags()],
                     bg="#1976D2", fg="white", font=("Helvetica", 10), padx=6, pady=3)
btn_swap.grid(row=0, column=4, rowspan=3, padx=10)

btn_convert = ctk.CTkButton(
    window,
    text="Convert",
    command=lambda: [convert_currency(), update_flags()],
    fg_color="#388E3C",
    hover_color="#2E7D32",
    text_color="white",
    font=("Helvetica", 12),
    corner_radius=5
)
btn_convert.pack(pady=15)

left_controls = tk.Frame(top_bar, bg="#ECEFF1")
left_controls.pack(side="left", anchor="nw", padx=(10, 0), pady=(5, 0))

btn_chart = ctk.CTkButton(
    left_controls,
    text="  📊  Show Last 7 Trading Days Chart    ",
    command=show_exchange_chart,
    font=(" ",12,"bold"),
    fg_color="#CFD8DC",
    text_color="#37474F",
    corner_radius=6,
    hover_color="#B0BEC5",
    cursor="hand2"
)
btn_chart.pack(anchor="w")

supported_label = tk.Label(left_controls, text="Chart available for major currencies (e.g. EUR, USD, GBP, JPY, ILS, etc.)",
                           font=("Helvetica", 8), bg="#ECEFF1", fg="#555555")
supported_label.pack(anchor="w", pady=(2, 0))

combo_from.bind("<<ComboboxSelected>>", update_flags)
combo_to.bind("<<ComboboxSelected>>", update_flags)

def swap_currencies():
    from_cur = combo_from.get()
    to_cur = combo_to.get()
    combo_from.set(to_cur)
    combo_to.set(from_cur)

def toggle_dark_mode():
    if dark_mode.get():
        window.configure(bg="#1E1E1E")
        main_frame.configure(bg="#1E1E1E")
        top_bar.configure(bg="#1E1E1E")
        left_controls.configure(bg="#1E1E1E")
        toggle.configure(bg="#1E1E1E", fg="white", selectcolor="#1E1E1E")

        title.config(bg="#1E1E1E", fg="#FFFFFF")
        label_from.config(bg="#1E1E1E", fg="#FFFFFF")
        label_to.config(bg="#1E1E1E", fg="#FFFFFF")
        spacer.config(bg="#1E1E1E")
        label_result_field.config(bg="#2C2C2C", fg="#FFFFFF")
        entry_amount.config(bg="#2C2C2C", fg="#FFFFFF", insertbackground="white")
        label_flag_from.config(bg="#1E1E1E")
        label_flag_to.config(bg="#1E1E1E")

        btn_swap.config(bg="#2196F3", fg="white")
        btn_convert.configure(fg_color="#4CAF50", hover_color="#388E3C", text_color="white")

        btn_chart.configure(
            fg_color="#37474F",
            text_color="white",
            hover_color="#263238"
        )
        supported_label.configure(bg="#1E1E1E", fg="#BBBBBB")

    else:
        window.configure(bg="#ECEFF1")
        main_frame.configure(bg="#ECEFF1")
        top_bar.configure(bg="#ECEFF1")
        left_controls.configure(bg="#ECEFF1")
        toggle.configure(bg="#ECEFF1", fg="#333333", selectcolor="#ECEFF1")

        title.config(bg="#ECEFF1", fg="#333333")
        label_from.config(bg="#ECEFF1", fg="#333333")
        label_to.config(bg="#ECEFF1", fg="#333333")
        spacer.config(bg="#ECEFF1")
        label_result_field.config(bg="white", fg="black")
        entry_amount.config(bg="white", fg="black", insertbackground="black")
        label_flag_from.config(bg="#ECEFF1")
        label_flag_to.config(bg="#ECEFF1")

        btn_swap.config(bg="#1976D2", fg="white")
        btn_convert.configure(fg_color="#388E3C", hover_color="#2E7D32", text_color="white")

        btn_chart.configure(
            fg_color="#CFD8DC",
            text_color="#37474F",
            hover_color="#B0BEC5"
        )
        supported_label.configure(bg="#ECEFF1", fg="#555555")

toggle = tk.Checkbutton(top_bar, text="Dark Mode", variable=dark_mode, command=toggle_dark_mode,
                        bg="#ECEFF1", fg="#000000", font=("Helvetica", 10), anchor="e", selectcolor="#ECEFF1")
toggle.pack(side="right")

window.mainloop()
