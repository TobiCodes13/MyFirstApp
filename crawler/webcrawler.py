
#Importiere erforderliche Bibliotheken
import json
from bs4 import BeautifulSoup
from requests import Session, RequestException
from rich import print


#Definiere von Konstanten
URL = "https://www.pro-football-reference.com"
BOX_URL = URL + "/boxscores/"
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0"}
OUTPUT_FILE = "season_links.json"

#-------------------------------------------------------------------------------------------------------------------------------------------------------------
#Funktionen

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

#Funktion zum Extrahieren von Informationen zur aktuellen Woche aus dem HTML
def extract_current_week_info(soup: BeautifulSoup) -> list: 
    # Extrahiert den Textinhalt des ersten h2-Elements und zerlegt ihn in eine Liste
    h2_element = soup.select_one("h2").text
    info_list = h2_element.split()
    return "/".join(info_list)                                 #Kombiniert die Elemente der Liste zu einem einzigen String

#Funktion zum Extrahieren von Links zu Spielzusammenfassungen (Box Scores)
def extract_boxscore_links(soup: BeautifulSoup) -> list:
   
    links = soup.select("a:-soup-contains('Final')")  #Selektiere alle Links, die den Text 'Final' enthalten

    return [URL + link['href'] for link in links]     #Erstelle eine Liste von vollständigen URLs, indem du die Basis-URL hinzufügst

#Funktion zum Erstellen von Links zu den Wochen einer Saison
def create_week_links(key: str) -> list:
    # Zerlege den Schlüssel in seine Bestandteile
    season, week, current_week_no = key.split("/")             #Zerlegt den Schlüssel in seine Bestandteile
    week_links = list()
    
    #Iteriere über die Wochennummern von der aktuellen Woche bis zur ersten Woche
    for week_no in range(int(current_week_no), 0, -1):
        week_link = f"{URL}/years/{season}/week_{week_no}.htm" #Erstellt den Wochenlink
        week_links.append(week_link)                           #Fügt ihn zur Liste hinzu
        week_links.append(week_link)
    
    return week_links                                          #Gib die Liste der Wochenlinks zurück

# Funktion zum Umwandeln von Wochenlinks in ein Dictionary von Box-Score-Links für die gesamte Saison
def transform_to_season_boxscore_links_dict(session: Session, week_links: list) -> dict:
    season_boxscore_links = dict()
    
    for week_link in week_links:                                        #Iteriert über die Wochenlinks
        
        week_key = "".join(week_link.split(".")[2].split("/")[-2:])     #Extrahiert die Woche aus dem Link und erstelle einen eindeutigen Schlüssel
        html = request_url(session=session, url=week_link)              #Sendet eine Anfrage für den Wochenlink und erhalte den HTML-Inhalt
        soup = parse_html_to_soup(html=html)                            #Parset das HTML und extrahieren Sie die Box-Score-Links
        boxscore_links = extract_boxscore_links(soup=soup)
        season_boxscore_links[week_key] = boxscore_links                #Fügt die Box-Score-Links dem Dictionary hinzu
   
    return season_boxscore_links                                        #Gibt das fertige Dictionary zurück

# Funktion zum Schreiben von Daten in eine JSON-Datei
def load_to_json_file(path: str, data: dict) -> None:
    with open(path, "w") as file:
        json.dump(data, file)          #Schreibt das Dictionary als JSON in die Datei
    return




#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Hauptfunktion des Skripts
def main():
   
    #Erstellt eine HTTP-Session und rufe die HTML-Seite mit den Box Scores auf
    http_session = Session()
    html = request_url(session=http_session, url=BOX_URL)
    soup = parse_html_to_soup(html)

    #Extrahiert Informationen zur aktuellen Woche
    key = extract_current_week_info(soup=soup)
    
    #Erstellt Links zu den Wochen der aktuellen Saison
    week_links = create_week_links(key)

    #Transformiert Wochenlinks in ein Dictionary von Box-Score-Links für die gesamte Saison
    season_boxscore_links = transform_to_season_boxscore_links_dict(session=http_session, week_links=week_links)

    #Speichert die Daten in einer JSON-Datei
    load_to_json_file(path=OUTPUT_FILE, data=season_boxscore_links)


if __name__ == "__main__":
    main()
