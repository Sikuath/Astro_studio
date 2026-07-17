# ==========================================================
# Astro IA
# Gestion du workflow astrophotographique
# ==========================================================


from datetime import datetime


from core.project_state import (
    load_project_state,
    save_project_state
)



# ==========================================================
# WORKFLOW ASTRO IA PAR DEFAUT
# ==========================================================


DEFAULT_WORKFLOW = [

    {
        "id": "fits",
        "name": "FITS validé",
        "done": False
    },


    {
        "id": "siril",
        "name": "Analyse du champ Siril",
        "done": False
    },


    {
        "id": "catalog",
        "name": "Filtrage catalogue objets",
        "done": False
    },


    {
        "id": "simbad",
        "name": "Enrichissement SIMBAD",
        "done": False
    },


    {
        "id": "vision",
        "name": "Analyse visuelle LLaVA",
        "done": False
    },


    {
        "id": "astro_ai",
        "name": "Analyse scientifique Astro IA",
        "done": False
    },


    {
        "id": "report",
        "name": "Rapport astrophotographique",
        "done": False
    },


    {
        "id": "processing",
        "name": "Traitement de l'image finale",
        "done": False
    }

]



# ==========================================================
# INITIALISATION WORKFLOW
# ==========================================================


def init_workflow(project_path):

    data = load_project_state(
        project_path
    )


    if not data.get("workflow"):


        data["workflow"] = DEFAULT_WORKFLOW


        data["workflow_updated"] = (
            datetime.now()
            .isoformat()
        )


        save_project_state(

            project_path,

            data

        )


    return data["workflow"]





# ==========================================================
# RECUPERATION WORKFLOW
# ==========================================================


def get_workflow(project_path):

    data = load_project_state(

        project_path

    )


    workflow = data.get(

        "workflow",

        []

    )



    if not workflow:


        workflow = init_workflow(

            project_path

        )



    return workflow





# ==========================================================
# MODIFICATION D'UNE ETAPE
# ==========================================================


def set_step(

    project_path,

    step_id,

    state

):


    data = load_project_state(

        project_path

    )


    workflow = data.get(

        "workflow",

        []

    )



    for step in workflow:


        if step["id"] == step_id:


            step["done"] = state


            break




    data["workflow"] = workflow



    data["workflow_updated"] = (

        datetime.now()

        .isoformat()

    )



    save_project_state(

        project_path,

        data

    )







# ==========================================================
# INVERSION D'UNE ETAPE
# ==========================================================


def toggle_step(

    project_path,

    step_id

):


    workflow = get_workflow(

        project_path

    )



    for step in workflow:


        if step["id"] == step_id:



            set_step(

                project_path,

                step_id,

                not step["done"]

            )


            return






# ==========================================================
# PROGRESSION
# ==========================================================


def workflow_progress(

    project_path

):


    workflow = get_workflow(

        project_path

    )



    if not workflow:

        return 0





    done = sum(

        1

        for step in workflow

        if step["done"]

    )



    return int(

        done

        /

        len(workflow)

        *

        100

    )







# ==========================================================
# RESUME WORKFLOW
# ==========================================================


def workflow_summary(

    project_path

):


    workflow = get_workflow(

        project_path

    )



    done = sum(

        1

        for step in workflow

        if step["done"]

    )



    return {


        "total":

            len(workflow),



        "done":

            done,



        "progress":

            workflow_progress(

                project_path

            )

    }