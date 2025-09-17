from tkinter import *
from screeninfo import get_monitors
from settings import *
from api_ares import *

# Funkce
def hledej():
    api_ares = ApiAres(vstup.get())
    result_ico["text"] = api_ares.data["ico"]
    result_dic["text"] = api_ares.data["dic"]
    result_jmeno["text"] = api_ares.data["obchodniJmeno"]
    result_adresa["text"] = f"{api_ares.data["sidlo"]["nazevUlice"]} {api_ares.data["sidlo"]["cisloDomovni"]}/{api_ares.data["sidlo"]["cisloOrientacni"]}"
    result_adresa1["text"] = f"{api_ares.data["sidlo"]["nazevObce"]} - {api_ares.data["sidlo"]["nazevCastiObce"]}"
    result_psc["text"] = api_ares.data["sidlo"]["psc"]
    result_stat["text"] = api_ares.data["sidlo"]["nazevStatu"]
    result_kod_stat["text"] = api_ares.data["sidlo"]["kodStatu"]
    result_zalozeno["text"] = api_ares.data["datumVzniku"]
    result_spis_znacka["text"] = api_ares.data["dalsiUdaje"][2]["spisovaZnacka"]
    result_cznace["text"] = api_ares.data["czNace"]
    result_aktualizace["text"] = api_ares.data["datumAktualizace"]

# Rozměry obrazovky
monitor = get_monitors()[0]
screen_width = monitor.width
screen_height = monitor.height

