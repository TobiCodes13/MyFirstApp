import json
from bs4 import BeautifulSoup
from requests import Session, RequestException
from rich import print
import time

#Deklaration Variablen
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0"}
INPUT_PATH = "/home/tobi/Workspace/MyFirstApp/season_links.json"
OUTPUT_FILE = "nfl_data_new.json"

#-----------------------------------------------------------------------------------------------------------------------
#Funktionen

#Einlesen json mit URL-Seiten'
def read_json(path: str) -> dict:
   with open(path, "r") as file:
      data= json.load(file) 
   return data

#Funktion zum Senden von HTTP-Anfragen mit Wiederholungsversuchen
def request_url(session: Session, url: str, retries: int = 3, timeout: int = 10):
    for _ in range(retries):
        try:
            
            response = session.get(url=url, timeout=timeout, headers=HEADERS) #Sendet eine HTTP-Anfrage und erhalte die Antwort
            response.raise_for_status()                                       #Wirft eine Ausnahme im Falle eines HTTP-Fehlers
            return response.text                                              #Gibt den Textinhalt der Antwort zurück
         
        except RequestException as raised_exception:                          #Behandelt eine RequestException, wenn die Anfrage fehlschlägt
            print(f"Die Anfrage an {url} ist fehlgeschlagen.")
            continue
         
    print(f"Die Anfrage an {url} ist final fehlgeschlagen.")   #Gib eine Meldung aus, wenn die Anfrage nach mehreren Versuchen endgültig fehlschlägt
    return

#Funktion zum Parsen von HTML zu BeautifulSoup-Objekten
def parse_html_to_soup(html: str) -> BeautifulSoup:
    return BeautifulSoup(html, "html.parser")




#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

def main():
   boxscore_links = (read_json(path=INPUT_PATH))
   http_session = Session()
   
   #url = "https://www.pro-football-reference.com/boxscores/202312040jax.htm"
   
   scraped_data = dict()
   
   #for key, urls in list(boxscore_links.items())[:2]:
   for key, urls in boxscore_links.items():
      payload_data = []
      
      for url in urls:
         
         time.sleep(2)
         html = request_url(session=http_session, url=url)
         soup = parse_html_to_soup(html)
         table = soup.find("table", class_ = "linescore")
         
         rows = table.select("table tbody tr")
         
         teams = []
         
         for row in rows:
            table_data_cells = row.find_all(["td"])
            team_name = table_data_cells[1].text
            point_cells = table_data_cells[2:]
            points = [int(cell.text) for cell in point_cells]
            final_points = points[-1]
            quarter_points = points[:-1]
            
            if not (final_points == sum(quarter_points)):
               raise ValueError("Quarter Points do not match final points")
            
            result = (team_name, final_points)
            teams.append(result)
            
         data = {
            "team": teams[1][0],
            "opponent": teams[0][0],
            "points_scored": teams[1][1],
            "points_allowed": teams[0][1],
         }
            
         payload_data.append(data)
         
         
         
      updated_key = f"2023/week-{key.split('_')[1]}" #Änderung der Namensgebung auf "2023/week-XX"
      scraped_data[updated_key] = payload_data
      print(scraped_data)  

   # Speichere die Daten als JSON-Datei
   with open(OUTPUT_FILE, "w") as output_file:
      json.dump(scraped_data, output_file, indent=2)
      
   return
   
if __name__ == "__main__":
    main()