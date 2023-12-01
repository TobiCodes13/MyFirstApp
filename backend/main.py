from fastapi import FastAPI
import json

PATH = "data/nfl_data.json"

app = FastAPI()

@app.get("/data")
async def get_data():
    with open(file=PATH, mode="r") as raw_file:     #Funtion oeffnet Datei aus Path im Lesemodus (r). With schliesst Datei direkt nach der Ausfuehrung um Ressourcen zu schonen                         
        data = json.load(raw_file)                  #Inhalt wird als json-File interpretiert und in Variabele data geladen
    return data


