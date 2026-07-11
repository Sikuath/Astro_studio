import streamlit as st
from pathlib import Path

from core.config import load_config, save_config
from core.reject import clear_rejected_folder

from ui.theme import load_theme
from ui.sidebar import show_sidebar



# ==========================
# Configuration Streamlit
# ==========================

st.set_page_config(
    page_title="Projet Astro",
    page_icon="📁",
    layout="wide"
)



# ==========================
# Initialisation workflow
# ==========================

if "workflow_step" not in st.session_state:

    st.session_state.workflow_step = 1



# ==========================
# Thème + Sidebar
# ==========================

load_theme()

show_sidebar()



# ==========================
# Titre
# ==========================

st.title(
    "📁 Projet"
)



# ==========================
# Chargement configuration
# ==========================

config = load_config()



lights_current = config.get(
    "lights_folder",
    ""
)


rejected_current = config.get(
    "rejected_folder",
    ""
)


siril_current = config.get(
    "siril_path",
    r"C:\Program Files\Siril\bin\siril-cli.exe"
)



# ==========================
# Dossiers
# ==========================

st.subheader(
    "📂 Dossiers du projet"
)



lights_folder = st.text_input(
    "📷 Dossier des Lights",
    value=lights_current
)



rejected_folder = st.text_input(
    "🗑️ Dossier des rejets",
    value=rejected_current
)



# ==========================
# Siril CLI
# ==========================

st.divider()


st.subheader(
    "🔭 Configuration Siril"
)



siril_path = st.text_input(
    "⚙️ Exécutable Siril CLI",
    value=siril_current
)



siril_file = Path(
    siril_path
)



if siril_file.exists():

    if "siril-cli" in siril_file.name.lower():

        st.success(
            "✅ Siril CLI détecté"
        )

    else:

        st.warning(
            """
⚠️ Ce fichier n'est pas Siril CLI.

Utilisez :

C:\\Program Files\\Siril\\bin\\siril-cli.exe
"""
        )


else:

    st.error(
        "❌ Siril CLI introuvable"
    )



# ==========================
# Sauvegarde configuration
# ==========================

st.divider()



configuration_ok = False



if st.button(
    "💾 Enregistrer configuration",
    use_container_width=True
):


    lights_path = Path(
        lights_folder
    )


    rejected_path = Path(
        rejected_folder
    )


    siril_file = Path(
        siril_path
    )



    if not lights_path.exists():

        st.error(
            "❌ Le dossier Lights n'existe pas"
        )



    elif not siril_file.exists():

        st.error(
            "❌ Siril CLI introuvable"
        )



    elif "siril-cli" not in siril_file.name.lower():

        st.error(
            "❌ Utilisez siril-cli.exe et non siril.exe"
        )



    else:


        if not rejected_path.exists():

            rejected_path.mkdir(
                parents=True,
                exist_ok=True
            )



        config["lights_folder"] = lights_folder

        config["rejected_folder"] = rejected_folder

        config["siril_path"] = siril_path



        save_config(
            config
        )



        st.session_state["lights_folder"] = lights_folder

        st.session_state["rejected_folder"] = rejected_folder

        st.session_state["siril_path"] = siril_path



        st.session_state.workflow_step = 1



        configuration_ok = True



        st.success(
            "✅ Configuration sauvegardée"
        )



# ==========================
# Passage étape suivante
# ==========================

if (
    configuration_ok
    or
    (
        "lights_folder" in st.session_state
        and st.session_state.workflow_step == 1
    )
):


    st.divider()


    if st.button(
        "➡️ Continuer vers Preview Lights",
        use_container_width=True
    ):


        st.session_state.workflow_step = 2


        st.success(
            "🔭 Passage à l'étape Preview Lights"
        )


        st.switch_page(
            "pages/02_Preview.py"
        )



# ==========================
# Gestion des rejets
# ==========================

st.divider()



st.subheader(
    "🧹 Gestion des rejets"
)



if rejected_folder:


    rejected_path = Path(
        rejected_folder
    )


    if rejected_path.exists():


        if "confirm_clear_rejected" not in st.session_state:

            st.session_state.confirm_clear_rejected = False



        if st.button(
            "🗑️ Vider le dossier des rejets",
            use_container_width=True
        ):

            st.session_state.confirm_clear_rejected = True



        if st.session_state.confirm_clear_rejected:


            st.warning(
                """
⚠️ Attention :

Cette action supprimera définitivement
toutes les images du dossier des rejets.

Êtes-vous certain ?
"""
            )



            col1, col2 = st.columns(2)



            with col1:

                if st.button(
                    "✅ Oui, vider",
                    use_container_width=True
                ):


                    clear_rejected_folder(
                        rejected_folder
                    )


                    st.session_state.confirm_clear_rejected = False


                    st.success(
                        "✅ Dossier des rejets vidé"
                    )


                    st.rerun()



            with col2:

                if st.button(
                    "❌ Annuler",
                    use_container_width=True
                ):


                    st.session_state.confirm_clear_rejected = False


                    st.rerun()



    else:

        st.info(
            "ℹ️ Le dossier des rejets sera créé automatiquement"
        )



else:

    st.info(
        "ℹ️ Choisissez un dossier de rejets"
    )