import customtkinter as ctk
import json
from widgets.bd_pizza_card import BDPizzaCard
from bd_tools import calculateBDPrice

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("App")
        self.geometry("600x600")

        self.size_var = ctk.StringVar(value="Közepes")
        self.topping_vars = {
            "Sajt": ctk.BooleanVar(value=True),
            "Sonka": ctk.BooleanVar(value=False),
            "Kukorica": ctk.BooleanVar(value=False),
            "Csípős szósz": ctk.BooleanVar(value=False)
        }

        title_label = ctk.CTkLabel(self, text="pizza builder", font=("Arial", 20))
        title_label.pack(pady=10)

        size_frame = ctk.CTkFrame(self)
        size_frame.pack(pady=10, fill="x")

        size_title = ctk.CTkLabel(size_frame, text="Válassz méretet:")
        size_title.pack(anchor="w", padx=10, pady=5)

        for size in ["Kicsi", "Közepes", "Nagy"]:
            rb = ctk.CTkRadioButton(
                size_frame,
                text=size,
                variable=self.size_var,
                value=size
            )
            rb.pack(anchor="w", padx=20)

        toppings_frame = ctk.CTkFrame(self)
        toppings_frame.pack(pady=10, fill="x")

        toppings_title = ctk.CTkLabel(toppings_frame, text="Válaszd ki a feltéteket:")
        toppings_title.pack(anchor="w", padx=10, pady=5)

        for topping, var in self.topping_vars.items():
            cb = ctk.CTkCheckBox(
                toppings_frame,
                text=topping,
                variable=var
            )
            cb.pack(anchor="w", padx=20)

        button_frame = ctk.CTkFrame(self)
        button_frame.pack(pady=10)

        self.result_label = ctk.CTkLabel(button_frame, text="Összeg: - Ft")
        self.result_label.pack(side="left", padx=10)

        calc_button = ctk.CTkButton(button_frame, text="Ár kiszámítása", command=self.calculate_pizza)
        calc_button.pack(side="left", padx=10)

        save_button = ctk.CTkButton(button_frame, text="Mentés listába", command=self.save_pizza)
        save_button.pack(side="left", padx=10)

        self.history_frame = ctk.CTkScrollableFrame(self, label_text="Összeállított pizzák")
        self.history_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.orders = []
        self.current_price = None

    def get_selected_toppings(self):
        return [name for name, var in self.topping_vars.items() if var.get()]

    def calculate_pizza(self):
        size = self.size_var.get()
        toppings = self.get_selected_toppings()
        price = calculateBDPrice(size, toppings)
        self.current_price = price
        self.result_label.configure(text=f"Összeg: {price} Ft")

    def save_pizza(self):
        if self.current_price is None:
            self.calculate_pizza()
        size = self.size_var.get()
        toppings = self.get_selected_toppings()
        price = self.current_price

        order = {
            "size": size,
            "toppings": toppings,
            "price": price
        }
        self.orders.append(order)

        card = BDPizzaCard(self.history_frame, size, toppings, price)
        card.pack(fill="x", padx=5, pady=3)

        with open("data/orders.json", "w", encoding="utf-8") as f:
            json.dump(self.orders, f, indent=2, ensure_ascii=False)