# Okno
window = Tk()
x = (screen_width // 2) - (WIDTH // 2)
y = (screen_height // 2) - (HEIGHT // 2)
window.geometry(f"{WIDTH}x{HEIGHT}+{x}+{y}")
window.title("Hledání subjektu podle IČO")
window.minsize(WIDTH, HEIGHT)
window.resizable(False, False)
window.iconbitmap("dog.ico")
window.config(bg=BACKGROUND_COLOR)

# Framy
nadpis_frame = Frame(window, bg=BACKGROUND_COLOR)
nadpis_frame.pack(fill="x")
nadpis_frame.columnconfigure(0, weight=1)  # sloupec se roztáhne

input_frame = Frame(window, bg=BACKGROUND_COLOR)
input_frame.pack(fill="x")
input_frame.columnconfigure(0, weight=1)

result_frame = Frame(window, bg=BACKGROUND_COLOR)
result_frame.pack(fill="x")
# sloupec 1 s výsledky roztáhne, zatímco sloupec 0 s popisky zůstane pevný
result_frame.columnconfigure(0, weight=0) # sloupec s popisky se neroztáhne
result_frame.columnconfigure(1, weight=1) # sloupec s výsledky se roztáhne

buton_frame = Frame(window, bg=BACKGROUND_COLOR)
buton_frame.pack(fill="x")
buton_frame.columnconfigure(0, weight=1)

# Label (popisek)
text_okna = Label(nadpis_frame,
                  text="Zadejte IČO a klikněte na Hledej.",
                  bg=BACKGROUND_COLOR,
                  fg=TEXT_COLOR,
                  font=FONT_NADPIS
                  )
text_okna.grid(row=0, column=0, sticky="ew", pady=10)

# Vstupní pole (input)
vstup = Entry(input_frame, font=FONT_NADPIS)
vstup.focus()
vstup.insert(0, "28571533")
vstup.grid(row=0, column=0, sticky="ew", pady=5, padx=10)
# Tlačítko
tlacitko = Button(input_frame, text="Hledej", bg=BUTTON_COLOR, fg=TEXT_COLOR, command=hledej, width=25, font=FONT_BUTTONS)
tlacitko.grid(row=0, column=1, sticky="ew", pady=5, padx=10)

# Result texty a data z API
text_ico = Label(result_frame, text="IČO:", bg=BACKGROUND_COLOR, fg=TEXT_COLOR, font=FONT_TEXT)
text_ico.grid(row=0, column=0, sticky="e", padx=10)
result_ico = Label(result_frame, bg=BACKGROUND_COLOR, fg=TEXT_COLOR, font=FONT_TEXT)
result_ico.grid(row=0, column=1, sticky="w")

text_dic = Label(result_frame, text="DIČ:", bg=BACKGROUND_COLOR, fg=TEXT_COLOR, font=FONT_TEXT)
text_dic.grid(row=1, column=0, sticky="e", padx=10)
result_dic = Label(result_frame, bg=BACKGROUND_COLOR, fg=TEXT_COLOR, font=FONT_TEXT)
result_dic.grid(row=1, column=1, sticky="w")

text_jmeno = Label(result_frame, text="Jméno:", bg=BACKGROUND_COLOR, fg=TEXT_COLOR, font=FONT_TEXT)
text_jmeno.grid(row=2, column=0, sticky="e", padx=10)
result_jmeno = Label(result_frame, bg=BACKGROUND_COLOR, fg=TEXT_COLOR, font=FONT_TEXT)
result_jmeno.grid(row=2, column=1, sticky="w")

text_adresa = Label(result_frame, text="Adresa:", bg=BACKGROUND_COLOR, fg=TEXT_COLOR, font=FONT_TEXT)
text_adresa.grid(row=3, column=0, sticky="e", padx=10)
result_adresa = Label(result_frame, bg=BACKGROUND_COLOR, fg=TEXT_COLOR, font=FONT_TEXT)
result_adresa.grid(row=3, column=1, sticky="w")

text_adresa1 = Label(result_frame, text="Adresa1:", bg=BACKGROUND_COLOR, fg=TEXT_COLOR, font=FONT_TEXT)
text_adresa1.grid(row=4, column=0, sticky="e", padx=10)
result_adresa1 = Label(result_frame, bg=BACKGROUND_COLOR, fg=TEXT_COLOR, font=FONT_TEXT)
result_adresa1.grid(row=4, column=1, sticky="w")

text_psc = Label(result_frame, text="PSČ:", bg=BACKGROUND_COLOR, fg=TEXT_COLOR, font=FONT_TEXT)
text_psc.grid(row=5, column=0, sticky="e", padx=10)
result_psc = Label(result_frame, bg=BACKGROUND_COLOR, fg=TEXT_COLOR, font=FONT_TEXT)
result_psc.grid(row=5, column=1, sticky="w")

text_stat = Label(result_frame, text="Stát:", bg=BACKGROUND_COLOR, fg=TEXT_COLOR, font=FONT_TEXT)
text_stat.grid(row=6, column=0, sticky="e", padx=10)
result_stat = Label(result_frame, bg=BACKGROUND_COLOR, fg=TEXT_COLOR, font=FONT_TEXT)
result_stat.grid(row=6, column=1, sticky="w")

text_kod_stat = Label(result_frame, text="Kód státu:", bg=BACKGROUND_COLOR, fg=TEXT_COLOR, font=FONT_TEXT)
text_kod_stat.grid(row=7, column=0, sticky="e", padx=10)
result_kod_stat = Label(result_frame, bg=BACKGROUND_COLOR, fg=TEXT_COLOR, font=FONT_TEXT)
result_kod_stat.grid(row=7, column=1, sticky="w")

text_zalozeno = Label(result_frame, text="Vznik:", bg=BACKGROUND_COLOR, fg=TEXT_COLOR, font=FONT_TEXT)
text_zalozeno.grid(row=8, column=0, sticky="e", padx=10)
result_zalozeno = Label(result_frame, bg=BACKGROUND_COLOR, fg=TEXT_COLOR, font=FONT_TEXT)
result_zalozeno.grid(row=8, column=1, sticky="w")

text_spis_znacka = Label(result_frame, text="Spis. zn.:", bg=BACKGROUND_COLOR, fg=TEXT_COLOR, font=FONT_TEXT)
text_spis_znacka.grid(row=9, column=0, sticky="e", padx=10)
result_spis_znacka = Label(result_frame, bg=BACKGROUND_COLOR, fg=TEXT_COLOR, font=FONT_TEXT)
result_spis_znacka.grid(row=9, column=1, sticky="w")

text_cznace = Label(result_frame, text="czNace:", bg=BACKGROUND_COLOR, fg=TEXT_COLOR, font=FONT_TEXT)
text_cznace.grid(row=10, column=0, sticky="e", padx=10)
result_cznace = Label(result_frame, bg=BACKGROUND_COLOR, fg=TEXT_COLOR, font=FONT_TEXT)
result_cznace.grid(row=10, column=1, sticky="w")

text_aktualizace = Label(result_frame, text="Aktualizace:", bg=BACKGROUND_COLOR, fg=TEXT_COLOR, font=FONT_TEXT)
text_aktualizace.grid(row=11, column=0, sticky="e", padx=10)
result_aktualizace = Label(result_frame, bg=BACKGROUND_COLOR, fg=TEXT_COLOR, font=FONT_TEXT)
result_aktualizace.grid(row=11, column=1, sticky="w")



# Spodní tlačítko
exit_buton = Button(buton_frame, text="EXIT", bg=BUTTON_COLOR, fg=TEXT_COLOR, width=25, command=window.destroy, font=FONT_BUTTONS)
exit_buton.grid(row=0, column=0, sticky="es", padx=10, pady=10)

# Hlavní cyklus
window.mainloop()