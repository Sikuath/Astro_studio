# ==========================================================
# Astro IA
# Page 00 - Configuration
# ==========================================================


import streamlit as st


from core.config import (
    load_config,
    save_config,
    restore_default
)



# ==========================================================
# PAGE CONFIGURATION
# ==========================================================

st.title(
    "⚙️ Configuration Astro IA"
)



config = load_config()



# ==========================================================
# CREATION COLONNES PRINCIPALES
# ==========================================================

left, right = st.columns(
    2,
    gap="large"
)



# ==========================================================
# COLONNE GAUCHE
# IA + LOGICIELS
# ==========================================================

with left:



    st.header(
        "🧠 Intelligence artificielle"
    )


    ollama = config.get(
        "ollama",
        {}
    )


    ollama["default_model"] = st.text_input(

        "Modèle principal",

        ollama.get(
            "default_model",
            "astro-expert:latest"
        )

    )


    ollama["vision_model"] = st.text_input(

        "Modèle vision",

        ollama.get(
            "vision_model",
            "llava:7b"
        )

    )



    st.divider()



    st.header(
        "🛠️ Logiciels"
    )


    paths = config.get(
        "paths",
        {}
    )


    for key, value in paths.items():


        paths[key] = st.text_input(

            key.replace(
                "_",
                " "
            ).capitalize(),

            value,

            key=f"path_{key}"

        )




# ==========================================================
# COLONNE DROITE
# INSTRUMENTS
# ==========================================================

with right:



    st.header(
        "🔭 Instruments"
    )


    instruments = config.get(
        "instruments",
        {}
    )



    for identifiant, inst in instruments.items():


        with st.expander(

            inst.get(
                "name",
                identifiant
            )

        ):


            inst["name"] = st.text_input(

                "Nom",

                inst.get(
                    "name",
                    identifiant
                ),

                key=f"name_{identifiant}"

            )



            inst["type"] = st.text_input(

                "Type",

                inst.get(
                    "type",
                    ""
                ),

                key=f"type_{identifiant}"

            )



            c1, c2 = st.columns(2)



            with c1:


                inst["aperture"] = st.number_input(

                    "Diamètre mm",

                    value=float(

                        inst.get(
                            "aperture",
                            0
                        )

                    ),

                    key=f"aperture_{identifiant}"

                )



            with c2:


                inst["focal_length"] = st.number_input(

                    "Focale mm",

                    value=float(

                        inst.get(
                            "focal_length",
                            0
                        )

                    ),

                    key=f"focal_{identifiant}"

                )



            if "effective_focal_length" in inst:


                inst["effective_focal_length"] = st.number_input(

                    "Focale corrigée",

                    value=float(

                        inst.get(
                            "effective_focal_length",
                            0
                        )

                    ),

                    key=f"effective_{identifiant}"

                )




    st.divider()



    st.subheader(
        "🎯 Configuration actuelle"
    )


    setup_list = list(
        instruments.keys()
    )


    setup = None



    if setup_list:


        current = config.get(

            "current_setup",

            setup_list[0]

        )



        setup = st.selectbox(

            "Instrument utilisé",

            options=setup_list,

            index=(

                setup_list.index(current)

                if current in setup_list

                else 0

            )

        )


        config["current_setup"] = setup



    else:


        st.info(

            "Aucun instrument configuré."

        )




# ==========================================================
# VALIDATION
# ==========================================================

st.divider()



# Petite zone boutons centrée

b1, b2, b3 = st.columns(
    [2,1,2]
)



with b2:


    save_button = st.button(

        "💾 Enregistrer",

        type="primary"

    )


if save_button:


    config["ollama"] = ollama

    config["paths"] = paths

    config["instruments"] = instruments



    if setup:

        config["current_setup"] = setup



    save_config(

        config

    )


    st.session_state.config_validated = True



    if setup:


        st.session_state.current_setup = setup


        st.session_state.instrument = (

            instruments[setup]
            .get(
                "name",
                setup
            )

        )


    st.success(

        "✅ Configuration enregistrée"

    )


    st.switch_page(

        "ui/pages/01_FITS.py"

    )





# ==========================================================
# RESTAURATION
# ==========================================================

st.divider()



st.warning(

    "⚠️ Restaurer la configuration usine remplacera le fichier actuel."

)



r1, r2, r3 = st.columns(
    [2,1,2]
)



with r2:


    restore_button = st.button(

        "🔄 Restaurer",

    )



if restore_button:


    restore_default()


    st.session_state.config_validated = False



    st.success(

        "✅ Configuration usine restaurée"

    )


    st.rerun()