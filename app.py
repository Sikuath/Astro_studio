import streamlit as st
from tools import sho_mixer
from ui.project import sidebar_project

st.set_page_config(layout="wide")

sidebar_project()

page = st.sidebar.radio(
    "Modules",
    ["🏠 Projet", "🌈 SHO Mixer"]
)

if page == "🏠 Projet":
    st.title("Projet")

elif page == "🌈 SHO Mixer":
    sho_mixer.run()

# =========================
# MAIN AREA
# =========================

if page == "🏠 Projet":

    col1, col2 = st.columns([2, 1])

    with col1:
        st.title("📁 Projet SHO Studio")
        st.write("Configure ton dossier dans la sidebar.")

    with col2:
        st.info("💡 Astuce\n\nPlace tes fichiers SII / HA / OIII dans un même dossier.")

