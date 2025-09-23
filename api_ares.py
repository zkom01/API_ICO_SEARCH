# https://ares.gov.cz/ekonomicke-subjekty-v-be/rest/ekonomicke-subjekty/28571533
# request = žádost
# response = odpověď

import requests

class ApiAres:
   def __init__(self, ico):
    self.ico = ico
    response = requests.get(f"https://ares.gov.cz/ekonomicke-subjekty-v-be/rest/ekonomicke-subjekty/{self.ico}")
    # print(response)
    # print(response.status_code)
    response.raise_for_status() # v případě chyby , chybu vypíše
    self.data = response.json()






