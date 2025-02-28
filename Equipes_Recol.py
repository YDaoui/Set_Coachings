import streamlit as st
import pandas as pd
from datetime import datetime
from Utils_Coaching import load_data

def equipe_recolt_page():
    _, df_effectif, df_recolt = load_data()

    if st.session_state.logged_in:
        NomP = st.session_state.user_info["NomP"]
        Statut = st.session_state.user_info["Statut"]

    st.title("Gestion de l'Équipe et des Récoltes")
    date_debut = st.date_input("Date de début", datetime.today())
    date_fin = st.date_input("Date de fin", datetime.today())

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