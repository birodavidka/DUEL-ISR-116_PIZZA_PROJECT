import customtkinter as ctk

class BDPizzaCard(ctk.CTkFrame):
    def __init__(self, master, size, toppings, price):
        super().__init__(master)
        toppings_text = ", ".join(toppings) if toppings else "Nincs feltét"
        text = f"Méret: {size} | Feltétek: {toppings_text} | Ár: {price} Ft"
        self.label = ctk.CTkLabel(self, text=text, anchor="w", justify="left")
        self.label.pack(padx=10, pady=5, fill="x")
