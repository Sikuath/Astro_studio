import streamlit as st

from ui.sidebar import show_sidebar
from ui.theme import load_theme
from pathlib import Path

# ==========================
# Configuration
# ==========================
BASE_DIR = Path(__file__).parent

ICON = BASE_DIR / "assets" / "Astro_suite.ico"

st.set_page_config(
    page_title="Astro Prétraitement",
    page_icon=str(ICON),
    layout="wide",
    initial_sidebar_state="expanded"
)



# ==========================
# Initialisation workflow
# ==========================

if "workflow_step" not in st.session_state:

    st.session_state.workflow_step = 1



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
# Sidebar workflow
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
## Assistant de traitement des acquisitions astronomiques

Workflow :

<div class="workflow">

<div class="step">
<div>
<b>📁 Configuration du projet</b><br>
Sélection des dossiers et paramètres Siril
</div>
</div>

<div class="step">

<div>
<b>🔭 Sélection des meilleures acquisitions</b><br>
Tri manuel des Lights
</div>
</div>

<div class="step">

<div>
<b>🗑️ Vérification des rejets</b><br>
Contrôle des images mises de côté
</div>
</div>

<div class="step">

<div>
<b>⚙️ Prétraitement automatique Siril</b><br>
Calibration, alignement et empilement
</div>
</div>

<div class="step">

<div>
<b>✨ Traitement final LRGB / SHO</b><br>
Finalisation de l'image astronomique
</div>
</div>

</div>

<br>

Utilisez les boutons **Continuer ➡️** présents à chaque étape
pour avancer dans le traitement.
""",
unsafe_allow_html=True
)



# ==========================
# Etat workflow
# ==========================

st.divider()



steps = {

    1: "📁 Configuration du projet",

    2: "🔭 Tri des Lights",

    3: "📊 Analyse qualité",

    4: "⚙️ Prétraitement Siril",

    5: "✨ Traitement final"

}



current_step = st.session_state.workflow_step



st.info(
    f"Étape actuelle : {steps[current_step]}"
)



# ==========================
# Projet actif
# ==========================

st.divider()



if "lights_folder" in st.session_state:

    st.success(
        f"📁 Projet actif : {st.session_state['lights_folder']}"
    )


else:

    st.warning(
        "📂 Aucun projet chargé"
    )

# ==========================
# Bouton étape suivante
# ==========================

st.divider()


col1, col2, col3 = st.columns(
    [2,1,2]
)


with col2:

    if st.button(
        "➡️ Commencer",
        use_container_width=True
    ):

        st.session_state.workflow_step = 1

        st.switch_page(
            "pages/01_Project.py"
        )

# ==========================
# Aide
# ==========================

st.caption(
    "🔭 Astro Suite — Workflow astrophotographie"
)