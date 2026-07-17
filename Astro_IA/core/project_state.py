# ==========================================================
# Astro IA
# Gestion état projet
# ==========================================================


import json
from pathlib import Path




# ==========================================================
# FICHIER ETAT PROJET
# ==========================================================


def get_state_file(project_path):

    project_path = Path(
        project_path
    )


    return project_path / "project_state.json"






# ==========================================================
# CHARGEMENT
# ==========================================================


def load_project_state(project_path):


    state_file = get_state_file(
        project_path
    )


    if not state_file.exists():


        return {}



    try:


        with open(

            state_file,

            "r",

            encoding="utf-8"

        ) as f:


            return json.load(f)



    except Exception as e:


        print(
            "Erreur lecture project_state :",
            e
        )


        return {}






# ==========================================================
# SAUVEGARDE
# ==========================================================


def save_project_state(

    project_path,

    data

):


    state_file = get_state_file(

        project_path

    )


    try:


        with open(

            state_file,

            "w",

            encoding="utf-8"

        ) as f:


            json.dump(

                data,

                f,

                indent=4,

                ensure_ascii=False

            )



    except Exception as e:


        print(

            "Erreur sauvegarde project_state :",

            e

        )