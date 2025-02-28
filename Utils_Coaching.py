
import streamlit as st
import pandas as pd




def load_data():
    excel_file = 'Assistance.xlsm'
    try:
        df_users = pd.read_excel(excel_file, sheet_name='Users')
        df_effectif = pd.read_excel(excel_file, sheet_name='Effectifs')
        df_recolt = pd.read_excel(excel_file, sheet_name='Recolt')
        
        df_recolt["Date"] = pd.to_datetime(df_recolt["Date"], errors='coerce')
        df_recolt.dropna(subset=["Date"], inplace=True)
        
        return df_users, df_effectif, df_recolt
    except Exception as e:
        st.error(f"Erreur lors du chargement du fichier Excel : {e}")
        st.stop()