from tkinter import *
from screeninfo import get_monitors
from settings import *

# Funkce
def hledej():
    result_ico["text"] = vstup.get()

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
input_frame = Frame(window, bg=modra)
result_frame = Frame(window, bg=modra)
buton_frame = Frame(window, bg=modra)

nadpis_frame.pack(pady=10)
input_frame.pack(pady=10)
result_frame.pack(fill="x", anchor="w", pady=10)
buton_frame.pack(fill="x", side="bottom", pady=10)

# Label (popisek)
text_okna = Label(
    nadpis_frame,
    text="Zadejte IČO do pole níže a klikněte na Hledej.",
    bg=modra,
    fg=bila,
    font=("Helvetica", 14, "bold")
)
text_okna.grid(row=0, column=0)

# Vstupní pole (input)
vstup = Entry(input_frame, font=("Helvetica", 14, "bold"))
vstup.focus()
vstup.grid(row=0, column=0)

# Tlačítko
tlacitko = Button(input_frame, text="Hledej", bg=modra, fg=bila, command=hledej, width=25)
tlacitko.grid(row=0, column=1, padx=10)

# Result texty a data z API
text_ico = Label(result_frame, text="IČO: ", bg=modra, fg=bila, font=("Helvetica", 14, "bold"))
text_ico.grid(row=0, column=0, padx=50, pady=10)

result_ico = Label(result_frame, bg=modra, fg=bila, font=("Helvetica", 14, "bold"))
result_ico.grid(row=0, column=1, sticky="w")

# Spodní tlačítko
exit_buton = Button(buton_frame, text="EXIT", bg=modra, fg=bila, width=25, command=window.destroy)
exit_buton.pack(side="right", padx=10)

# Hlavní cyklus
window.mainloop()