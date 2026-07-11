import streamlit as st
from pathlib import Path


from core.config import load_config
from core.session_analyzer import analyze_session
from core.fits_loader import find_fits
from core.fits_metadata import get_fits_metadata


from ui.theme import load_theme
from ui.sidebar import show_sidebar



# =====================================================
# Configuration Streamlit
# =====================================================

st.set_page_config(
    page_title="Prétraitement Siril",
    page_icon="⚙️",
    layout="wide"
)



# =====================================================
# Workflow
# =====================================================

st.session_state.workflow_step = 4



# =====================================================
# Thème + Sidebar
# =====================================================

load_theme()

show_sidebar()



# =====================================================
# Titre
# =====================================================

st.title(
    "⚙️ Prétraitement Siril"
)



# =====================================================
# Chargement configuration
# =====================================================

config = load_config()


lights_folder = config.get(
    "lights_folder",
    ""
)



if not lights_folder:

    st.error(
        "❌ Aucun dossier Lights configuré"
    )

    st.stop()



lights_path = Path(
    lights_folder
)



if not lights_path.exists():

    st.error(
        "❌ Le dossier Lights est introuvable"
    )

    st.stop()



# =====================================================
# Lecture FITS
# =====================================================

target = "Objet inconnu"

camera = "Caméra inconnue"



fits_files = find_fits(
    lights_folder
)



if fits_files:


    metadata = get_fits_metadata(
        fits_files[0]
    )


    target = metadata.get(
        "Objet",
        target
    )


    camera = metadata.get(
        "Caméra",
        camera
    )



# =====================================================
# Analyse session
# =====================================================

if "session_analysis" not in st.session_state:


    with st.spinner(
        "🔎 Analyse automatique des acquisitions..."
    ):


        st.session_state.session_analysis = analyze_session(
            lights_folder
        )



analysis = st.session_state.session_analysis



# =====================================================
# Fallback
# =====================================================

if target in [
    "",
    "Objet inconnu"
]:

    target = analysis.get(
        "target",
        target
    )



if camera in [
    "",
    "Caméra inconnue"
]:

    camera = analysis.get(
        "camera",
        camera
    )



processing_type = analysis.get(
    "type",
    "Inconnu"
)



# =====================================================
# Résumé compact
# =====================================================

st.subheader(
    "🔭 Analyse session"
)



col1, col2, col3 = st.columns(
    3
)



with col1:

    st.caption(
        "🎯 Objet"
    )

    st.write(
        f"**{target}**"
    )



with col2:

    st.caption(
        "📷 Caméra"
    )

    st.write(
        f"**{camera}**"
    )



with col3:

    st.caption(
        "📁 Images"
    )

    st.write(
        f"**{analysis['files']} fichiers**"
    )



# =====================================================
# Filtres
# =====================================================

st.divider()


st.subheader(
    "🎨 Filtres détectés"
)



filters = analysis.get(
    "filters",
    {}
)



if filters:


    txt = "   ".join(
        [
            f"**{f}** : {n}"
            for f, n in sorted(filters.items())
        ]
    )


    st.info(
        txt
    )


else:

    st.warning(
        "⚠️ Aucun filtre détecté"
    )



# =====================================================
# Pipeline choisi
# =====================================================

st.divider()


st.subheader(
    "🧠 Pipeline sélectionné"
)



if processing_type == "SHO":


    st.success(
        "🌈 SHO détecté → Hα + OIII + SII"
    )



elif processing_type == "LSHO":


    st.success(
        "🌈 LSHO détecté → L + Hα + OIII + SII"
    )



elif processing_type == "LRGB":


    st.success(
        "🎨 LRGB détecté → L + R + G + B"
    )



else:


    st.warning(
        "⚠️ Impossible de déterminer le traitement"
    )



# =====================================================
# Validation
# =====================================================

st.divider()


st.subheader(
    "🚀 Validation"
)



st.write(
    f"""
Le pipeline suivant sera préparé :

🎯 **{target}**

🎨 **{processing_type}**

📷 **{camera}**

📁 **{analysis['files']} images**
"""
)



col1, col2, col3 = st.columns(
    [2,1,2]
)



with col2:


    if st.button(
        "🚀 Lancer Siril",
        use_container_width=True
    ):


        if processing_type == "Inconnu":


            st.error(
                "❌ Type de traitement inconnu"
            )


        else:


            st.session_state.workflow_step = 5


            st.switch_page(
                "pages/05_Traitement.py"
            )



# =====================================================
# Informations techniques
# =====================================================

with st.expander(
    "🔎 Informations techniques"
):


    st.json(
        {
            **analysis,
            "target_header": target,
            "camera_header": camera
        }
    )



# =====================================================
# Pied de page
# =====================================================

st.caption(
    "📁 Projet → 🔭 Preview → 🗑️ Check → ⚙️ Prétraitement → 🖥️ Siril"
)