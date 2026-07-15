from pathlib import Path
import base64

import streamlit as st

from core.config import load_config
from core.session import init_session
from ui.sidebar import show_sidebar


# ============================================================
# CONFIGURATION STREAMLIT
# ============================================================

st.set_page_config(
    page_title="Astro IA",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CHARGEMENT DU CSS + BACKGROUND
# ============================================================

def load_css():

    css_file = Path("ui/style.css")
    bg_file = Path("ui/background.jpg")

    if not css_file.exists():
        return

    css = css_file.read_text(encoding="utf-8")

    if bg_file.exists():

        encoded = base64.b64encode(
            bg_file.read_bytes()
        ).decode()

        css = css.replace(
            "background.jpg",
            f"data:image/jpeg;base64,{encoded}"
        )

    st.markdown(
        f"<style>{css}</style>",
        unsafe_allow_html=True
    )


load_css()


# ============================================================
# INITIALISATION
# ============================================================

config = load_config()

init_session(config)


# ============================================================
# SIDEBAR
# ============================================================

show_sidebar(config)


# ============================================================
# PAGE D'ACCUEIL
# ============================================================

st.title("🤖 Astro IA")

st.markdown(
"""
Bienvenue dans **Astro IA**.

Cet assistant fonctionne **100 % en local** grâce à :

- 🧠 Ollama
- 👁️ Vision IA
- 🔭 Siril
- 🎨 GIMP
- 📷 Lecture FITS
- 📄 Génération de rapports

---

## Workflow

1. ⚙ Configurer Astro IA

2. 📷 Charger une image

3. 📑 Lire le fichier FITS

4. 🤖 Analyse par IA

5. 🪐 Génération du workflow Siril

6. 🎨 Génération du workflow GIMP

7. 📄 Création du rapport final

---

### Philosophie du projet

- ✅ Open Source uniquement

- ✅ Fonctionne hors ligne

- ✅ Aucune API Cloud

- ✅ Aucune donnée envoyée sur Internet

- ✅ Compatible Siril + GIMP

- ✅ Optimisé pour Astro Suite
"""
)


st.info(
    "Sélectionnez une étape du workflow dans la barre latérale pour commencer."
)