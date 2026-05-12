# 🔍 API ARES – vyhledávač ekonomických subjektů podle IČO

Desktopová aplikace v Pythonu s grafickým rozhraním, která umožňuje rychlé vyhledání a zobrazení informací o firmách z veřejného registru ARES.

Cílem projektu je zjednodušit práci s veřejnými daty a poskytnout přehledné GUI nad REST API ARES.

---

## ⚙️ Hlavní funkce

- **Vyhledání subjektu** podle IČO.
- **Načtení detailů** přímo z registru ARES.
- **Zobrazení informací**: adresa, identifikační údaje, ekonomická činnost (NACE).
- **Validace vstupu**: kontrola formátu IČO před odesláním požadavku.
- **Robustní error handling**: ošetření výpadků sítě, neexistujících IČO a chyb API.
- **Moderní vzhled**: GUI postavené na knihovně customtkinter.

---

## 🌐 Použité API

Aplikace využívá oficiální REST API systému ARES:

https://ares.gov.cz/ekonomicke-subjekty-v-be/rest/ekonomicke-subjekty/{ico}

---

## 🧰 Použité technologie

- Python 3.10+
- customtkinter – pro moderní vzhled oken
- requests – pro HTTP komunikaci
- screeninfo – pro správné centrování okna na monitoru

---

## ▶️ Spuštění

1. Nainstalujte potřebné knihovny:

pip install customtkinter requests screeninfo

2. Spusťte aplikaci:

python main.py

---

## 🗂️ Struktura projektu
```
API_ARES/
├── main.py         # GUI a hlavní logika aplikace
├── api_ares.py     # Komunikace s ARES API
├── settings.py     # Konfigurace aplikace a konstanty
├── dog.ico         # Ikona aplikace
└── themes/         # Barevné motivy GUI (JSON)
```

---

## 🎨 UI a témata

Aplikace podporuje custom témata. 

Výchozí nastavení využívá motiv: themes/eda.json.

---

## ⚠️ Ošetření chyb

Aplikace aktivně monitoruje a informuje uživatele o těchto stavech:
- Nevalidní IČO: Formátová kontrola délky a znaků.
- Nenalezený subjekt: Ošetření HTTP stavu 404.
- Výpadek připojení: Detekce nedostupnosti internetu nebo API.
- Obecné HTTP chyby: Ošetření ostatních návratových kódů (500, 403 atd.).

---

## 🧠 Klíčové koncepty projektu

Tento projekt demonstruje praktické využití:
- Asynchronního (nebo blokujícího) volání REST API.
- Parsování a strukturování JSON dat.
- Objektově orientovaného návrhu desktopového GUI.
- Validace vstupů a uživatelsky přívětivého hlášení chyb.
