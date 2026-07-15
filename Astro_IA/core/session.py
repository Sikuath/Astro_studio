import streamlit as st


# ==========================================================
# INITIALISATION DE LA SESSION
# ==========================================================

def init_session(config):
    """
    Initialise toutes les variables de session utilisées
    dans Astro IA.
    """

    defaults = {

        # --------------------------------------------------
        # Configuration
        # --------------------------------------------------

        "config": config,

        "config_validated": False,

        # --------------------------------------------------
        # Workflow
        # --------------------------------------------------

        "analysis_ready": False,
        "fits_loaded": False,
        "report_ready": False,

        # --------------------------------------------------
        # Fichiers
        # --------------------------------------------------

        "image_path": "",
        "image_name": "",

        "fits_path": "",

        # --------------------------------------------------
        # Données FITS
        # --------------------------------------------------

        "fits_header": {},

        # --------------------------------------------------
        # Résultat IA
        # --------------------------------------------------

        "analysis_result": "",

        # --------------------------------------------------
        # Session Astro
        # --------------------------------------------------

        "instrument": "",
        "camera": "",
        "object": "",

        # --------------------------------------------------
        # Workflow Siril / GIMP
        # --------------------------------------------------

        "siril_workflow": "",
        "gimp_workflow": "",

        # --------------------------------------------------
        # Rapport
        # --------------------------------------------------

        "report_text": ""

    }

    for key, value in defaults.items():

        if key not in st.session_state:

            st.session_state[key] = value