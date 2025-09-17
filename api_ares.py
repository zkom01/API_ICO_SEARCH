# https://ares.gov.cz/ekonomicke-subjekty-v-be/rest/ekonomicke-subjekty/28571533
# request = žádost
# response = odpověď

import requests

class ApiAres:
   def __init__(self, ico):
    # ico = input("Zadejte ICO (8 číslic): ")
    self.ico = ico
    self.data = None
    response = requests.get(f"https://ares.gov.cz/ekonomicke-subjekty-v-be/rest/ekonomicke-subjekty/{self.ico}")
    # print(response)
    # print(response.status_code)
    response.raise_for_status() # v případě chyby , chybu vypíše
    self.data = response.json()


    # print(data)
    # print(data["ico"])
    # print(data["obchodniJmeno"])

    # print(data["sidlo"]["kodStatu"])
    # print(data["sidlo"]["nazevStatu"])
    # print(data["sidlo"]["nazevKraje"])
    # print(data["sidlo"]["nazevObce"])
    # print(data["sidlo"]["nazevUlice"])
    # print(data["sidlo"]["cisloDomovni"])
    # print(data["sidlo"]["cisloOrientacni"])
    # print(data["sidlo"]["nazevCastiObce"])
    # print(data["sidlo"]["psc"])
    # print(data["sidlo"]["textovaAdresa"])
    # print(data["datumVzniku"])
    # print(data["datumAktualizace"])
    # print(data["dic"])
    # # print(data["adresaDorucovaci"])
    # print(data["adresaDorucovaci"]["radekAdresy1"])
    # print(data["adresaDorucovaci"]["radekAdresy2"])
    # print(data["adresaDorucovaci"]["radekAdresy3"])
    # print(data["dalsiUdaje"][2]["spisovaZnacka"])
    # print(data["czNace"])




