import streamlit as st
import pandas as pd
from Utils_Coaching import load_data

def login_page():
    df_users, df_effectif, _ = load_data()

    col1, col2 = st.columns([1, 2])

    with col1:
        st.image("Images/Logo_Axa_Noir.png", width=280)

    with col2:
        st.subheader("🔐 Page de connexion")
        
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