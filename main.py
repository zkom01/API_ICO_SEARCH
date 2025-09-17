from tkinter import *
from screeninfo import get_monitors
from settings import *
from api_ares import *

# Funkce
def hledej():
    api_ares = ApiAres(vstup.get())
    result_ico["text"] = api_ares.data["ico"]
    result_jmeno["text"] = api_ares.data["obchodniJmeno"]

# Rozměry obrazovky
monitor = get_monitors()[0]
screen_width = monitor.width
screen_height = monitor.height

# Okno
window = Tk()
x = (screen_width // 2) - (width // 2)
y = (screen_height // 2) - (height // 2)
window.geometry(f"{width}x{height}+{x}+{y}")
window.title("Hledání subjektu podle IČO")
window.minsize(width, height)
window.resizable(False, False)
window.iconbitmap("dog.ico")
window.config(bg=modra)

# Framy
nadpis_frame = Frame(window, bg=modra)
nadpis_frame.pack(fill="x")
nadpis_frame.columnconfigure(0, weight=1)  # sloupec se roztáhne

input_frame = Frame(window, bg=modra)
input_frame.pack(fill="x")
input_frame.columnconfigure(0, weight=1)

result_frame = Frame(window, bg=modra)
result_frame.pack(fill="x")
# sloupec 1 s výsledky roztáhne, zatímco sloupec 0 s popisky zůstane pevný
result_frame.columnconfigure(0, weight=0) # sloupec s popisky se neroztáhne
result_frame.columnconfigure(1, weight=1) # sloupec s výsledky se roztáhne

buton_frame = Frame(window, bg=modra)
buton_frame.pack(fill="x")
buton_frame.columnconfigure(0, weight=1)

# Label (popisek)
text_okna = Label(nadpis_frame,
                  text="Zadejte IČO do pole níže a klikněte na Hledej.",
                  bg=modra,
                  fg=bila,
                  font=FONT_BIG
                  )
text_okna.grid(row=0, column=0, sticky="ew", pady=5)

# Vstupní pole (input)
vstup = Entry(input_frame, font=FONT_BIG )
vstup.focus()
vstup.insert(0, "28571533")
vstup.grid(row=0, column=0, sticky="ew", pady=10, padx=10)

# Tlačítko
tlacitko = Button(input_frame, text="Hledej", bg=modra, fg=bila, command=hledej, width=25, font=FONT_SMALL)
tlacitko.grid(row=0, column=1, sticky="ew", padx=10)

# Result texty a data z API
text_ico = Label(result_frame, text="IČO: ", bg=modra, fg=bila, font=FONT_MIDDLE)
text_ico.grid(row=0, column=0, sticky="e", padx=10)
result_ico = Label(result_frame, bg=modra, fg=bila, font=FONT_MIDDLE)
result_ico.grid(row=0, column=1, sticky="w")

text_jmeno = Label(result_frame, text="Jméno: ", bg=modra, fg=bila, font=FONT_MIDDLE)
text_jmeno.grid(row=1, column=0, sticky="e", padx=10)
result_jmeno = Label(result_frame, bg=modra, fg=bila, font=FONT_MIDDLE)
result_jmeno.grid(row=1, column=1, sticky="w")

# Spodní tlačítko
exit_buton = Button(buton_frame, text="EXIT", bg=modra, fg=bila, width=25, command=window.destroy, font=FONT_SMALL)
exit_buton.grid(row=0, column=0, sticky="e", padx=10, pady=10)

# Hlavní cyklus
window.mainloop()