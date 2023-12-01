#Import der benoetigten Bibliotheken
import json
import streamlit as st
import pandas as pd
import requests

URL = "http://127.0.0.1:8000"
ENDPOINT_DATA = URL+"/data"
ENDPOINT_TEAMS = URL+"/teams"

#Level 1
def provide_raw_data():                                 #Definition Funktion "provide_raw_data". Path wird als Uebergabeparameter erwartet
    
    response = requests.get(url=ENDPOINT_DATA)
    raw_data = response.json()

    with st.expander(label="Raw Data"):                     #Rohdaten (raw_data) werden in einem Expanderbereich von Streamlit angezeigt
        st.json(raw_data)

    return            


# #Level 2
# def provide_derived_data(raw_data_df):                      #Funktion mit dem Namen "provide_derived_data". Erwartet den Pandas Data Frame "raw_data_df" als Uebergabe (Siehe provide_raw_data)
    
#      raw_data_df = pd.DataFrame(raw_data["games"])           #"games"-Daten werden raw_data in ein Pandas DataFrame (Liste) "raw_data_df" konvertiert
    
    
#     with st.expander(label="Insights"):                     #Ein Expander in Streamlit wird erstellt und mit dem Label "Insights" versehen.
#         st.subheader("Home Insights")                       #Ueberschrift fuer die Heimstatistiken wird hinzugefuegt.
#         home_stats = raw_data_df.groupby("team")[["points_scored", "points_allowed"]].mean()    #Berechnung der durchschnittlichen Punkte erzielt/zugelassen.
#         home_stats["team"] = home_stats.index               #Der Index (Heimteam) wird als eine neue Spalte hinzugefuegt.
#         home_stats.sort_values("points_scored", ascending=False, inplace=True)  #Sortierung nach erzielten Punkten absteigend.
#         home_stats.reset_index(drop=True, inplace=True)     #Index des DataFrames wird neu gesetzt und um 1 erhoeht.
#         home_stats.index += 1
#         st.write(home_stats)                                #Anzeige Heimstatistiken in Streamlit

#         st.subheader("Away Insights")                       #Ueberschrift fuer die Auswaertsstatistiken wird hinzugefuegt.
#         away_stats = raw_data_df.groupby("opponent")[["points_scored", "points_allowed"]].mean()    #Berechnung der durchschnittlichen Punkte erzielt/zugelassen.
#         away_stats["team"] = away_stats.index               #Der Index (Auswaertsteam) wird als eine neue Spalte hinzugefuegt.
#         away_stats.sort_values("points_scored", ascending=False, inplace=True)  #Sortierung nach erzielten Punkten absteigend.
#         away_stats.reset_index(drop=True, inplace=True)     #Index des DataFrames wird neu gesetzt und um 1 erhoeht.
#         away_stats.index += 1
#         st.write(away_stats)                                #Anzeige Auswaertsstatistiken in Streamlit.

#     return home_stats, away_stats                           #Rueckgabe Heim- & Auswaertsstatistik


#Level 3
def provide_algorithm(raw_data_df):                         #Erzeugung Funktion zur Vorhersage. Uebergabe von Rohdaten
    
    with st.expander("Algorithm for Home Advantage"):       #Expander Streamlit
        st.markdown(                                        #Erklaerung zur Ermittlung der Vorhersage
            """
                    **Heimvorteil sind +3 Punkte im Handicap**  
                    *(Modellierte Annahme)*
                    
                    Erklärung:
                    Die Schätzung des Heimvorteils in der NFL auf ungefähr 2,5 bis 3 Punkte pro Spiel basiert auf einer Kombination von historischen Daten, Studien und Erfahrungen von Sportanalysten. Es ist wichtig zu beachten, dass dies eine allgemeine Schätzung ist und keine exakte wissenschaftliche Berechnung darstellt. Hier sind einige der Quellen und Grundlagen, auf denen diese Schätzung basiert:
                    - **Historische Daten:** Durch die Analyse von jahrzehntelangen NFL-Spielprotokollen können Sportanalysten Muster erkennen, die darauf hinweisen, dass Teams, die zu Hause spielen, tendenziell bessere Ergebnisse erzielen als bei Auswärtsspielen. Dies kann als Ausgangspunkt für die Schätzung des Heimvorteils dienen.
                    - **Akademische Studien:** Es gibt einige akademische Studien und wissenschaftliche Arbeiten, die den Heimvorteil im Sport, einschließlich der NFL, untersuchen. Diese Studien nutzen statistische Methoden, um den Heimvorteil zu quantifizieren. Obwohl die Ergebnisse variieren können, zeigen viele dieser Studien einen Heimvorteil von etwa 2,5 bis 3 Punkten pro Spiel.
                    - **Erfahrung von Sportanalysten:** Sportexperten und Analysten, die die NFL und andere Sportligen abdecken, bringen ihre Erfahrung und Einsichten in die Schätzung des Heimvorteils ein. Dies kann auf beobachteten Mustern und ihrer Kenntnis der Dynamik von Heim- und Auswärtsspielen basieren.
                    """
        )

        prepared_data_df = raw_data_df.copy()               #Kopie der Rohdaten wird erstellt um Originaldaten nicht zu veraendern.

        condition_1 = raw_data_df["points_scored"] - raw_data_df["points_allowed"] > 3  #Ermittlung Spiele, bei denen Team mehr als 3 Pkt. Vorsprung hatte.
        condition_2 = raw_data_df["points_scored"] - raw_data_df["points_allowed"] < 0

        prepared_data_df["true wins"] = condition_1 | condition_2   #Neue Spalte "true wins" die angibt, ob das Team das Spiel gewonnen hat (True) oder nicht (False).

        st.write(prepared_data_df)                          #DataFrame wird anzeigen.
    return



