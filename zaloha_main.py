from tkinter import *
from screeninfo import get_monitors
from settings import *
from api_ares import *

# --- Funkce ---

def hledej():
    """
    Spustí dotaz na API ARES na základě zadaného IČO.

    Validuje délku IČO, a pokud je platná, volá API,
    parsuje JSON odpověď a zobrazuje získané údaje v GUI.
    """
    # Vymaže předchozí výsledky zobrazené v labelech
    for (_, nazev) in labels:
        results[nazev]["text"] = ""
    text_error_label["text"] = ""

    # Kontrola, zda IČO má přesně 8 znaků
    if len(vstup.get()) != 8:
        # Pokud ne, zobrazí chybovou hlášku
        text_error_label["text"] = "Chyba: Zadejte přesně 8 číslic!"
        return  # Ukončí funkci, aby se dotaz neodeslal

    # Pokud je délka správná, vymaže hlášku a pokračuje
    text_error_label["text"] = ""

    try:
        api_ares = ApiAres(vstup.get())
        # Bezpečné získávání hodnot pomocí .get()
        results["ico"]["text"] = api_ares.data.get("ico", "N/A")
        results["dic"]["text"] = api_ares.data.get("dic", "N/A")
        results["jmeno"]["text"] = api_ares.data.get("obchodniJmeno", "N/A")

        # Zpracování vnořených slovníků
        sidlo_data = api_ares.data.get("sidlo", {})
        results["adresa"]["text"] = f"{sidlo_data.get("nazevUlice", "")} {sidlo_data.get("cisloDomovni", "")}/{sidlo_data.get("cisloOrientacni", "")}"
        results["adresa1"]["text"] = f"{sidlo_data.get("nazevObce", "")} - {sidlo_data.get("nazevCastiObce", "")}"
        results["psc"]["text"] = sidlo_data.get("psc", "N/A")
        results["stat"]["text"] = sidlo_data.get("nazevStatu", "N/A")
        results["kod_stat"]["text"] = sidlo_data.get("kodStatu", "N/A")
        results["zalozeno"]["text"] = api_ares.data.get("datumVzniku", "N/A")

        # Získání spisové značky z vnořené struktury a ošetření chyby indexu
        dalsi_udaje = api_ares.data.get("dalsiUdaje", [])
        spisova_znacka = "N/A"
        if len(dalsi_udaje) > 2:
            spisova_znacka = dalsi_udaje[2].get("spisovaZnacka", "N/A")
        results["spis_znacka"]["text"] = spisova_znacka
        results["cznace"]["text"] = api_ares.data.get("czNace", "N/A")
        results["aktualizace"]["text"] = api_ares.data.get("datumAktualizace", "N/A")

    except requests.exceptions.ConnectionError:
        # Konkrétní chyba pro problémy se sítí
        text_error_label["text"] = "Chyba připojení."
        text_error_label["fg"] = "orange"

    except requests.exceptions.HTTPError as e:
        # Zde zachytíme specifickou chybu 404
        if e.response.status_code == 404:
            text_error_label["text"] = "Zadané IČO nebylo nalezeno."
            text_error_label["fg"] = "orange"
        else:
            # Ošetření jiných chyb 4xx nebo 5xx
            text_error_label["text"] = f"Došlo k HTTP chybě: {e}"

# --- Validační funkce ---

def validate_input(new_text):
    """
    Validuje vstup, aby to byly pouze číslice a maximálně 8 znaků.

    Parametry:
    new_text (str): Nový text, který se pokouší uživatel zadat.

    Vrací:
    bool: True, pokud je vstup platný, jinak False.
    """
    # Povolí zadávání číslic a také prázdný řetězec (pro mazání)
    if new_text.isdigit() or new_text == "":
        if len(new_text) <= 8:
            return True
    return False

# --- Nastavení a inicializace GUI ---

# Získání rozměrů obrazovky pro vycentrování okna
monitor = get_monitors()[0]
screen_width = monitor.width
screen_height = monitor.height

