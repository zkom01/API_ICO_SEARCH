# 🔍 API ARES – Vyhledávač subjektů podle IČO

Desktopová Python aplikace s grafickým rozhraním pro vyhledávání informací o ekonomických subjektech z veřejného REST API [ARES](https://ares.gov.cz) (Administrativní registr ekonomických subjektů). Stačí zadat 8místné IČO a aplikace okamžitě zobrazí kompletní údaje o firmě nebo osobě.

---

## 📋 Obsah

1. [Technologie a závislosti](#1-technologie-a-závislosti)
2. [Struktura projektu](#2-struktura-projektu)
3. [Popis souborů](#3-popis-souborů)
4. [Jak aplikace funguje](#4-jak-aplikace-funguje)
5. [Zobrazované údaje](#5-zobrazované-údaje)
6. [Ošetření chyb](#6-ošetření-chyb)
7. [Systém témat (themes)](#7-systém-témat-themes)
8. [Instalace a spuštění](#8-instalace-a-spuštění)

---

## 1. Technologie a závislosti

| Knihovna | Účel |
|---|---|
| `customtkinter` | Moderní GUI framework postavený na Tkinteru |
| `requests` | HTTP dotazy na REST API ARES |
| `screeninfo` | Detekce rozlišení monitoru pro vycentrování okna |

Instalace závislostí:

```bash
pip install customtkinter requests screeninfo
```

---

## 2. Struktura projektu

```
API_ARES/
│
├── main.py           # Hlavní soubor – GUI a aplikační logika
├── api_ares.py       # Třída ApiAres – volání REST API ARES
├── settings.py       # Konstanty (rozměry okna, fonty)
├── dog.ico           # Ikona okna aplikace
├── zaloha_main.py    # Záložní / archivní verze main.py
├── .gitignore        # Ignorované soubory pro Git
│
└── themes/           # 19 vlastních barevných témat pro customtkinter
    ├── eda.json       # Výchozí téma (modro-azurové)
    ├── midnight.json
    ├── autumn.json
    ├── breeze.json
    └── ... (celkem 19 témat)
```

---

## 3. Popis souborů

### `api_ares.py` – Třída ApiAres

Jednoduchá třída zapouzdřující HTTP požadavek na veřejné API ARES.

```python
class ApiAres:
    def __init__(self, ico):
        self.ico = ico
        response = requests.get(
            f"https://ares.gov.cz/ekonomicke-subjekty-v-be/rest/ekonomicke-subjekty/{self.ico}"
        )
        response.raise_for_status()  # vyvolá výjimku při HTTP chybě (4xx, 5xx)
        self.data = response.json()  # deserializovaná JSON odpověď
```

Po úspěšném zavolání je kompletní JSON odpověď dostupná přes `api_ares.data`. Metoda `raise_for_status()` zajišťuje, že HTTP chyby (např. 404 – IČO nenalezeno) jsou zachyceny jako výjimky a ošetřeny v GUI vrstvě.

**Endpoint API:**
```
GET https://ares.gov.cz/ekonomicke-subjekty-v-be/rest/ekonomicke-subjekty/{ico}
```

---

### `settings.py` – Konstanty aplikace

Centrální místo pro nastavení rozměrů a typografie. Změna hodnot zde ovlivní celé GUI.

```python
WIDTH  = 440
HEIGHT = 470

FONT_NADPIS1  = "Helvetica", 20, "bold"   # hlavní nadpis
FONT_NADPIS   = "Helvetica", 18, "bold"   # vstupní pole a chybové hlášky
FONT_TEXT     = "Helvetica", 14, "bold"   # popisky a výsledky
FONT_BUTTONS  = "Helvetica", 14, "bold"   # tlačítka
```

---

### `main.py` – GUI a logika aplikace

Hlavní soubor obsahuje:
- inicializaci okna a jeho vycentrování na obrazovce
- layout ve čtyřech rámcích (`nadpis_frame`, `input_frame`, `result_frame`, `buton_frame`)
- validaci vstupu v reálném čase
- volání API a zobrazení výsledků
- ošetření chybových stavů

---

## 4. Jak aplikace funguje

### Tok dat

```
Uživatel zadá IČO
        │
        ▼
validate_input()          ← povolí pouze číslice, max. 8 znaků (real-time)
        │
        ▼
hledej() [klik na tlačítko nebo Enter]
        │
        ├── délka != 8 → zobrazí chybovou hlášku, ukončí
        │
        ▼
ApiAres(ico)              ← HTTP GET na ARES REST API
        │
        ├── ConnectionError → "Chyba připojení."
        ├── HTTPError 404   → "Zadané IČO nebylo nalezeno."
        ├── jiná HTTPError  → obecná chybová hláška
        │
        ▼
Parsování JSON odpovědi   ← přímé klíče + vnořené objekty (sidlo, dalsiUdaje)
        │
        ▼
Aktualizace Label widgetů v result_frame
```

### Validace vstupu

Funkce `validate_input()` je registrována jako `validatecommand` na vstupním poli – spouští se při **každém stisku klávesy** ještě před zápisem znaku:

```python
def validate_input(new_text):
    if new_text.isdigit() or new_text == "":
        if len(new_text) <= 8:
            return True
    return False
```

Uživatel tak nemůže zadat písmena ani zadávat více než 8 číslic – není nutná žádná dodatečná kontrola formátu.

### Layout GUI

```
┌─────────────────────────────────────────┐
│  nadpis_frame                           │
│  "Zadejte IČO a klikněte na Hledej."    │
├─────────────────────────────────┬───────┤
│  input_frame                    │       │
│  [ vstupní pole pro IČO    ]    [Hledej]│
├─────────────────────────────────────────┤
│  result_frame                           │
│  IČO:        28571533                   │
│  DIČ:        CZ28571533                 │
│  Jméno:      ...                        │
│  Adresa:     ...                        │
│  ...                                    │
├──────────────────────────┬──────────────┤
│  buton_frame             │              │
│                  [VYMAZAT]       [EXIT] │
└─────────────────────────────────────────┘
```

---

## 5. Zobrazované údaje

Aplikace zobrazuje následující pole z JSON odpovědi ARES API:

| Popisek v GUI | Klíč v JSON | Poznámka |
|---|---|---|
| IČO | `ico` | přímý klíč |
| DIČ | `dic` | přímý klíč |
| Jméno | `obchodniJmeno` | přímý klíč |
| Adresa | `sidlo.nazevUlice` + `cisloDomovni/cisloOrientacni` | vnořený objekt `sidlo` |
| Adresa1 | `sidlo.nazevObce` + `nazevCastiObce` | vnořený objekt `sidlo` |
| PSČ | `sidlo.psc` | vnořený objekt `sidlo` |
| Stát | `sidlo.nazevStatu` | vnořený objekt `sidlo` |
| Kód státu | `sidlo.kodStatu` | vnořený objekt `sidlo` |
| Vznik | `datumVzniku` | přímý klíč |
| Spis. zn. | `dalsiUdaje[2].spisovaZnacka` | pole vnořených objektů |
| czNace | `czNace` | přímý klíč |
| Aktualizace | `datumAktualizace` | přímý klíč |

Pokud klíč v odpovědi chybí, zobrazí se `N/A`.

---

## 6. Ošetření chyb

| Stav | Chybová zpráva | Barva |
|---|---|---|
| IČO nemá 8 číslic | `Chyba: Zadejte přesně 8 číslic` | červená |
| IČO nebylo v ARES nalezeno (HTTP 404) | `Zadané IČO nebylo nalezeno.` | oranžová |
| Žádné síťové připojení | `Chyba připojení.` | oranžová |
| Jiná HTTP chyba (4xx / 5xx) | obecná hláška s kódem | výchozí |

Při každém novém hledání i při chybě se předchozí výsledky automaticky vymažou funkcí `delete()`.

---

## 7. Systém témat (themes)

Aplikace obsahuje **19 vlastních barevných témat** ve formátu JSON pro knihovnu `customtkinter`. Každé téma definuje barvy pro světlý i tmavý režim (formát `["světlá_barva", "tmavá_barva"]`).

### Dostupná témata

| Název souboru | Charakter |
|---|---|
| `eda.json` | Modro-azurové – **výchozí téma** |
| `midnight.json` | Tmavě modré |
| `autumn.json` | Teplé podzimní |
| `breeze.json` | Světle vzdušné |
| `carrot.json` | Oranžové |
| `cherry.json` | Třešňově červené |
| `coffee.json` | Hnědé/kávové |
| `lavender.json` | Levandulové |
| `marsh.json` | Bažinově zelené |
| `metal.json` | Kovově šedé |
| `orange.json` | Jasně oranžové |
| `patina.json` | Patinově zelené |
| `pink.json` | Růžové |
| `red.json` | Červené |
| `rime.json` | Chladné bílé |
| `rose.json` | Růžovozlaté |
| `sky.json` | Nebesky modré |
| `violet.json` | Fialové |
| `yellow.json` | Žluté |

### Změna tématu

V `main.py` stačí upravit jeden řádek:

```python
customtkinter.set_default_color_theme("themes/eda.json")   # výchozí
# customtkinter.set_default_color_theme("themes/midnight.json")
# customtkinter.set_default_color_theme("themes/cherry.json")
```

Případně lze použít i vestavěná témata customtkinteru:

```python
customtkinter.set_default_color_theme("dark-blue")
customtkinter.set_default_color_theme("blue")
customtkinter.set_default_color_theme("green")
```

---

## 8. Instalace a spuštění

### Požadavky

- Python 3.8+
- Přístup k internetu (volání API ARES)

### Postup

**1. Klonování / stažení projektu**
```bash
git clone <url-repozitáře>
cd API_ARES
```

**2. Vytvoření virtuálního prostředí** *(doporučeno)*
```bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Linux / macOS
```

**3. Instalace závislostí**
```bash
pip install customtkinter requests screeninfo
```

**4. Spuštění aplikace**
```bash
python main.py
```

### Testovací IČO

Pro ověření funkčnosti lze zadat např.:

```
28571533
```

---

## 📌 Poznámky

- API ARES je veřejná služba státní správy ČR – nevyžaduje žádný API klíč ani registraci.
- Soubor `zaloha_main.py` obsahuje starší verzi GUI postavenou na původním `tkinter` (bez `customtkinter`) – slouží jako archivní záloha.
- Okno je pevně velikostní (`resizable(False, False)`) a automaticky se centruje na primárním monitoru.

---

*Desktopová aplikace API ARES – vyhledávač ekonomických subjektů ČR.*