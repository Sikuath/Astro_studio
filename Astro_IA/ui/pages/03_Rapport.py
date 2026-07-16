# ==========================================================
# Astro IA
# Page 03 - Rapport
# ==========================================================


import streamlit as st
from datetime import datetime



# ==========================================================
# TITRE
# ==========================================================


st.title(
    "📋 Rapport astrophotographique"
)



# ==========================================================
# VERIFICATION
# ==========================================================


if not st.session_state.get(
    "analysis_ready",
    False
):

    st.warning(
        "Aucune analyse disponible."
    )

    st.stop()



# ==========================================================
# RECUPERATION DONNEES
# ==========================================================


header = st.session_state.get(
    "fits_header",
    {}
)


context = st.session_state.get(
    "ai_context",
    {}
)


analysis = st.session_state.get(
    "analysis_result",
    ""
)



# ----------------------------------------------------------
# NOUVEAU : RESULTAT VISION LLAVA
# ----------------------------------------------------------

vision_result = st.session_state.get(
    "vision_result",
    None
)



fov = st.session_state.get(
    "fov",
    {}
)


objects = st.session_state.get(
    "objects",
    []
)



# ==========================================================
# INFORMATIONS ACQUISITION
# ==========================================================


st.header(
    "📷 Acquisition"
)



col1,col2 = st.columns(2)



with col1:


    st.write(
        f"**Objet :** {header.get('OBJECT','?')}"
    )


    st.write(
        f"**Instrument indiqué FITS :** {header.get('INSTRUME','?')}"
    )


    st.write(
        f"**Télescope / système :** {header.get('TELESCOP','?')}"
    )


    st.write(
        f"**Focale :** {header.get('FOCALLEN','?')} mm"
    )



with col2:


    st.write(
        f"**Pose :** {header.get('EXPTIME','?')} s"
    )


    st.write(
        f"**Gain :** {header.get('GAIN','?')}"
    )


    st.write(
        f"**Température capteur :** {header.get('CCD-TEMP','?')} °C"
    )


    st.write(
        f"**Caméra :** {header.get('INSTRUME','?')}"
    )



st.info(
"""
Les informations ci-dessus proviennent des métadonnées FITS.
Elles constituent les données d'acquisition de référence.
"""
)



# ==========================================================
# POSITION
# ==========================================================


st.header(
    "🌌 Position du champ"
)



c1,c2 = st.columns(2)



with c1:

    st.write(
        f"RA : {header.get('RA','?')}"
    )



with c2:

    st.write(
        f"DEC : {header.get('DEC','?')}"
    )



st.info(
"""
Les coordonnées proviennent directement du header FITS.
Elles sont utilisées comme référence pour l'analyse.
"""
)



# ==========================================================
# CHAMP OPTIQUE
# ==========================================================


st.header(
    "📐 Champ photographié"
)



if fov:


    c1,c2,c3 = st.columns(3)



    with c1:

        st.metric(
            "Largeur",
            f"{fov.get('fov_horizontal_deg')}°"
        )



    with c2:

        st.metric(
            "Hauteur",
            f"{fov.get('fov_vertical_deg')}°"
        )



    with c3:

        st.metric(
            "Échantillonnage",
            f"{fov.get('sampling_arcsec_pixel')}\"/pix"
        )



# ==========================================================
# OBJETS CATALOGUES
# ==========================================================


st.header(
    "⭐ Objets catalogués dans le champ"
)



if objects:


    st.write(
        f"{len(objects)} objets conservés après filtrage."
    )


    st.dataframe(
        objects,
        use_container_width=True
    )



else:


    st.info(
        "Aucun objet catalogué."
    )



st.caption(
"""
Les objets proviennent du catalogue Siril.
Ils indiquent des sources cataloguées dans le champ.
Ils ne constituent pas une preuve de qualité d'image.
"""
)



# ==========================================================
# ANALYSE VISION LLAVA
# ==========================================================


st.header(
    "👁️ Analyse visuelle LLaVA"
)



if vision_result:


    st.warning(
"""
Cette analyse est réalisée par un modèle de vision.
Elle correspond à une interprétation visuelle.

Elle ne remplace pas les mesures scientifiques :
FWHM, HFR, excentricité, bruit, suivi ou photométrie.
"""
    )


    st.markdown(
        vision_result
    )


else:


    st.info(
        "Aucune analyse visuelle LLaVA disponible."
    )
# ==========================================================
# ANALYSE IA ASTRO (QWEN3)
# ==========================================================


st.header(
    "🤖 Analyse scientifique Astro IA"
)



if analysis:


    st.markdown(

        analysis

    )


else:


    st.warning(

        "Aucun rapport Astro IA généré."

    )



# ==========================================================
# RESUME DES MODELES UTILISES
# ==========================================================


st.header(
    "🧠 Modèles utilisés"
)


models_info = []


models_info.append(
    "✅ Astro IA scientifique : modèle Ollama principal (Qwen3)"
)


if vision_result:

    models_info.append(
        "✅ Analyse visuelle : LLaVA 7B"
    )


else:

    models_info.append(
        "❌ Analyse visuelle : non utilisée"
    )



for item in models_info:

    st.write(
        item
    )



st.info(
"""
Architecture Astro IA :

- Qwen3 analyse les métadonnées FITS, FOV, catalogue et règles scientifiques.
- LLaVA analyse uniquement l'aspect visuel de l'image.
- Les deux analyses restent séparées.
- Une interprétation visuelle ne peut jamais devenir une mesure scientifique.
"""
)



# ==========================================================
# EXPORT RAPPORT TXT
# ==========================================================


st.divider()


st.header(
    "💾 Export"
)



report_text = f"""

=====================================
Rapport Astro IA
=====================================

Date :
{datetime.now()}


=====================================
ACQUISITION FITS
=====================================


Objet :
{header.get('OBJECT','?')}


Instrument indiqué :
{header.get('INSTRUME','?')}


Télescope :
{header.get('TELESCOP','?')}


Focale :
{header.get('FOCALLEN','?')} mm


Temps de pose :
{header.get('EXPTIME','?')} s


Gain :
{header.get('GAIN','?')}


Température :
{header.get('CCD-TEMP','?')} °C



=====================================
POSITION
=====================================


RA :
{header.get('RA','?')}


DEC :
{header.get('DEC','?')}



=====================================
CHAMP OPTIQUE
=====================================


Largeur :
{fov.get('fov_horizontal_deg','?')} °


Hauteur :
{fov.get('fov_vertical_deg','?')} °


Echantillonnage :
{fov.get('sampling_arcsec_pixel','?')} arcsec/pixel



=====================================
CATALOGUE SIRIL
=====================================


Nombre objets :
{len(objects)}


{objects}



=====================================
ANALYSE VISUELLE LLAVA
=====================================


{vision_result if vision_result else "Aucune analyse visuelle disponible."}



=====================================
ANALYSE ASTRO IA QWEN3
=====================================


{analysis}



=====================================
FIN DU RAPPORT

"""



st.download_button(

    "⬇ Télécharger le rapport TXT",

    report_text,

    file_name=

        f"rapport_{header.get('OBJECT','astro')}.txt",

    mime="text/plain"

)



# ==========================================================
# RETOUR
# ==========================================================


st.divider()



if st.button(

    "⬅ Retour analyse"

):


    st.switch_page(

        "ui/pages/02_Analyse.py"

    )