# 🔍 API ARES – vyhledávač ekonomických subjektů podle IČO

Desktopová aplikace s grafickým rozhraním pro vyhledávání informací o firmách a osobách z veřejného registru [ARES](https://ares.gov.cz) (Administrativní registr ekonomických subjektů).

---

## 📋 Co aplikace zobrazuje

Po zadání IČO aplikace načte a zobrazí:

| Pole | Popis |
|---|---|
| IČO | Identifikační číslo osoby |
| DIČ | Daňové identifikační číslo |
| Jméno | Obchodní jméno subjektu |
| Adresa | Ulice a číslo popisné/orientační |
| Adresa | Obec a část obce |
| PSČ | Poštovní směrovací číslo |
| Stát | Název státu sídla |
| Kód státu | Dvoupísmenný kód státu (ISO) |
| Vznik | Datum vzniku subjektu |
| Spis. zn. | Spisová značka |
| czNace | Klasifikace ekonomické činnosti |
| Aktualizace | Datum poslední aktualizace záznamu |

---

## ⚙️ Instalace

### Požadavky

- Python 3.10+
- customtkinter
- requests
- screeninfo

### Instalace závislostí

```bash
pip install customtkinter requests screeninfo
```

### Spuštění

```bash
python main.py
```
---

## 🗂️ Struktura projektu

```
API_ARES/
├── main.py           # Hlavní soubor – GUI a aplikační logika
├── api_ares.py       # Třída ApiAres – komunikace s REST API ARES
├── settings.py       # Konstanty – rozměry okna a fonty
├── zaloha_main.py    # Záložní verze s klasickým tkinter (archiv)
├── dog.ico           # Ikona okna aplikace
└── themes/           # Barevné motivy pro customtkinter (19 témat)
    ├── eda.json       # Výchozí téma (modro-tyrkysové)
    ├── autumn.json
    ├── midnight.json
    └── ...            # a dalších 16 témat
```

---

## 🎨 Témata

Aplikace podporuje 19 barevných motivů. Téma se nastavuje v `main.py`:

```python
customtkinter.set_default_color_theme("themes/eda.json")
```

Dostupná témata: `autumn`, `breeze`, `carrot`, `cherry`, `coffee`, `eda`, `lavender`, `marsh`, `metal`, `midnight`, `orange`, `patina`, `pink`, `red`, `rime`, `rose`, `sky`, `violet`, `yellow`

Každé téma podporuje světlý i tmavý režim (přepínání přes systémové nastavení nebo `customtkinter.set_appearance_mode()`).

---

## 🌐 API ARES

Aplikace volá veřejné REST API ARES bez nutnosti autentizace:

```
GET https://ares.gov.cz/ekonomicke-subjekty-v-be/rest/ekonomicke-subjekty/{ico}
```

Příklad pro IČO `28571533`:
```
https://ares.gov.cz/ekonomicke-subjekty-v-be/rest/ekonomicke-subjekty/28571533
```

Odpověď je ve formátu JSON. Aplikace zpracovává i vnořené struktury jako `sidlo` (adresa sídla) a `dalsiUdaje` (spisová značka).

---

## ❗ Ošetřené chybové stavy

| Situace | Chování aplikace |
|---|---|
| IČO kratší nebo delší než 8 číslic | Zobrazí chybu, dotaz se neodesílá |
| IČO nebylo v ARES nalezeno (HTTP 404) | Zobrazí upozornění oranžově |
| Problém se sítí / bez internetu | Zobrazí chybu připojení oranžově |
| Jiná HTTP chyba (4xx / 5xx) | Zobrazí kód chyby červeně |
