import streamlit as st
from pathlib import Path


# ==========================================================
# SIDEBAR
# ==========================================================

def show_sidebar(config):

    with st.sidebar:

        # ==========================================
        # IMAGE
        # ==========================================

        img = Path("ui/background.jpg")

        if img.exists():

            st.image(
                str(img),
                use_container_width=True
            )

        # ==========================================
        # TITRE
        # ==========================================

        st.title("🤖 Astro IA")

        st.caption(
            "Assistant astrophotographique local"
        )

        st.divider()

        # ==========================================
        # WORKFLOW
        # ==========================================

        st.subheader("📂 Workflow")

        workflow = [

            ("Configuration", "config_validated"),
            ("Analyse", "analysis_ready"),
            ("FITS", "fits_loaded"),
            ("Rapport", "report_ready")

        ]

        for name, key in workflow:

            if st.session_state.get(key, False):

                st.success(f"✔ {name}")

            else:

                st.info(f"○ {name}")

        st.divider()

        # ==========================================
        # IA
        # ==========================================

        st.subheader("🖥 IA")

        st.write(
            f"**Assistant :** "
            f"{config['ollama']['default_model']}"
        )

        st.write(
            f"**Vision :** "
            f"{config['ollama']['vision_model']}"
        )

        st.divider()

        # ==========================================
        # SESSION
        # ==========================================

        st.subheader("🔭 Session")

        instrument = st.session_state.get(
            "instrument",
            "Aucun"
        )

        objet = st.session_state.get(
            "object",
            "Aucun"
        )

        image = st.session_state.get(
            "image_name",
            "Aucune"
        )

        st.write(f"**Instrument :** {instrument}")

        st.write(f"**Objet :** {objet}")

        st.write(f"**Image :** {image}")

        st.divider()

        # ==========================================
        # VERSION
        # ==========================================

        st.caption("Astro Suite")

        st.caption("Astro IA v0.1")

                # ─────────────────────────────
        # FOOTER SIDEBAR
        # ─────────────────────────────

        st.markdown(

            """

            <style>

            .astro-sidebar-footer {

                margin-top: 40px;

                padding-top: 15px;

                border-top: 1px solid rgba(255,255,255,0.15);

                text-align: center;

                font-size: 0.55em;

                color: #888;

                line-height: 1.5;

            }

            </style>


            <div class="astro-sidebar-footer">

            © 2026 <b>Sikuath</b> — Astro Suite<br>
            Logiciel distribué sous licence MIT.<br>
            Images, captures d'écran et contenus graphiques<br>
            sous licence <b>CC BY-NC-ND 4.0</b>,<br>
            sauf mention contraire.

            </div>

            """,

            unsafe_allow_html=True

        )
