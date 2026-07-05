import streamlit as st
from core.config import load_config, save_config

def sidebar_project():

    config = load_config()

    workdir = st.sidebar.text_input(
        "Dossier de travail",
        value=config.get("workdir", "")
    )

    siril = st.sidebar.text_input(
        "Chemin Siril",
        value=config.get("siril_path", "")
    )

    # 🔥 IMPORTANT : push vers session_state
    st.session_state["workdir"] = workdir
    st.session_state["siril"] = siril

    # sauvegarde disque
    if workdir != config.get("workdir") or siril != config.get("siril_path"):
        config["workdir"] = workdir
        config["siril_path"] = siril
        save_config(config)

    st.sidebar.markdown("---")
    st.sidebar.write("Projet actif :")
    st.sidebar.code(workdir if workdir else "Aucun")