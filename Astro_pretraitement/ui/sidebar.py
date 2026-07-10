import streamlit as st


def show_sidebar():

    with st.sidebar:

        st.title("🔭 Astro Prétraitement")

        st.divider()

        st.page_link(
            "pages/01_Project.py",
            label="Projet",
            icon="📁"
        )

        st.page_link(
            "pages/02_Preview.py",
            label="Preview Lights",
            icon="🔭"
        )

        st.page_link(
            "pages/03_Pretraitement.py",
            label="Prétraitement Siril",
            icon="⚙️"
        )

        st.divider()

        st.caption(
            "Astro Suite"
        )

 # ─────────────────────────────
    # FOOTER SIDEBAR
    # ─────────────────────────────

    st.sidebar.markdown(
        """
        <div style="
            position: fixed;
            bottom: 8px;
            left: 15px;
            width: 220px;
            text-align: center;
            font-size: 0.55em;
            color: #888;
            line-height: 1.4;
        ">
            © 2026 <b>Sikuath</b> — Astro Studio<br>
            Logiciel distribué sous licence MIT.<br>
            Images, captures d'écran et contenus graphiques<br>
            sous licence <b>CC BY-NC-ND 4.0</b>,<br>
            sauf mention contraire.
        </div>
        """,
        unsafe_allow_html=True
    )