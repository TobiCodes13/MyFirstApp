#Import der benoetigten Bibliotheken
import json
from io import StringIO
import streamlit as st
import pandas as pd
import requests

#URL und Endpunkte für die API
URL = "http://127.0.0.1:8000"
ENDPOINT_DATA = URL+"/level-1/data"
ENDPOINT_TEAMS = URL+"/level-1/teams"
ENDPOINT_STATS = URL+"/level-2/stats"
ENDPOINT_ALGORITHM = URL+"/level-3/algorithm" 
ENDPOINT_DECISION_SUPPORT = URL+"/level-4/decision-support"

#-------------------------------------------------------------------------
#Level 1
def provide_raw_data():                           
    
    response = requests.get(url=ENDPOINT_DATA)      #API-Anfrage, um Rohdaten abzurufen
    raw_data = response.json()

    with st.expander(label="Raw Data"):             #Streamlit Expander für die Anzeige der Rohdaten             
        st.json(raw_data)

    return            

#-------------------------------------------------------------------------
#Level 2
def provide_derived_data():                      
    
    with st.expander(label="Insights"):             #Streamlit Expander für die Anzeige von abgeleiteten Daten
        
        team_types = ["team", "opponent"]           #Liste der Team-Typen
        
        for team_type in team_types:                #Iteration über jeden Team-Typ
            
            if team_type == "team":                 #Label für die Anzeige je nach Team-Typ festlegen
                label = "Home"
            else:
                label = "Away"
                
            st.subheader(f"{label} Insights")       #Streamlit Untertitel für die Anzeige der Statistiken                 
            
            response = requests.get(url=ENDPOINT_STATS, params={"team_type": team_type})    # API-Anfrage, um Statistiken für den aktuellen Team-Typ abzurufen
            raw_data = response.json()
        
            df = pd.read_json(StringIO(raw_data), orient="index")   #Umwandeln der JSON-Daten in ein Pandas DataFrame
            st.write(df)                                            #Anzeige des DataFrames in Streamlit
    return                           

#-------------------------------------------------------------------------
#Level 3
def provide_algorithm():                         
    
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

        response = requests.get(url=ENDPOINT_ALGORITHM)        #API-Anfrage, um die Algorithmus-Daten abzurufen
        algorithm_data = response.json()
        
        algorithm_df = pd.read_json(StringIO(algorithm_data), orient="index")   #JSON-Daten in ein Pandas DataFrame umwandeln
        st.write(algorithm_df)                                 #Anzeige des DataFrames in Streamlit

        
    return

#-------------------------------------------------------------------------
#Level 4

def provide_decision_support(home_team, away_team):
    # Make sure to pass home_team and away_team as query parameters
    response = requests.get(url=ENDPOINT_DECISION_SUPPORT, params={"home_team": home_team, "away_team": away_team})
    decision_support_data = response.json()  # Parse the JSON response

    # Check if the data is a string, and convert it to a dictionary
    if isinstance(decision_support_data, str):
        decision_support_data = json.loads(decision_support_data)

    decision_support_df = pd.DataFrame.from_dict(decision_support_data, orient="index")

    # Reset the index to default integer index
    decision_support_df.reset_index(drop=True, inplace=True)

    with st.expander("Metrics for Decision"):
        st.subheader("Home Team Metrics")
        st.metric(label="Home Scoring Mean", value=decision_support_df.loc[0, "points_scored"])
        st.metric(label="Home Allowed Mean", value=decision_support_df.loc[0, "points_allowed"])

        st.subheader("Away Team Metrics")
        st.metric(label="Away Scoring Mean", value=decision_support_df.loc[1, "points_scored"])
        st.metric(label="Away Allowed Mean", value=decision_support_df.loc[1, "points_allowed"])
    
    return

#-------------------------------------------------------------------------
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

def fetch_teams():
    response = requests.get(url=ENDPOINT_TEAMS)
    return response.json()


def main():                                                     #Main-Funktion.
    
    st.title("NFL-Predictor")

    teams = fetch_teams()

    home_team = st.selectbox(label="Home", options=teams, index=0)
    away_team = st.selectbox(label="Away", options=teams, index=1)

    # Level 1
    provide_raw_data()

    # Level 2
    provide_derived_data()

    # Level 3
    provide_algorithm()

    # Level 4
    provide_decision_support(home_team, away_team) 

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