#Level 4
def provide_decision_support(home_stats, away_stats, home_team, away_team):     #Funktion fuer Level 4. Unterstuetzung der Entscheidung. Uebergabe Teams und Statistiken.
    
    with st.expander("Metrics for Decision"):                                   #Expander Streamlit.
        first_col, second_col = st.columns(2)                                   #Die Anzeige wird in zwei Spalten aufgeteilt.
        home_scoring_rank = home_stats[home_stats.team == home_team].index[0]   #Die durchschnittliche erzielte Punktzahl des Heimteams wird aus den `home_stats` extrahiert.
        home_scoring_mean = home_stats[home_stats["team"] == home_team]["points_scored"].values[0]
        first_col.metric(label="Home Scoring Mean", value=home_scoring_mean)    #Ein Metrik-Widget wird erstellt, um die durchschnittliche erzielte Punktzahl des Heimteams anzuzeigen.

        away_scoring_rank = away_stats[away_stats.team == away_team].index[0]   #Die durchschnittliche erzielte Punktzahl des Auswaertsteams wird aus den `away_stats` extrahiert.
        away_scoring_mean = away_stats[away_stats["team"] == away_team]["points_scored"].values[0]
        second_col.metric(label="Away Scoring Mean", value=away_scoring_mean)   #Metrik-Widget.

        home_allowed_rank = home_stats[home_stats.team == home_team].index[0]   #Die durchschnittlich zugelassene Punktzahl des Heimteams wird aus den `home_stats` extrahiert.
        home_allowed_mean = home_stats[home_stats["team"] == home_team]["points_allowed"].values[0]
        first_col.metric(label="Home Allowed Mean", value=home_allowed_mean)    #Metrik-Widget.

        away_allowed_rank = away_stats[away_stats.team == away_team].index[0]   #Die durchschnittlich zugelassene Punktzahl des Auswaertsteams wird aus den `away_stats` extrahiert.
        away_allowed_mean = away_stats[away_stats["team"] == away_team]["points_allowed"].values[0]
        second_col.metric(label="Away Allowed Mean", value=away_allowed_mean)   #Metrik-Widget.

    return home_scoring_mean, home_allowed_mean, away_scoring_mean, away_allowed_mean #Die durchschnittlichen Punktzahlen fuer Heim- und Auswaertsteams werden zurueckgegeben.



# #Level 5
# def provide_automated_decision(                            #Funktion zur automatischen Entscheidung in Level 5. Supportstatistik und Teams werden uebergeben
    # home_scoring_mean,
    # home_allowed_mean,
    # away_scoring_mean,
    # away_allowed_mean,
    # home_team,
    # away_team,'
# ):
#     with st.expander("Prediction"):                        #Expander in Streamlit "Prediction"
#         home_pred = (home_scoring_mean + away_allowed_mean) / 2 #Die vorhergesagte durchschnittliche Punktzahl des Heimteams wird berechnet.
#         away_pred = (away_scoring_mean + home_allowed_mean) / 2 #Die vorhergesagte durchschnittliche Punktzahl des Auswaertsteams wird berechnet.

#         spread_pred = home_pred - away_pred                 #Punkteunterschied wird vorhergesagt.

#         if spread_pred > 0:                                 #Wenn Punkteunterschied groesser Null gewinnt das Heimteam.
#             winner = home_team
#             spread_pred *= -1                                              

#         else:                                               #Sonst gewinnt das Auswaertsteam.
#             winner = away_team                              
#             spread_pred = spread_pred

#         st.success(f"{winner} wins with a handicap of {spread_pred} points.")   #Erfolgsmeldung mit Bekanntgabe des Gewinners wird erstellt.





def main():                                                     #Main-Funktion.
    
    st.title("NFL-Predictor")                                   #Titel Streamlit = NFL-Predictor.

    response = requests.get(url=ENDPOINT_TEAMS)
    print(response.json())
    teams = response.json()
    
    home_team = st.selectbox(label="Home", options=teams, index=0)
    away_team = st.selectbox(label="Away", options=teams, index=1)

    # Level 1
    provide_raw_data()       #Funktion fuer Level 1 wird aufgrufen

    # # Level 2
    # home_stats, away_stats = provide_derived_data(raw_data_df=raw_data_df) #Funktion fuer Level 2 wird aufgerufen und Statistiken werden in Variabelen gespeichert.

    # # Level 3
    # provide_algorithm(raw_data_df=raw_data_df)                  #Funktion fuer Level 3 wird aufgerufen. Zur Vorhersage werden dem Algorithmus die Rohdaten uebergeben.

    # # Level 4
    # (
    #     home_scoring_mean,
    #     home_allowed_mean,
    #     away_scoring_mean,
    #     away_allowed_mean,
    # ) = provide_decision_support(home_stats, away_stats, home_team, away_team) #Funktion fuer Level 4. Uebergabe der Statistiken und Teams zur Entscheidungshilfe.

    # # Level 5
    # provide_automated_decision(                                 #Funktion fuer Level 5 = Automatisierte Entscheidung basierend auf dem Mittelwert der Teams. Teams und Mittelwerte werden uebergeben.
    #     home_scoring_mean,
    #     home_allowed_mean,
    #     away_scoring_mean,
    #     away_allowed_mean,
    #     home_team,
    #     away_team,
    # )
    return                                                      #Keine Rueckgabe von Variablen

if __name__ == "__main__":                                      #Funktion stellt sicher, dass Main nur ausgefuert wird, wenn Skript direkt ausgefuehrt wird.
    main()
