# Pizza Builder app - users guide

### Adataim:
név: Biró Dávid
neptun: tuxolp


## Alkalmazás rövid leírása:

Egy egyszerű grafikus felülettel rendelkező pizza rendelő alkalmazás, amely lehetővé teszi pizzák összeállítását, árkalkulációt és a rendelések mentését.

## Alkalmazott modul:

`customtkinter`:
A CustomTkinter egy modern, testreszabható Python GUI könyvtár, amely a beépített Tkinter könyvtárra épül, de sokkal szebb és korszerűbb kinézettel.


### 1. Környezet létrehozása:
Létrehozzuk a .venv virtuális környezetet

```bash
python3 -m venv .venv
```
Aktiváljuk a .venv-et:

```bash
source .venv/bin/activate
```
most már a saját fájlrendszerünktől elkülönitve tudjuk telepíteni a függőségeket

### 2. Függőségek telepítése
Telepítjük a szükséges Python könyvtárat:

```bash
pip3 install customtkinter
```

### 3. alkalmazás indítása a .venvben:

```bash
python3 main.py
```

### Felhasználói útmutató

1. **Méret kiválasztása**: Válasszunk a három méret közül (Kicsi, Közepes, Nagy)

2. **Feltétek hozzáadása**: Pipáljuk be a kívánt feltéteket:
   - Sajt: 300 Ft
   - Sonka: 450 Ft
   - Kukorica: 250 Ft
   - Csípős szósz: 200 Ft

3. **Ár kiszámítása**: Kattintsunk az "Ár kiszámítása" gombra
   - Az összeg azonnal megjelenik

4. **Pizza mentése**: Kattintsunk a "Mentés listába" gombra
   - A pizza megjelenik a lista alján
   - Automatikusan elmenti a `data/orders.json` fájlba

5. **Rendelési történet**: Megtekinthetjük a listában az összes mentett pizzát 

## main.py - A belépési pont

```python
from app import App 
if __name__ == "__main__":
    app = App()
    app.mainloop()
```

Ez a program indítófájlja. Importálja az `App` osztályt, létrehoz egy példányt belőle, majd elindítja a grafikus felületet a `mainloop()` metódussal.

---

## bd_tools.py - Árkalkulációs modul

### Alapárak szótára
```python
BASE_PRICES = {
    "Kicsi": 2000,
    "Közepes": 2600,
    "Nagy": 3200
}
```
Tárolja a pizza méretenkénti alapárait forintban.

### Feltétek árai
```python
TOPPING_PRICES = {
    "Sajt": 300,
    "Sonka": 450,
    "Kukorica": 250,
    "Csípős szósz": 200
}
```
Minden feltét külön díja.

### Árkalkuláció függvény
```python
def calculateBDPrice(size, toppings):
    base = BASE_PRICES.get(size, BASE_PRICES["Közepes"])
    extra = sum(TOPPING_PRICES[t] for t in toppings)
    return base + extra
```

- Kikeresi a méret alapárát
- Összeadja a kiválasztott feltétek árait
- Visszaadja a teljes árat

---

## bd_pizza_card.py - Pizza kártya widget

### Egyedi widget létrehozása
```python
class BDPizzaCard(ctk.CTkFrame):
    def __init__(self, master, size, toppings, price):
        super().__init__(master)
```
Egy keretben (`CTkFrame`) megjelenít egy elmentett pizza rendelést.

### Szöveg formázás
```python
toppings_text = ", ".join(toppings) if toppings else "Nincs feltét"
text = f"Méret: {size} | Feltétek: {toppings_text} | Ár: {price} Ft"
```

- Összefűzi a feltéteket vesszővel
- Formázott szöveget készít a pizza adataiból

### Megjelenítés
```python
self.label = ctk.CTkLabel(self, text=text, anchor="w", justify="left")
self.label.pack(padx=10, pady=5, fill="x")
```

- Címkét (`Label`) hoz létre a szöveggel
- Balra igazítva jeleníti meg

