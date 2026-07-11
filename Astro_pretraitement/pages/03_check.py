import streamlit as st
from pathlib import Path

from ui.theme import load_theme
from ui.sidebar import show_sidebar

from core.config import load_config
from core.fits_loader import find_fits
from core.preview import fits_preview
from core.reject import restore_file


# =====================================================
# Configuration page
# =====================================================

st.set_page_config(
    page_title="Vérification des rejets",
    page_icon="🗑️",
    layout="wide"
)


st.session_state.workflow_step = 3


load_theme()
show_sidebar()



# =====================================================
# Titre
# =====================================================

st.title(
    "🗑️ Vérification des images rejetées"
)


st.markdown(
"""
Avant de lancer le prétraitement, vérifiez une dernière fois que
les images présentes dans le dossier **Rejected** sont bien celles
que vous souhaitez écarter.

Vous pouvez restaurer une image en un clic.
"""
)



# =====================================================
# Configuration
# =====================================================

config = load_config()



lights_folder = Path(
    config.get(
        "lights_folder",
        ""
    )
)



rejected_folder = Path(
    config.get(
        "rejected_folder",
        ""
    )
)



# =====================================================
# Aucun dossier Rejected
# =====================================================

if not rejected_folder.exists():


    st.success(
        "✅ Aucune image rejetée."
    )


    col1, col2, col3 = st.columns(
        [2,1,2]
    )


    with col2:


        if st.button(
            "⚙️ Lancer Prétraitement"
        ):


            st.switch_page(
                "pages/04_Pretraitement.py"
            )


    st.stop()



# =====================================================
# Chargement images rejetées
# =====================================================

files = find_fits(
    rejected_folder
)



if len(files) == 0:


    st.success(
        "✅ Le dossier Rejected est vide."
    )


    col1, col2, col3 = st.columns(
        [2,1,2]
    )


    with col2:


        if st.button(
            "⚙️ Lancer Prétraitement"
        ):


            st.switch_page(
                "pages/04_Pretraitement.py"
            )


    st.stop()



st.info(
    f"🗑️ {len(files)} image(s) rejetée(s)."
)



# =====================================================
# Galerie
# =====================================================

cols = st.columns(3)



for i, file in enumerate(files):


    with cols[i % 3]:


        preview = fits_preview(
            file
        )


        st.image(
            preview,
            use_container_width=True
        )


        st.caption(
            file.name
        )



        if st.button(
            "↩ Restaurer",
            key=file.name,
            use_container_width=True
        ):


            restore_file(
                file,
                lights_folder
            )


            st.success(
                "✅ Image restaurée"
            )


            st.rerun()



# =====================================================
# Suite workflow
# =====================================================

st.divider()



col1, col2, col3 = st.columns(
    [2,1,2]
)



with col2:


    if st.button(
        "⚙️ Lancer Prétraitement"
    ):


        st.session_state.workflow_step = 4


        st.switch_page(
            "pages/04_Pretraitement.py"
        )



# =====================================================
# Footer
# =====================================================

st.caption(
    "📁 Projet → 🔭 Preview → 🗑️ Check → ⚙️ Prétraitement"
)