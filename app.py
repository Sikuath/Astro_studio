import streamlit as st
from pathlib import Path
import base64

from ui.sidebar import sidebar

from ui.pages.home import show_home
from ui.pages.project import show_project
from tools.sho_mixer import sho_mixer
#from ui.pages.results import show_results


# ─────────────────────────────────────
# CONFIG STREAMLIT
# ─────────────────────────────────────
st.set_page_config(
    page_title="Astro Studio",
    page_icon="🔭",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ─────────────────────────────────────
# CSS + BACKGROUND
# ─────────────────────────────────────
def load_css():

    css_path = Path("ui/style.css")

    if css_path.exists():
        st.markdown(
            f"<style>{css_path.read_text(encoding='utf-8')}</style>",
            unsafe_allow_html=True
        )


def set_background():

    img_path = Path("ui/background.jpg")

    if img_path.exists():
        with open(img_path, "rb") as f:
            encoded = base64.b64encode(f.read()).decode()

        st.markdown(
            f"""
            <style>
            .stApp {{
                background-image: url("data:image/png;base64,{encoded}");
                background-size: cover;
                background-position: center;
                background-attachment: fixed;
            }}
            </style>
            """,
            unsafe_allow_html=True
        )


# ─────────────────────────────────────
# INIT STATE
# ─────────────────────────────────────
def init_state():
    defaults = {
        "page": "Accueil",
        "workdir": None,
        "siril": None,
        "config": None,
    }

    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


init_state()


# ─────────────────────────────────────
# STYLE GLOBAL (IMPORTANT)
# ─────────────────────────────────────
load_css()
set_background()


# ─────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────
page = sidebar()


# ─────────────────────────────────────
# ROUTING
# ─────────────────────────────────────
if page == "Accueil":
    show_home()

elif page == "Projet":
    show_project()

elif page == "Traitement":
    sho_mixer()

elif page == "Résultats":
    show_results()

else:
    st.error("Page inconnue")


# ─────────────────────────────────────
# FOOTER
# ─────────────────────────────────────
st.markdown("---")

st.caption("🔭 Astro Studio — pipeline astrophotographie (Siril + Streamlit)")