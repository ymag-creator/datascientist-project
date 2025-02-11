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
# postcode_district
postcode_district = pd.read_csv(os.path.join(path, "postcode_district.csv"))
print(postcode_district.columns)
if "select_postcode_district" not in st.session_state:
    # st.session_state.select_postcode_district = postcode_district.iloc[0][0]
    st.session_state.select_postcode_district = 0
    print("-----st.session_state.select_postcode_district", st.session_state.select_postcode_district)
select_postcode_district = st.selectbox("Choisissez un Code Post District :", postcode_district, index=int(st.session_state.select_postcode_district))

# property_type
property_type = pd.read_csv(os.path.join(path, "property_type.csv"))
if "select_property_type" not in st.session_state:
    # st.session_state.select_postcode_district = postcode_district.iloc[0][0]
    st.session_state.select_property_type = 0
    print("-----st.session_state.select_property_type", st.session_state.select_property_type)
select_property_type = st.selectbox("Choisissez un Type de Propriété :", property_type, index=int(st.session_state.select_property_type))

# stop_code
stop_code = pd.read_csv(os.path.join(path, "stop_code.csv"))
if "select_stop_code" not in st.session_state:
    # st.session_state.select_postcode_district = postcode_district.iloc[0][0]
    st.session_state.select_stop_code = 0
    print("-----st.session_state.select_property_type", st.session_state.select_stop_code)
select_stop_code = st.selectbox("Choisissez un Type d'incident :", stop_code, index=int(st.session_state.select_stop_code))

rowDateTime = st.columns([1, 1])
# select_date
if "select_date" not in st.session_state:
    # st.session_state.select_postcode_district = postcode_district.iloc[0][0]
    st.session_state.select_date = date.today()
    print("-----st.session_state.select_property_type", st.session_state.select_date)
select_date = rowDateTime[0].container(height=100).date_input("Choisissez une date", st.session_state.select_date, format="DD/MM/YYYY")
# select_time
if "select_time" not in st.session_state:
    # st.session_state.select_postcode_district = postcode_district.iloc[0][0]
    st.session_state.select_time = datetime.now()
    print("-----st.session_state.select_property_type", st.session_state.select_date)
select_time = rowDateTime[1].container(height=100).time_input("Choisissez l'heure", st.session_state.select_time)

# Crée le dataframe de prédiction
st.write("Dataframe")
df = model.create_dataframe(select_date.year, select_time.hour, select_property_type, select_postcode_district,
                            select_stop_code, select_date.month, select_date.weekday() + 1)
st.dataframe(df.head(10))


# Fonction pour changer la valeur de la selectbox
def change_postcode_district(new_postcode_district, refresh=True):
    st.session_state.select_postcode_district = int(
        postcode_district[postcode_district["0"] == new_postcode_district].index[0]
    )
    # st.session_state.select_postcode_district = 16
    print(st.session_state.select_postcode_district)
    # st.rerun()   # Recharger l'interface avec la nouvelle valeur sélectionnée
    if refresh:
        st.rerun()


# Fonction pour changer la valeur de la selectbox
def change_incident(new_property_type, new_stop_code, refresh=True):
    # select_property_type = "RAILWAY TRACKSIDE VEGETATION"
    # st.session_state.select_postcode_district = "CR44"
    st.session_state.select_property_type = int(
        property_type[property_type["0"] == new_property_type].index[0]
    )
    st.session_state.select_stop_code = int(
        stop_code[stop_code["0"] == new_stop_code].index[0]
    )
    # st.session_state.select_postcode_district = 16
    print(st.session_state.select_postcode_district)
    # st.rerun()   # Recharger l'interface avec la nouvelle valeur sélectionnée
    if(refresh):
        st.rerun()


def change_date(date, refresh=True):
    # select_property_type = "RAILWAY TRACKSIDE VEGETATION"
    # st.session_state.select_postcode_district = "CR44"
    st.session_state.select_date = date
    # st.session_state.select_postcode_district = 16
    print(st.session_state.select_date)
    # st.rerun()   # Recharger l'interface avec la nouvelle valeur sélectionnée
    if(refresh):
        st.rerun()


def change_time(time, refresh=True):
    # select_property_type = "RAILWAY TRACKSIDE VEGETATION"
    # st.session_state.select_postcode_district = "CR44"
    st.session_state.select_time = time
    # st.session_state.select_postcode_district = 16
    print(st.session_state.select_time)
    # st.rerun()   # Recharger l'interface avec la nouvelle valeur sélectionnée
    if(refresh):
        st.rerun()

st.write("Exemples ")

rowButtons = st.columns([1, 1])
c11 = rowButtons[0].container(height=170)
c12 = rowButtons[1].container(height=170)

if c11.button("1 RAILWAY TRACKSIDE VEGETATION / PRIMARY FIRE "):
    change_incident("RAILWAY TRACKSIDE VEGETATION","PRIMARY FIRE")
if c12.button("2 HOUSE - SINGLE OCCUPANCY / CHIMNEY FIRE "):
    change_incident("HOUSE - SINGLE OCCUPANCY", "CHIMNEY FIRE")
if c11.button("3 BULK WASTE STORAGE / SST-LIFT RELEASE"):
    change_incident("BULK WASTE STORAGE", "SST-LIFT RELEASE")
if c12.button("4  BULK WASTE STORAGE / ALARM "):
    change_incident("BULK WASTE STORAGE", "ALARM")
if st.button("5 VEHICLE REPAIR WORKSHOP / ALARM"):
    change_incident("VEHICLE REPAIR WORKSHOP", "ALARM")

rowButtons2 = st.columns([1, 1, 1, 1])
c21 = rowButtons2[0].container(height=170)
c22 = rowButtons2[1].container(height=170)
c23 = rowButtons2[2].container(height=170)
c24 = rowButtons2[3].container(height=170)

if c21.button("BR1"):
    change_postcode_district("BR1")
if c22.button("CR5"):
    change_postcode_district("CR5")

if c23.button("Samedi"):
    change_date(date(2025, 2, 22))
if c24.button("Aujourd'hui"):
    change_date(date(2025, 2, 18))

if c21.button("0h30"):
    change_time(datetime(2025, 2, 22, 0, 30))
if c22.button("7h30"):
    change_time(datetime(2025, 2, 22, 7, 30))

if c23.button("BR8 à 17h30"):
    change_time(datetime(2025, 2, 22, 17, 30), False)
    change_postcode_district("BR8")


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
st.header("Ask To Zoltar")
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
