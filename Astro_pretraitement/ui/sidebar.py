import streamlit as st



def show_sidebar():

    with st.sidebar:


        st.title(
            "🔭 Astro Suite"
        )


        st.divider()



        # ==========================
        # Etat du workflow
        # ==========================

        step = st.session_state.get(
            "workflow_step",
            1
        )



        workflow = [

            (
                1,
                "📁",
                "Projet"
            ),

            (
                2,
                "🔭",
                "Preview Lights"
            ),

            (
                3,
                "📊",
                "Vérification des rejets"
            ),

            (
                4,
                "⚙️",
                "Prétraitement Siril"
            ),

            (
                5,
                "✨",
                "Traitement final"
            )

        ]



        st.subheader(
            "Workflow"
        )



        for number, icon, name in workflow:



            if number < step:

                st.success(
                    f"✅ {number}. {icon} {name}"
                )


            elif number == step:

                st.info(
                    f"➡️ {number}. {icon} {name}"
                )


            else:

                st.write(
                    f"⬜ {number}. {icon} {name}"
                )



        st.divider()



        # ==========================
        # Informations projet
        # ==========================

        if "lights_folder" in st.session_state:

            st.caption(
                "📂 Projet chargé"
            )

        else:

            st.caption(
                "📂 Aucun projet"
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
            © 2026 <b>Sikuath</b> — Astro Suite<br>
            Logiciel distribué sous licence MIT.<br>
            Images, captures d'écran et contenus graphiques<br>
            sous licence <b>CC BY-NC-ND 4.0</b>,<br>
            sauf mention contraire.
        </div>
        """,
        unsafe_allow_html=True
    )