import streamlit as st
import pandas as pd
from datetime import datetime
from Utils_Coaching import load_data,load_data
from Equipes_Recol import equipe_recolt_page


def recolt_page():
    _, _, df_recolt = load_data()

    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("Filtrer les ventes par période")
        date_debut = st.date_input("Date de début", datetime.today())
        date_fin = st.date_input("Date de fin", datetime.today())
        excel_file = 'Assistance.xlsm'
        df_effectif = pd.read_excel(excel_file, sheet_name='Effectifs')
    with col2:
        if st.button("Afficher les ventes"):
            df_filtered = df_recolt[(df_recolt["Date"] >= pd.to_datetime(date_debut)) & (df_recolt["Date"] <= pd.to_datetime(date_fin))]
            
            if st.session_state.user_info["Statut"] == "Manager":
                team_members = df_effectif[df_effectif["Team"] == st.session_state.user_info["NomP"]]["ID_Citrix"].tolist()
                df_filtered = df_filtered[df_filtered["ID_Citrix"].isin(team_members)]
                
            if not df_filtered.empty:
                st.write(f"Ventes de l'équipe {st.session_state.user_info['NomP']} entre {date_debut} et {date_fin} :")
                st.dataframe(df_filtered)
                csv = df_filtered.to_csv(index=False).encode('utf-8')
                st.download_button("Télécharger en CSV", csv, "ventes.csv", "text/csv")
            else:
                st.warning("Aucune vente trouvée pour cette période.")