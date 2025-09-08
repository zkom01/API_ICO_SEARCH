from tkinter import *
from screeninfo import get_monitors
from aplikace import Aplikace
from settings import *

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
window.minsize(width,height)
window.resizable(False,False)
window.iconbitmap("dog.ico")
window.config(bg=modra)


app = Aplikace(window)

# Hlavní cyklus
window.mainloop()

