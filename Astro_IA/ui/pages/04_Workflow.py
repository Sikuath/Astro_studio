# ==========================================================
# Astro IA
# Page 04 - Workflow astrophotographique
# ==========================================================


import streamlit as st


from core.workflow_manager import (
    get_workflow,
    toggle_step,
    workflow_summary
)


from core.project_state import (
    load_project_state
)



# ==========================================================
# TITRE
# ==========================================================


st.title(
    "🧭 Workflow astrophotographique"
)





# ==========================================================
# VERIFICATION PROJET
# ==========================================================


project_path = st.session_state.get(
    "project_path"
)



if not project_path:


    st.warning(
        "⚠️ Aucun projet actif."
    )


    st.stop()





# ==========================================================
# CHARGEMENT ETAT PROJET
# ==========================================================


project_state = load_project_state(

    project_path

)



workflow = get_workflow(

    project_path

)



summary = workflow_summary(

    project_path

)





# ==========================================================
# AVANCEMENT
# ==========================================================


st.header(
    "📊 Avancement"
)



st.progress(

    summary["progress"]

    /

    100

)



st.write(

    f"**{summary['done']} / {summary['total']} étapes terminées**"

)





if project_state.get(

    "workflow_updated"

):


    st.caption(

        "Dernière modification : "

        +

        project_state["workflow_updated"]

    )





st.divider()





# ==========================================================
# ETAPES
# ==========================================================


st.header(
    "🔭 Étapes Astro IA"
)



for step in workflow:


    step_id = step["id"]


    current = step["done"]


    label = step["name"]





    if current:

        display = (

            "✅ "

            +

            label

        )

    else:

        display = (

            "⬜ "

            +

            label

        )





    value = st.checkbox(

        display,

        value=current,

        key=f"workflow_{step_id}"

    )





    if value != current:


        toggle_step(

            project_path,

            step_id

        )


        st.rerun()







# ==========================================================
# MESSAGE
# ==========================================================


st.divider()



st.info(
"""
Le workflow est enregistré dans le projet.

Cette page sert uniquement au suivi de progression.

Aucune analyse Siril, LLaVA ou Qwen3
n'est relancée automatiquement.

Vous pouvez fermer Astro IA et reprendre
plus tard exactement à cette étape.
"""
)





# ==========================================================
# RETOUR
# ==========================================================


if st.button(

    "⬅ Retour analyse"

):


    st.switch_page(

        "ui/pages/02_Analyse.py"

    )