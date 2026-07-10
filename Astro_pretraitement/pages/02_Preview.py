import streamlit as st
import time

from core.fits_loader import find_fits
from core.preview import fits_preview
from core.reject import reject_file
from core.config import load_config

from streamlit_shortcuts import shortcut_button


# ==========================
# Configuration page
# ==========================

st.set_page_config(
    page_title="Astro Preview",
    page_icon="🔭",
    layout="wide"
)


st.title("🔭 Preview Lights")


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
        "Choisissez d'abord un projet"
    )

    st.stop()



files = find_fits(
    st.session_state["lights_folder"]
)



if not files:

    st.error(
        "Aucun fichier FITS trouvé"
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
# Anti répétition
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
# Navigation clavier
# ==========================

nav1, trash, nav2 = st.columns(
    [1,1,1]
)



with nav1:

    if shortcut_button(
        "⬅️ Précédente",
        "ArrowLeft"
    ):

        if can_execute():

            previous()

            st.rerun()



with trash:

    shortcut_button(
        "⬆️ Rejeter",
        "ArrowUp",
        on_click=reject_action
    )



with nav2:

    if shortcut_button(
        "Suivante ➡️",
        "ArrowRight"
    ):

        if can_execute():

            next_image()

            st.rerun()



# ==========================
# Image
# ==========================

image = fits_preview(
    current
)



if image:

    st.image(
        image,
        width=800
    )



# ==========================
# Bouton souris
# ==========================

st.divider()


if st.button(
    "🗑️ Rejeter cette image",
    use_container_width=True
):

    reject_action()



# ==========================
# Infos
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
# Aide
# ==========================

st.caption(
    "⬅️ précédent   |   ➡️ suivant   |   ⬆️ rejeter"
)