#Import der benoetigten Bibliotheken
import json
import streamlit as st
import pandas as pd


#Level 1
def provide_raw_data(path):                                 #Definition Funktion "provide_raw_data". Path wird als Uebergabeparameter erwartet
    with open(file=path, mode="r") as raw_file:             #Funtion oeffnet Datei aus Path im Lesemodus (r). With schliesst Datei direkt nach der Ausfuehrung um Ressourcen zu schonen                         
        raw_data = json.load(raw_file)                      #Inhalt wird als json-File interpretiert und in Variabele raw_data geladen

    raw_data_df = pd.DataFrame(raw_data["games"])           #"games"-Daten werden raw_data in ein Pandas DataFrame (Liste) "raw_data_df" konvertiert

    home_team = st.selectbox(label="Home Team", options=raw_data["teams"], index=0) #Auswahlbox fuer das Heimteam. Infos kommen aus dem "teams"-Spalte der json-Datei. Erstes Team standardmaessig ausgewaehlt (Index = 0)
    away_team = st.selectbox(label="Away Team", options=raw_data["teams"], index=1) #Auswahlbox fuer das Auswaertsteam. Infos kommen aus dem "teams"-Spalte der json-Datei. Zweite Team standardmaessig ausgewaehlt (Index = 1)

    with st.expander(label="Raw Data"):                     #Rohdaten (raw_data) werden in einem Expanderbereich von Streamlit angezeigt
        st.json(raw_data)

    return raw_data_df, home_team, away_team                #Funktion gibt das Data Frame und die Heim- sowie Hauswaertsteams zurueck


#Level 2
def provide_derived_data(raw_data_df):                      #Funktion mit dem Namen "provide_derived_data". Erwartet den Pandas Data Frame "raw_data_df" als Uebergabe (Siehe provide_raw_data)
    with st.expander(label="Insights"):                     #Ein Expander in Streamlit wird erstellt und mit dem Label "Insights" versehen.
        st.subheader("Home Insights")                       #Ueberschrift fuer die Heimstatistiken wird hinzugefuegt.
        home_stats = raw_data_df.groupby("team")[["points_scored", "points_allowed"]].mean()    #Berechnung der durchschnittlichen Punkte erzielt/zugelassen.
        home_stats["team"] = home_stats.index               #Der Index (Heimteam) wird als eine neue Spalte hinzugefuegt.
        home_stats.sort_values("points_scored", ascending=False, inplace=True)  #Sortierung nach erzielten Punkten absteigend.
        home_stats.reset_index(drop=True, inplace=True)     #Index des DataFrames wird neu gesetzt und um 1 erhoeht.
        home_stats.index += 1
        st.write(home_stats)                                #Anzeige Heimstatistiken in Streamlit

        st.subheader("Away Insights")                       #Ueberschrift fuer die Auswaertsstatistiken wird hinzugefuegt.
        away_stats = raw_data_df.groupby("opponent")[["points_scored", "points_allowed"]].mean()    #Berechnung der durchschnittlichen Punkte erzielt/zugelassen.
        away_stats["team"] = away_stats.index               #Der Index (Auswaertsteam) wird als eine neue Spalte hinzugefuegt.
        away_stats.sort_values("points_scored", ascending=False, inplace=True)  #Sortierung nach erzielten Punkten absteigend.
        away_stats.reset_index(drop=True, inplace=True)     #Index des DataFrames wird neu gesetzt und um 1 erhoeht.
        away_stats.index += 1
        st.write(away_stats)                                #Anzeige Auswaertsstatistiken in Streamlit.

    return home_stats, away_stats                           #Rueckgabe Heim- & Auswaertsstatistik




def main():                                                     #Main-Funktion.
    
    st.title("NFL-Predictor")                                   #Titel Streamlit = NFL-Predictor.

    path = "data/nfl_data.json"                                 #Dateipfad der json-Datei wird in Variablen path gespeichert (Uebergabe zu "provide_raw_data").

    # Level 1
    raw_data_df, home_team, away_team = provide_raw_data(path=path) #Funktion fuer Level 1 wird aufgrufen und Rueckgabewerte in Variablen gespeichert.

    # Level 2
    home_stats, away_stats = provide_derived_data(raw_data_df=raw_data_df) #Funktion fuer Level 2 wird aufgerufen und Statistiken werden in Variabelen gespeichert.

    return                                                      #Keine Rueckgabe von Variablen


if __name__ == "__main__":                                      #Funktion stellt sicher, dass Main nur ausgefuert wird, wenn Skript direkt ausgefuehrt wird.
    main()
