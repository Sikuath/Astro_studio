import streamlit as st
import time

from core.fits_loader import find_fits
from core.preview import fits_preview
from core.reject import reject_file
from core.config import load_config
from core.fits_metadata import get_fits_metadata

from streamlit_shortcuts import shortcut_button

from ui.theme import load_theme
from ui.sidebar import show_sidebar



# ==========================
# Configuration page
# ==========================

st.set_page_config(
    page_title="Astro Preview",
    page_icon="🔭",
    layout="wide"
)



# ==========================
# Workflow étape 2
# ==========================

st.session_state.workflow_step = 2



# ==========================
# Thème + Sidebar
# ==========================

load_theme()

show_sidebar()



# ==========================
# Titre
# ==========================

st.title(
    "🔭 Preview Lights"
)



# ==========================
# Chargement configuration
# ==========================

if "rejected_folder" not in st.session_state:

    config = load_config()

    st.session_state["rejected_folder"] = config.get(
        "rejected_folder",
        ""
    )



# ==========================
# Vérification projet
# ==========================

if "lights_folder" not in st.session_state:

    st.warning(
        "⚠️ Choisissez d'abord un projet"
    )

    st.stop()



files = find_fits(
    st.session_state["lights_folder"]
)



if not files:

    st.error(
        "❌ Aucun fichier FITS trouvé"
    )

    st.stop()



# ==========================
# Session
# ==========================

if "index" not in st.session_state:

    st.session_state.index = 0



if "reject_count" not in st.session_state:

    st.session_state.reject_count = 0



if "reject_requested" not in st.session_state:

    st.session_state.reject_requested = False



if "last_action_time" not in st.session_state:

    st.session_state.last_action_time = 0



# ==========================
# Anti répétition clavier
# ==========================

def can_execute(delay=0.3):

    now = time.time()

    if now - st.session_state.last_action_time < delay:

        return False


    st.session_state.last_action_time = now

    return True



# ==========================
# Sécurité index
# ==========================

st.session_state.index = max(
    0,
    min(
        st.session_state.index,
        len(files)-1
    )
)



current = files[
    st.session_state.index
]



# ==========================
# Traitement rejet
# ==========================

if st.session_state.get(
    "reject_requested",
    False
):

    reject_file(
        current,
        st.session_state["rejected_folder"]
    )


    st.session_state.reject_count += 1


    st.session_state.reject_requested = False


    files = find_fits(
        st.session_state["lights_folder"]
    )


    if files:

        st.session_state.index = min(
            st.session_state.index,
            len(files)-1
        )


    st.rerun()



# ==========================
# Actions
# ==========================

def previous():

    st.session_state.index = max(
        0,
        st.session_state.index - 1
    )



def next_image():

    st.session_state.index = min(
        len(files)-1,
        st.session_state.index + 1
    )



def reject_action():

    if can_execute(0.8):

        st.session_state.reject_requested = True



# ==========================
# En-tête
# ==========================

col_a, col_b = st.columns(
    [4,1]
)



with col_a:

    st.subheader(
        current.name
    )



with col_b:

    st.metric(
        "🗑️ Rejets",
        st.session_state.reject_count
    )



# ==========================
# Navigation compacte
# ==========================

nav1, trash, nav2 = st.columns(
    [1,1,1]
)



with nav1:

    if shortcut_button(
        "⬅️",
        "ArrowLeft"
    ):

        if can_execute():

            previous()

            st.rerun()



with trash:

    shortcut_button(
        "🗑️",
        "ArrowUp",
        on_click=reject_action
    )



with nav2:

    if shortcut_button(
        "➡️",
        "ArrowRight"
    ):

        if can_execute():

            next_image()

            st.rerun()



# ==========================
# Image + Métadonnées
# ==========================

image = fits_preview(
    current
)



if image:


    col_img, col_meta = st.columns(
        [3,1]
    )


    with col_img:

        st.image(
            image,
            width=800
        )



    with col_meta:

        st.subheader(
            "📋 FITS"
        )


        metadata = get_fits_metadata(
            current
        )


        if metadata:


            st.markdown(
                """
                <div style="
                background: rgba(0,0,0,0.25);
                padding:12px;
                border-radius:12px;
                ">
                """,
                unsafe_allow_html=True
            )


            for key, value in metadata.items():

                st.markdown(
                    f"**{key} :** {value}"
                )


            st.markdown(
                "</div>",
                unsafe_allow_html=True
            )


        else:

            st.info(
                "Aucune métadonnée"
            )



# ==========================
# Informations
# ==========================

info1, info2 = st.columns(2)



with info1:

    st.info(
        f"📷 Image {st.session_state.index + 1} / {len(files)}"
    )



with info2:

    st.success(
        f"📂 Lights restants : {len(files)}"
    )



# ==========================
# Actions principales
# ==========================

st.divider()


action1, action2 = st.columns(
    [1,1]
)



with action1:

    if st.button(
        "🗑️ Rejeter cette image"
    ):

        reject_action()



with action2:

    if st.button(
        "➡️ Contrôle final des rejets"
    ):

        st.session_state.workflow_step = 3

        st.switch_page(
            "pages/03_Check.py"
        )



# ==========================
# Aide
# ==========================

st.caption(
    "⬅️ précédent   |   ➡️ suivant   |   ⬆️ rejeter"
)