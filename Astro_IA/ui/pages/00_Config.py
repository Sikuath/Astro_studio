import streamlit as st

from core.config import load_config, save_config
from core.config import restore_default


st.title("⚙️ Configuration Astro IA")


config = load_config()


# ==========================
# Ollama
# ==========================

st.header("🧠 Intelligence artificielle")


ollama = config["ollama"]


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



# ==========================
# Chemins logiciels
# ==========================

st.header("🛠️ Logiciels")


paths = config["paths"]


for key,value in paths.items():

    paths[key] = st.text_input(
        key,
        value
    )



# ==========================
# Instruments
# ==========================

st.header("🔭 Instruments")


instruments = config["instruments"]


for identifiant,inst in instruments.items():

    with st.expander(
        inst["name"]
    ):

        inst["name"] = st.text_input(
            "Nom",
            inst["name"]
        )


        inst["type"] = st.text_input(
            "Type",
            inst["type"]
        )


        inst["aperture"] = st.number_input(
            "Diamètre (mm)",
            value=inst["aperture"]
        )


        inst["focal_length"] = st.number_input(
            "Focale (mm)",
            value=inst["focal_length"]
        )


        if "effective_focal_length" in inst:

            inst["effective_focal_length"] = st.number_input(
                "Focale corrigée",
                value=inst["effective_focal_length"]
            )



# ==========================
# Setup actif
# ==========================

st.header("🎯 Configuration actuelle")


setup = st.selectbox(
    "Instrument utilisé",
    options=list(instruments.keys()),
    index=list(instruments.keys())
    .index(
        config["current_setup"]
    )
)


config["current_setup"] = setup



# ==========================
# Validation
# ==========================


st.divider()


if st.button(
    "💾 Valider et enregistrer"
):

    config["ollama"] = ollama
    config["paths"] = paths
    config["instruments"] = instruments

    save_config(config)


    st.success(
        "✅ Configuration sauvegardée"
    )

st.divider()

st.warning(
    "⚠️ Restaurer la configuration usine "
    "effacera tes modifications actuelles."
)


if st.button(
    "🔄 Restaurer configuration usine"
):

    restore_default()

    st.success(
        "✅ Configuration restaurée"
    )

    st.rerun()