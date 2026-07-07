import streamlit as st
from pathlib import Path

from core.pipeline_manager import PipelineManager


def show_preprocessing():

    st.title("🔭 Prétraitement Siril")

    workdir = st.session_state.get("workdir")
    siril_path = st.session_state.get("siril")

    if not workdir or not siril_path:
        st.warning("Projet ou Siril non configuré")
        return

    manager = PipelineManager(workdir, siril_path)

    progress = st.progress(0)
    terminal = st.empty()

    logs = []

    def log(line):
        logs.append(line)
        terminal.code("\n".join(logs[-40:]))

    def callback(line):
        log(line)

    if st.button("🚀 Lancer pipeline complet"):

        ok, logs = manager.run_full(callback=callback)

        if ok:
            progress.progress(1.0)
            st.success("🎉 Pipeline terminé")
        else:
            st.error("❌ Pipeline en erreur")