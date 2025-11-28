BASE_PRICES = {
    "Kicsi": 2000,
    "Közepes": 2600,
    "Nagy": 3200
}

TOPPING_PRICES = {
    "Sajt": 300,
    "Sonka": 450,
    "Kukorica": 250,
    "Csípős szósz": 200
}

def calculateBDPrice(size, toppings):
    base = BASE_PRICES.get(size, BASE_PRICES["Közepes"])
    extra = sum(TOPPING_PRICES[t] for t in toppings)
    return base + extra
