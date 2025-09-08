from tkinter import *
from settings import *

class Aplikace:
    def __init__(self, tkokno):
        self.tkokno = tkokno
        self.zmena = False

        # Label (popisek)
        self.text_okna = Label(tkokno, text="Zadejte IČO do pole níže a klikněte na Hledej.", bg=modra, fg=bila,
                          font=("Helvetica", 14, "bold"),
                          borderwidth=5, relief="groove")
        self.text_okna.pack(ipadx=10, ipady=10, padx=5, pady=15)

        self.tlacitko = Button(tkokno, text="Hledej", command=self.hledej)
        self.tlacitko.pack()

    def hledej(self):
        if not self.zmena:
            self.text_okna["bg"] = "red"
            self.text_okna["text"] = "změna na červenou"
            self.zmena = True
        else:
            self.text_okna["bg"] = "green"
            self.text_okna["text"] = "změna na zelenou"
            self.zmena = False

