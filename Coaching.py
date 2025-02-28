import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
from PIL import Image
from datetime import datetime
#from Equipes import Equipe_Recolt
#from Utils_Coaching import *

import streamlit as st

def coaching_page():
    st.title("Page de Coaching")
    st.write("Contenu de la page de coaching...")

# 📂 Chargement des données utilisateurs (authentification)
excel_file = 'Assistance.xlsm'

try:
    # Charger les données des utilisateurs, des effectifs et des récolts
    df_users = pd.read_excel(excel_file, sheet_name='Users')
    df_effectif = pd.read_excel(excel_file, sheet_name='Effectifs')
    df_recolt = pd.read_excel(excel_file, sheet_name='Recolt')
    
    # Convertir la colonne Date au format datetime
    df_recolt["Date"] = pd.to_datetime(df_recolt["Date"], errors='coerce')
    df_recolt.dropna(subset=["Date"], inplace=True)
except Exception as e:
    st.error(f"Erreur lors du chargement du fichier Excel : {e}")
    st.stop()

# Vérification des colonnes attendues
required_columns_users = {"Login", "Password", "ID_Citrix"}
required_columns_effectif = {"ID_Citrix", "Nom_Prenom", "Statut", "Team"}
required_columns_recolt = {"Banque", "Ville", "Departement", "TRANSACTION_AMOUNT", "SHORT_MESSAGE", "ID_Citrix", "Sinistre/contrat", "Date", "Moi", "Jour", "Heure"}

for sheet, cols, df in zip(["Users", "Effectifs", "Recolt"],
                           [required_columns_users, required_columns_effectif, required_columns_recolt],
                           [df_users, df_effectif, df_recolt]):
    if not cols.issubset(df.columns):
        st.error(f"La feuille '{sheet}' doit contenir les colonnes {cols} !")
        st.stop()

# Nettoyage des données
df_users.dropna(inplace=True)
df_effectif.dropna(inplace=True)
df_recolt.dropna(inplace=True)

# 🎨 Initialisation de l'état de session
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_info" not in st.session_state:
    st.session_state.user_info = None

# 🎨 Interface de connexion
col1, col2 = st.columns([1, 2])

with col1:
    st.image("Images/Logo_Axa_Noir.png", width=280)

with col2:
    st.subheader("🔐 Page de connexion")
    
    if not st.session_state.logged_in:
        login = st.text_input("Nom d'utilisateur : ")
        password = st.text_input("Mot de passe :", type="password")
        
        if st.button("Se connecter"):
            user = df_users[(df_users["Login"] == login) & (df_users["Password"] == password)]
            if not user.empty:
                id_citrix = user["ID_Citrix"].values[0]
                user_info = df_effectif[df_effectif["ID_Citrix"] == id_citrix]
                
                if not user_info.empty:
                    st.session_state.logged_in = True
                    st.session_state.user_info = {
                        "NomP": user_info["Nom_Prenom"].values[0],
                        "Statut": user_info["Statut"].values[0],
                        "Team": user_info["Nom_Prenom"].values[0]  # Changer la Team pour correspondre au Nom_Prenom du Manager
                    }
                    st.success(f"Connexion réussie ! Bienvenue, {login}")
                else:
                    st.error("Impossible de récupérer les informations de l'utilisateur.")
            else:
                st.error("Nom d'utilisateur ou mot de passe incorrect !")
    else:
        st.success(f"Vous êtes connecté en tant que {st.session_state.user_info['NomP']}")

# 🔄 Affichage du menu et du contenu
if st.session_state.logged_in:
    NomP = st.session_state.user_info["NomP"]
    Statut = st.session_state.user_info["Statut"]
    Team = st.session_state.user_info["Team"]

    #with st.sidebar:
    st.markdown(f"<h2 style='color: white;'>Bienvenue, <strong>{NomP}</strong>!</h2>", unsafe_allow_html=True)
        
    menu_items = ["Coachings", "Recolt"] if Statut == "Agent" else ["Coaching", "Équipe", "Recolt"]
    selected = option_menu(f"Menu {NomP}", menu_items, icons=["calendar", "list-task", "calendar-event"], menu_icon="menu")

    if selected == "Recolt":
        col1, col2 = st.columns([1, 2])
        Equipe_Recolt()
        with col1:
            st.subheader("Filtrer les ventes par période")
            date_debut = st.date_input("Date de début", datetime.today())
            date_fin = st.date_input("Date de fin", datetime.today())
        with col2:
            if st.button("Afficher les ventes"):

                
                    df_filtered = df_recolt[(df_recolt["Date"] >= pd.to_datetime(date_debut)) & (df_recolt["Date"] <= pd.to_datetime(date_fin))]
            
            if Statut == "Manager":
                    team_members = df_effectif[df_effectif["Team"] == NomP]["ID_Citrix"].tolist()
                    df_filtered = df_filtered[df_filtered["ID_Citrix"].isin(team_members)]
                    
                
            if not df_filtered.empty:
                    st.write(f"Ventes de l'équipe {NomP} entre {date_debut} et {date_fin} :")
                    st.dataframe(df_filtered)
                    csv = df_filtered.to_csv(index=False).encode('utf-8')
                    st.download_button("Télécharger en CSV", csv, "ventes.csv", "text/csv")
            else:
                    st.warning("Aucune vente trouvée pour cette période.")

    if st.sidebar.button("Se déconnecter"):
        st.session_state.logged_in = False
        st.session_state.user_info = None
        st.rerun()
