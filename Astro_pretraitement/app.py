import streamlit as st

from ui.sidebar import show_sidebar
from ui.theme import load_theme



# ==========================
# Configuration
# ==========================

st.set_page_config(
    page_title="Astro Prétraitement",
    page_icon="📷",
    layout="wide",
    initial_sidebar_state="expanded"
)



# ==========================
# Masquer navigation native Streamlit
# ==========================

st.markdown(
    """
    <style>

    [data-testid="stSidebarNav"] {
        display: none;
    }

    </style>
    """,
    unsafe_allow_html=True
)



# ==========================
# Thème graphique
# ==========================

load_theme()



# ==========================
# Sidebar personnalisée
# ==========================

show_sidebar()



# ==========================
# Accueil
# ==========================

st.title(
    "📷 Astro Prétraitement"
)



st.markdown(
    """
## Assistant de tri des acquisitions astronomiques


Cette application permet :

- 🔭 visualisation rapide des lights FITS
- 🗑️ suppression des mauvaises acquisitions
- ⚙️ lancement du prétraitement Siril
- 🧪 préparation des couches LRGB / SHO


---

Commencez par choisir un projet dans le menu de gauche.
"""
)



# ==========================
# Projet actif
# ==========================

if "lights_folder" in st.session_state:

    st.success(
        f"📁 Projet actif : {st.session_state['lights_folder']}"
    )


else:

    st.info(
        "Aucun projet chargé"
    )