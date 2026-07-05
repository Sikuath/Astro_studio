import streamlit as st
import numpy as np
from scipy.ndimage import zoom as spzoom
from pathlib import Path

from core.fits_io import load_fits, save_fits
from core.processing import mix_sho, apply_palette
from core.preview import make_preview


def run():

    st.title("🌈 SHO Mixer")

    # =========================
    # PROJET
    # =========================
    workdir = st.session_state.get("workdir")

    if not workdir:
        st.warning("Projet non défini — va dans l’onglet Projet")
        st.stop()

    path = Path(workdir)

    S_path = path / "SII.fit"
    H_path = path / "HA.fit"
    O_path = path / "OIII.fit"

    if not (S_path.exists() and H_path.exists() and O_path.exists()):
        st.error("Fichiers SHO introuvables dans le dossier")
        st.stop()

    # =========================
    # LOAD FITS
    # =========================
    S, _ = load_fits(S_path)
    H, _ = load_fits(H_path)
    O, _ = load_fits(O_path)

    # =========================
    # LAYOUT
    # =========================
    col_left, col_right = st.columns([1, 2])

    # =========================
    # LEFT PANEL (CONTROLS)
    # =========================
    with col_left:

        st.subheader("🎛 Contrôles")

        palette = st.selectbox(
            "Palette",
            [
                "Manual",
                "Hubble SHO",
                "HOO Boost",
                "HOO Natural",
                "Hα Rich",
                "OIII Rich",
                "Foraxx Pro",
                "Gold & Blue",
                "Teal & Orange"
            ],
            key="sho_palette"
        )

        stretch = st.slider("Stretch", 0.5, 10.0, 3.0, key="sho_stretch")
        zoom = st.slider("Zoom", 1.0, 2.0, 1.0, key="sho_zoom")

        st.markdown("---")

        st.subheader("🎨 RGB Mix")

        # palette par défaut
        r_s, r_h, g_h, g_o, b_o = apply_palette(palette)

        # sliders UNIQUEMENT en mode manual + keys obligatoires
        if palette == "Manual":

            r_s = st.slider("R SII", 0.0, 1.0, 0.8, key="sho_r_s")
            r_h = st.slider("R Hα", 0.0, 1.0, 0.2, key="sho_r_h")
            g_h = st.slider("G Hα", 0.0, 1.0, 0.7, key="sho_g_h")
            g_o = st.slider("G OIII", 0.0, 1.0, 0.3, key="sho_g_o")
            b_o = st.slider("B OIII", 0.0, 1.0, 1.0, key="sho_b_o")

        st.markdown("---")
        st.write(f"📁 Projet : `{workdir}`")

    # =========================
    # CORE PROCESSING
    # =========================
    R, G, B = mix_sho(S, H, O, r_s, r_h, g_h, g_o, b_o)

    RGB = make_preview(R, G, B, stretch)

    if zoom > 1:
        RGB = spzoom(RGB, (zoom, zoom, 1), order=1)

    # =========================
    # RIGHT PANEL (PREVIEW)
    # =========================
    with col_right:

        st.subheader("👁 Preview")

        st.image(RGB, use_container_width=True)

        st.markdown("---")

        if st.button("Export FITS (RGB linear)", key="sho_export"):

            save_fits(path / "R.fit", R)
            save_fits(path / "G.fit", G)
            save_fits(path / "B.fit", B)

            st.success("Export terminé ✔")