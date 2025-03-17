import streamlit as st
from streamlit_option_menu import option_menu
from Login import login_page
#from Coaching import coaching_page
from Recolt import recolt_page
from Equipes_Recol import *

def coaching_page():
    st.title("Page de Coaching")
    st.write("Contenu de la page de coaching...")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_info" not in st.session_state:
    st.session_state.user_info = None


if not st.session_state.logged_in:
    login_page()
else:
    # Affichage du menu vertical
    with st.sidebar:
        st.markdown(f"<h2 style='color: white;'>Bienvenue, <strong>{st.session_state.user_info['NomP']}</strong>!</h2>", unsafe_allow_html=True)
        
        menu_items = ["Coachings", "Recolt"] if st.session_state.user_info["Statut"] == "Agent" else ["Coaching", "Équipe", "Recolt"]
        selected = option_menu(
            "Menu", 
            menu_items, 
            icons=["calendar", "list-task", "calendar-event"], 
            menu_icon="menu"
        )
        date_debut = st.date_input("Date de début", datetime.today())
        date_fin = st.date_input("Date de fin", datetime.today())


    # Affichage de la page sélectionnée
    if selected == "Coaching":
        coaching_page()
    elif selected == "Équipe":
        equipe_recolt_page()
    elif selected == "Recolt":
        recolt_page()

    # Bouton de déconnexion
    if st.sidebar.button("Se déconnecter"):
        st.session_state.logged_in = False
        st.session_state.user_info = None
        st.rerun()