---

## app.py - Fő alkalmazás logika

### Inicializálás

```python
class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("App")
        self.geometry("600x600")
```

- Az `App` osztály a főablak (`CTk` az alap osztály)
- Beállítja a címet és a méretet (600x600 pixel)

### Változók létrehozása
```python
self.size_var = ctk.StringVar(value="Közepes")
self.topping_vars = {
    "Sajt": ctk.BooleanVar(value=True),
    "Sonka": ctk.BooleanVar(value=False),
    ...
}
```

- **size_var:** Változó a méret tárolására (alapértelmezett: Közepes)
- **topping_vars:** Szótár a feltétek állapotához (ki/be kapcsolva)

---

### Felület felépítése

#### Méretválasztó keret
```python
size_frame = ctk.CTkFrame(self)
size_frame.pack(pady=10, fill="x")
```
Létrehoz egy keretet a méretválasztáshoz és elhelyezi.

#### Radio buttonok (méretválasztás)
```python
for size in ["Kicsi", "Közepes", "Nagy"]:
    rb = ctk.CTkRadioButton(
        size_frame,
        text=size,
        variable=self.size_var,
        value=size
    )
    rb.pack(anchor="w", padx=20)
```

**Radio buttonok:** Három opciógombot hoz létre a méretekhez. Mindegyik ugyanahhoz a `size_var` változóhoz kapcsolódik, így csak egyet lehet kiválasztani.

#### Checkboxok (feltétválasztás)
```python
for topping, var in self.topping_vars.items():
    cb = ctk.CTkCheckBox(
        toppings_frame,
        text=topping,
        variable=var
    )
    cb.pack(anchor="w", padx=20)
```

**Checkboxok:** Minden feltéthez egy pipálható négyzetet hoz létre. Több feltét is választható egyszerre.

---

### Funkciók

#### Kiválasztott feltétek lekérdezése
```python
def get_selected_toppings(self):
    return [name for name, var in self.topping_vars.items() if var.get()]
```

Lista comprehension-nel összegyűjti azokat a feltéteket, ahol a checkbox be van pipálva.

#### Ár kiszámítása
```python
def calculate_pizza(self):
    size = self.size_var.get()
    toppings = self.get_selected_toppings()
    price = calculateBDPrice(size, toppings)
    self.current_price = price
    self.result_label.configure(text=f"Összeg: {price} Ft")
```

Lekéri a méretet és feltéteket, kiszámítja az árat, és megjeleníti a címkén.

#### Pizza mentése
```python
def save_pizza(self):
    if self.current_price is None:
        self.calculate_pizza()
    ...
    order = {
        "size": size,
        "toppings": toppings,
        "price": price
    }
    self.orders.append(order)
```

- Ha nincs kiszámítva az ár, előbb kiszámítja
- Létrehoz egy rendelés szótárat
- Hozzáadja a rendelések listájához

#### Kártya létrehozása
```python
card = BDPizzaCard(self.history_frame, size, toppings, price)
card.pack(fill="x", padx=5, pady=3)
```

Létrehoz egy pizza kártyát a scrollozható keretben.

#### JSON mentés
```python
with open("data/orders.json", "w", encoding="utf-8") as f:
    json.dump(self.orders, f, indent=2, ensure_ascii=False)
```

Elmenti az összes rendelést egy JSON fájlba, szépen formázva és magyar karakterekkel.

---

## Működési folyamat

1. **Indítás:** `main.py` elindítja az alkalmazást
2. **Felület betöltése:** `app.py` létrehozza az ablakot és a widgeteket
3. **Felhasználói interakció:**
   - Méret kiválasztása radio buttonokkal
   - Feltétek kiválasztása checkboxokkal
4. **Árkalkuláció:** `bd_tools.py` kiszámítja az árat
5. **Mentés:** A rendelés elmenti JSON-ba és megjelenik a listában
6. **Megjelenítés:** `bd_pizza_card.py` megjeleníti a mentett pizzát

---