# Vytvoření hlavního okna Tkinter
window = Tk()
x = (screen_width // 2) - (WIDTH // 2)
y = (screen_height // 2) - (HEIGHT // 2)
# Nastavení geometrie okna a jeho vlastností
window.geometry(f"{WIDTH}x{HEIGHT}+{x}+{y}")
window.title("Hledání subjektu podle IČO")
window.minsize(WIDTH, HEIGHT)
window.resizable(False, False)
window.iconbitmap("dog.ico")
window.config(bg=BACKGROUND_COLOR)

# --- Vytvoření framů pro uspořádání widgetů ---
nadpis_frame = Frame(window, bg=BACKGROUND_COLOR)
nadpis_frame.pack(fill="x")
nadpis_frame.columnconfigure(0, weight=1)  # sloupec se roztáhne

input_frame = Frame(window, bg=BACKGROUND_COLOR)
input_frame.pack(fill="x")
input_frame.columnconfigure(0, weight=1)

result_frame = Frame(window, bg=BACKGROUND_COLOR)
result_frame.pack(fill="x")
# Nastavení poměru roztažení sloupců pro popisky a výsledky
result_frame.columnconfigure(0, weight=0) # sloupec s popisky se neroztáhne
result_frame.columnconfigure(1, weight=1) # sloupec s výsledky se roztáhne

buton_frame = Frame(window, bg=BACKGROUND_COLOR)
buton_frame.pack(fill="x")
buton_frame.columnconfigure(0, weight=1) # sloupec s tlačítkem se roztáhne

# --- Vytvoření widgetů ---

# Label pro hlavní nadpis
text_okna = Label(nadpis_frame,
                  text="Zadejte IČO a klikněte na Hledej.",
                  bg=BACKGROUND_COLOR,
                  fg=TEXT_COLOR,
                  font=FONT_NADPIS
                  )
text_okna.grid(row=0, column=0, sticky="ew", pady=10)

# Registrace validační funkce pro vstupní pole
validate_command = window.register(validate_input)
# Vstupní pole pro zadání IČO s validací v reálném čase
vstup = Entry(input_frame,
              font=FONT_NADPIS,
              validate="key", # Spustí validaci při každém stisku klávesy
              validatecommand=(validate_command, '%P')) # %P je nový text, který by měl být ve vstupu
vstup.focus() # Nastaví kurzor do vstupního pole po spuštění
# vstup.insert(0, "28571533") # Pro testovací účely
vstup.grid(row=0, column=0, sticky="ew", pady=5, padx=10)

# Tlačítko pro spuštění hledání
tlacitko = Button(input_frame, text="Hledej", bg=BUTTON_COLOR, fg=TEXT_COLOR, command=hledej, width=25, font=FONT_BUTTONS)
tlacitko.grid(row=0, column=1, sticky="ew", pady=5, padx=10)

# Seznam popisků a jejich cílových klíčů pro výsledky
labels = [
    ("IČO:", "ico"),
    ("DIČ:", "dic"),
    ("Jméno:", "jmeno"),
    ("Adresa:", "adresa"),
    ("Adresa1:", "adresa1"),
    ("PSČ:", "psc"),
    ("Stát:", "stat"),
    ("Kód státu:", "kod_stat"),
    ("Vznik:", "zalozeno"),
    ("Spis. zn.:", "spis_znacka"),
    ("czNace:", "cznace"),
    ("Aktualizace:", "aktualizace"),
]

# Slovník pro uložení výsledných Label widgetů pro snadný přístup
results = {}

# Vytvoření Label widgetů pro popisky a výsledky v cyklu
for row, (text, key) in enumerate(labels):
    # Label pro popisek (např. "IČO:")
    lbl = Label(result_frame, text=text, bg=BACKGROUND_COLOR, fg=TEXT_COLOR, font=FONT_TEXT)
    lbl.grid(row=row, column=0, sticky="e", padx=10)

    # Label pro zobrazení výsledků
    results[key] = Label(result_frame, bg=BACKGROUND_COLOR, fg=TEXT_COLOR, font=FONT_TEXT)
    results[key].grid(row=row, column=1, sticky="w")

# Label pro zobrazení chybových hlášek
text_error_label = Label(result_frame, bg=BACKGROUND_COLOR, fg="red", font=FONT_NADPIS)
text_error_label.grid(row=5, column=1, sticky="w", padx=10)

# Spodní tlačítko pro ukončení aplikace
exit_buton = Button(buton_frame, text="EXIT", bg=BUTTON_COLOR, fg=TEXT_COLOR, width=25, command=window.destroy, font=FONT_BUTTONS)
exit_buton.grid(row=0, column=0, sticky="es", padx=10, pady=10)

# --- Hlavní cyklus aplikace ---
# Spustí hlavní smyčku událostí Tkinter, která čeká na akce uživatele
window.mainloop()





# # Result texty a data z API
# text_ico = Label(result_frame, text="IČO:", bg=BACKGROUND_COLOR, fg=TEXT_COLOR, font=FONT_TEXT)
# text_ico.grid(row=0, column=0, sticky="e", padx=10)
# ico = Label(result_frame, bg=BACKGROUND_COLOR, fg=TEXT_COLOR, font=FONT_TEXT)
# ico.grid(row=0, column=1, sticky="w")
#
# text_dic = Label(result_frame, text="DIČ:", bg=BACKGROUND_COLOR, fg=TEXT_COLOR, font=FONT_TEXT)
# text_dic.grid(row=1, column=0, sticky="e", padx=10)
# dic = Label(result_frame, bg=BACKGROUND_COLOR, fg=TEXT_COLOR, font=FONT_TEXT)
# dic.grid(row=1, column=1, sticky="w")
#
# text_jmeno = Label(result_frame, text="Jméno:", bg=BACKGROUND_COLOR, fg=TEXT_COLOR, font=FONT_TEXT)
# text_jmeno.grid(row=2, column=0, sticky="e", padx=10)
# jmeno = Label(result_frame, bg=BACKGROUND_COLOR, fg=TEXT_COLOR, font=FONT_TEXT)
# jmeno.grid(row=2, column=1, sticky="w")
#
# text_adresa = Label(result_frame, text="Adresa:", bg=BACKGROUND_COLOR, fg=TEXT_COLOR, font=FONT_TEXT)
# text_adresa.grid(row=3, column=0, sticky="e", padx=10)
# adresa = Label(result_frame, bg=BACKGROUND_COLOR, fg=TEXT_COLOR, font=FONT_TEXT)
# adresa.grid(row=3, column=1, sticky="w")
#
# text_adresa1 = Label(result_frame, text="Adresa1:", bg=BACKGROUND_COLOR, fg=TEXT_COLOR, font=FONT_TEXT)
# text_adresa1.grid(row=4, column=0, sticky="e", padx=10)
# adresa1 = Label(result_frame, bg=BACKGROUND_COLOR, fg=TEXT_COLOR, font=FONT_TEXT)
# adresa1.grid(row=4, column=1, sticky="w")
#
# text_psc = Label(result_frame, text="PSČ:", bg=BACKGROUND_COLOR, fg=TEXT_COLOR, font=FONT_TEXT)
# text_psc.grid(row=5, column=0, sticky="e", padx=10)
# psc = Label(result_frame, bg=BACKGROUND_COLOR, fg=TEXT_COLOR, font=FONT_TEXT)
# psc.grid(row=5, column=1, sticky="w")
#
# text_stat = Label(result_frame, text="Stát:", bg=BACKGROUND_COLOR, fg=TEXT_COLOR, font=FONT_TEXT)
# text_stat.grid(row=6, column=0, sticky="e", padx=10)
# stat = Label(result_frame, bg=BACKGROUND_COLOR, fg=TEXT_COLOR, font=FONT_TEXT)
# stat.grid(row=6, column=1, sticky="w")
#
# text_kod_stat = Label(result_frame, text="Kód státu:", bg=BACKGROUND_COLOR, fg=TEXT_COLOR, font=FONT_TEXT)
# text_kod_stat.grid(row=7, column=0, sticky="e", padx=10)
# kod_stat = Label(result_frame, bg=BACKGROUND_COLOR, fg=TEXT_COLOR, font=FONT_TEXT)
# kod_stat.grid(row=7, column=1, sticky="w")
#
# text_zalozeno = Label(result_frame, text="Vznik:", bg=BACKGROUND_COLOR, fg=TEXT_COLOR, font=FONT_TEXT)
# text_zalozeno.grid(row=8, column=0, sticky="e", padx=10)
# zalozeno = Label(result_frame, bg=BACKGROUND_COLOR, fg=TEXT_COLOR, font=FONT_TEXT)
# zalozeno.grid(row=8, column=1, sticky="w")
#
# text_spis_znacka = Label(result_frame, text="Spis. zn.:", bg=BACKGROUND_COLOR, fg=TEXT_COLOR, font=FONT_TEXT)
# text_spis_znacka.grid(row=9, column=0, sticky="e", padx=10)
# spis_znacka = Label(result_frame, bg=BACKGROUND_COLOR, fg=TEXT_COLOR, font=FONT_TEXT)
# spis_znacka.grid(row=9, column=1, sticky="w")
#
# text_cznace = Label(result_frame, text="czNace:", bg=BACKGROUND_COLOR, fg=TEXT_COLOR, font=FONT_TEXT)
# text_cznace.grid(row=10, column=0, sticky="e", padx=10)
# cznace = Label(result_frame, bg=BACKGROUND_COLOR, fg=TEXT_COLOR, font=FONT_TEXT)
# cznace.grid(row=10, column=1, sticky="w")
#
# text_aktualizace = Label(result_frame, text="Aktualizace:", bg=BACKGROUND_COLOR, fg=TEXT_COLOR, font=FONT_TEXT)
# text_aktualizace.grid(row=11, column=0, sticky="e", padx=10)
# aktualizace = Label(result_frame, bg=BACKGROUND_COLOR, fg=TEXT_COLOR, font=FONT_TEXT)
# aktualizace.grid(row=11, column=1, sticky="w")

