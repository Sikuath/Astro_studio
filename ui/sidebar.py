import streamlit as st

def sidebar():

    st.sidebar.title("🔭 Astro Studio")

    # ─────────────────────────────
    # PROJET ACTIF (lecture seule)
    # ─────────────────────────────
    st.sidebar.markdown("## 📁 Projet actif")

    workdir = st.session_state.get("workdir")
    siril = st.session_state.get("siril")

    if workdir:
        st.sidebar.success(f"📂 {workdir}")
    else:
        st.sidebar.warning("Aucun dossier sélectionné")

    if siril:
        st.sidebar.info(f"⚙️ Siril : {siril}")

    st.sidebar.markdown("---")

    # ─────────────────────────────
    # STATUS
    # ─────────────────────────────
    st.sidebar.markdown("## 🧠 État")

    st.sidebar.write(
        "Config :",
        "OK" if st.session_state.get("config") else "Non chargée"
    )

    st.sidebar.write("Session :", "active")

    st.sidebar.markdown("---")

    # ─────────────────────────────
    # NAVIGATION
    # ─────────────────────────────
    st.sidebar.markdown("## 🚀 Workflow")

    page = st.sidebar.radio(
        "Aller à",
        [
            "Accueil",
            "Projet",
            "Traitement",
            "Résultats"
        ]
    )

    st.session_state["page"] = page

    st.sidebar.markdown("---")

    # ─────────────────────────────
    # AIDE
    # ─────────────────────────────
    st.sidebar.markdown("## ❓ Aide")

    st.sidebar.caption(
        "Configure ton projet dans l’onglet Projet.\n"
        "Puis lance le traitement dans l’onglet dédié."
    )

    return page