import streamlit as st
import pandas as pd
from datetime import datetime, date

import os
import sys

# Obtenir le chemin absolu du répertoire parent
dir_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
# Ajouter le chemin à sys.path, sinon PredictModel n'est pas trouvé en run
if dir_path not in sys.path:
    sys.path.append(dir_path)
from models.predict_model import PredictModel

# vérifie les chemins
print("Répertoire courant:", os.getcwd())  # Vérifie si Streamlit tourne bien depuis le bon dossier
print("sys.path:", sys.path)  # Vérifie les chemins de recherche des modules
# Stock le chemin des fichiers du streamlit
path = os.path.dirname(__file__)
print("----path", path)

# Charge la classe du model
model = PredictModel()

# En tête
st.image(os.path.join(path, "lfb.png"), width=200)
st.title("Temps de Réponse de la Brigade des Pompiers de Londres")
# st.sidebar.title("Sommaire")
st.image(os.path.join(path, "districts copie.jpg"), use_container_width=True)

# Champs de saisie
postcode_district = pd.read_csv(os.path.join(path, "postcode_district.csv"))
select_postcode_district = st.selectbox("Choisissez un Code Post District :", postcode_district)

property_type = pd.read_csv(os.path.join(path, "property_type.csv"))
select_property_type = st.selectbox("Choisissez un Type de Propriété :", property_type)

stop_code = pd.read_csv(os.path.join(path, "stop_code.csv"))
select_stop_code = st.selectbox("Choisissez un Type d'incident :", stop_code)

select_date = st.date_input("Choisissez une date", date.today(), format="DD/MM/YYYY")

select_time = st.time_input("Choisissez l'heure", datetime.now())

# Crée le dataframe de prédiction
st.write("Dataframe")
df = model.create_dataframe(select_date.year, select_time.hour, select_property_type, select_postcode_district,
                            select_stop_code, select_date.month, select_date.weekday() + 1)
st.dataframe(df.head(10))


def format_seconds(seconds):
    """Formatage intelligent des secondes

    Args:
        seconds (_type_): Temps en secondes à formater

    Returns:
        _type_: un temps formaté
    """
    # si moins d'une minute, retoune le temps en secondes
    if seconds < 60:
        return f"{round(seconds)} sec"
    # converti en minutes
    minutes, sec = divmod(seconds, 60)
    # si moins d'une heure, retourne le temps en minutes et secondes
    if minutes < 60:
        return f"{round(minutes)} min {round(sec)} sec"
    # si plus d'une heure, retourne le temps en heures, minutes et secondes
    hours, minutes = divmod(minutes, 60)
    return f"{round(hours)} h {round(minutes)} min {round(sec)} sec"

# Prédiction
st.header("Les prédictions de Zoltar")
# Colonne 1 pour l'image
row1 = st.columns([1,2])
col1 = row1[0].container(height=600)
col1.image(os.path.join(path, "Zoltar.jpg"), width=280)
# Colonne 2 pour les prédictions
col2 = row1[1].container(height=600)
result = model.predict(df)
result_df = pd.DataFrame(result)
# Renomme les colonnes pour une meilleure lisibilité
new_names = {"TurnoutTimeSeconds_min": "Temps de préparation minimum",
    "TurnoutTimeSeconds_mean": "Temps de préparation median",
    "TurnoutTimeSeconds_max": "Temps de préparation maximum",
    "TravelTimeSeconds_min": "Temps de trajet minimum",
    "TravelTimeSeconds_mean": "Temps de trajet median",
    "TravelTimeSeconds_max": "Temps de trajet maximum",
    "PumpSecondsOnSite_min": "Temps sur site minimum",
    "PumpSecondsOnSite_mean": "Temps sur site median",
    "PumpSecondsOnSite_max": "Temps sur site maximum"}
result_df = result_df.rename(new_names, axis = 1)
# Dupliquez la 1ere ligne et formate les temps
result_df = pd.concat([result_df.iloc[[0]], result_df], ignore_index=True)
result_df.iloc[0] = result_df.iloc[0].apply(format_seconds)
# Affiche les prédictions dasn un DF
col2.write("Prédictions (en secondes)")
col2.dataframe(result_df.T.rename({0:"Temps", 1:"Secondes"}, axis = 1))
