from fastapi import FastAPI
from fastapi import Depends
import json
import pandas as pd

PATH = "data/nfl_data.json"   #Pfad zur JSON-Datei

app = FastAPI()               #Erstellen einer FastAPI-Instanz

def FileHandler():            #Funktion zum Lesen der JSON-Datei und Laden der Daten als JSON
    with open(file=PATH, mode="r") as raw_file:     #Funtion oeffnet Datei aus Path im Lesemodus (r). With schliesst Datei direkt nach der Ausfuehrung um Ressourcen zu schonen                         
        data = json.load(raw_file)                  #Inhalt wird als json-File interpretiert und in Variabele data geladen
    return data

#-------------------------------------------------------------------------

@app.get("/level-1/data")       #FastAPI-Endpunkt zum Abrufen der gesamten Daten
async def get_data():
    return FileHandler()

@app.get("/level-1/teams")      #FastAPI-Endpunkt zum Abrufen der Teams aus den Daten
async def get_teams():
    data = FileHandler()
    return data ["teams"]

#-------------------------------------------------------------------------

@app.get("/level-2/stats")      #FastAPI-Endpunkt zum Abrufen von Statistiken basierend auf dem übergebenen 'team_type'
async def get_stats(team_type: str = "team"):
    
    raw_data = FileHandler()    #Laden der Daten
    
    raw_data_df = pd.DataFrame(raw_data["games"])       #Erstellen eines Pandas DataFrame aus den Spielen in den Rohdaten
    
    stats = raw_data_df.groupby(team_type)[["points_scored", "points_allowed"]].mean()    #Berechnung der durchschnittlichen Punkte für das gegebene 'team_type'
    stats[team_type] = stats.index                      #Hinzufügen des Index als neue Spalte ('team_type')
    stats.sort_values("points_scored", ascending=False, inplace=True)  #Sortierung nach erzielten Punkten absteigend.
    stats.reset_index(drop=True, inplace=True)          #Index des DataFrames wird neu gesetzt und um 1 erhoeht.
    stats.index += 1
    
    return stats.to_json(orient="index")                #Umwandeln der Statistiken in ein JSON-Format mit Index-Orientierung

#-------------------------------------------------------------------------

@app.get("/level-3/algorithm")  #Definiert den API-Endpunkt für Level 3 (Algorithmus)
async def get_algorithm():
    
    raw_data = FileHandler()                                    #Ruft die Funktion FileHandler auf, um die Daten zu laden
    
    raw_data_df = pd.DataFrame(raw_data["games"])               #Erstellt ein Pandas DataFrame aus dem "games"-Teil der Daten
    
    prepared_data_df = raw_data_df.copy()                       #Kopiert das DataFrame, um die Originaldaten nicht zu verändern

    condition_1 = raw_data_df["points_scored"] - raw_data_df["points_allowed"] > 3  #Überprüft, ob das Team mehr als 3 Punkte Vorsprung hatte
    condition_2 = raw_data_df["points_scored"] - raw_data_df["points_allowed"] < 0  #Überprüft, ob das Team weniger Punkte erzielt hat als der Gegner

    prepared_data_df["true wins"] = condition_1 | condition_2   #Erzeugt eine neue Spalte "true_wins", die angibt, ob das Team das Spiel gewonnen hat (True) oder nicht (False).

    return prepared_data_df.to_json(orient="index")             #Konvertiert das DataFrame in JSON und gibt es zurück

#-------------------------------------------------------------------------
